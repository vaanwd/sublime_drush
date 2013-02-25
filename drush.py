import platform
import sublime
import sublime_plugin
import re
import os

os.environ["TERM"] = "dumb"
PLATFORM_IS_WINDOWS = platform.system() is 'Windows'

class DrushCommand(sublime_plugin.TextCommand):
  working_dirs = ''
  path = ''
  folders = []
  DEFAULT_DRUSH_EXECUTABLE = 'drush.bat' if PLATFORM_IS_WINDOWS else 'drush'
  SETTINGS = sublime.load_settings("Drush.sublime-settings")
  view_panel = None
  last_cmd = ''

  def run(self, edit):
    view = self.view
    self.working_dirs = view.window().folders()
    if len(self.working_dirs) > 0:
      self.path = self.working_dirs[0]
      self.view_panel = view.window().show_input_panel('drush', self.last_cmd, self.after_input, self.on_change, None)
      self.view_panel.set_name('drush_command_bar')
    else:
      sublime.message_dialog('No opened project was found!\nPlease open a Drupal project!')

  def after_input(self, text):
    if text.strip() == "":
      sublime.status_message("No command provided")
      return
    else:
      self._runDrush(text)

  def on_change(self, text):
    if text.strip() == "":
      return

    if self.SETTINGS.get('remember_last_command') or True :
      self.last_cmd = text.strip()

  def _runDrush(self, text):
    try:
      root = ''
      uri = ''
      command_splitted = ''
      drush = str(self._get_drush_executable().strip())
      drush_args = str(self._get_drush_sup_args().strip()).replace('\\', '/')
      drush_project_args = str(self._get_drush_sup_project_args().strip()).replace('\\', '/')

      if "--root=" in drush_args:
        root = ''
      elif "--root=" in drush_project_args:
        root = ''
      elif "--root=" in text:
        root = ''
      else:
        root = str('--root=' + self.path).replace('\\', '/')

      if "--uri=" in drush_args:
        uri = ''
      elif "--uri=" in drush_project_args:
        uri = ''
      elif "--uri=" in text:
        uri = ''

      import shlex
      command_splitted = shlex.split(str(drush + ' ' + drush_args + ' ' + drush_project_args + ' ' + text.replace('\\', '/') + ' ') + root + uri)

      sublime.active_window().run_command('exec', {'cmd': command_splitted, "working_dir": self.path})
    except OSError as e:
        error_message = 'Drush error: '
        if e.errno is 2:
            error_message += 'Could not find your "drush" executable.'
        error_message += str(e)

        sublime.status_message(error_message)
        return ('', error_message)

  def _get_drush_executable(self):
    return self.SETTINGS.get('drush_executable') or self.DEFAULT_DRUSH_EXECUTABLE

  def getDirectories(self):
    return sublime.active_window().folders()

  # Credit to titoBouzout - https://github.com/titoBouzout/SideBarEnhancements
  def getProjectFile(self):
    if not self.getDirectories():
      return None
    import json
    data = file(os.path.normpath(os.path.join(sublime.packages_path(), '..', 'Settings', 'Session.sublime_session')), 'r').read()
    data = data.replace('\t', ' ')
    data = json.loads(data, strict=False)
    projects = data['workspaces']['recent_workspaces']

    if os.path.lexists(os.path.join(sublime.packages_path(), '..', 'Settings', 'Auto Save Session.sublime_session')):
      data = file(os.path.normpath(os.path.join(sublime.packages_path(), '..', 'Settings', 'Auto Save Session.sublime_session')), 'r').read()
      data = data.replace('\t', ' ')
      data = json.loads(data, strict=False)
      if 'workspaces' in data and 'recent_workspaces' in data['workspaces'] and data['workspaces']['recent_workspaces']:
        projects += data['workspaces']['recent_workspaces']
      projects = list(set(projects))
    for project_file in projects:
      project_file = re.sub(r'^/([^/])/', '\\1:/', project_file);
      project_json = json.loads(file(project_file, 'r').read(), strict=False)
      if 'folders' in project_json:
        folders = project_json['folders']
        found_all = True
        for directory in self.getDirectories():
          found = False
          for folder in folders:
            folder_path = re.sub(r'^/([^/])/', '\\1:/', folder['path']);
            if folder_path == directory.replace('\\', '/'):
              found = True
              break;
          if found == False:
            found_all = False
            break;
      if found_all:
        return project_file
    return None

  def hasOpenedProject(self):
    return self.getProjectFile() != None

  def getProjectJson(self):
    if not self.hasOpenedProject():
      return None
    import json
    return json.loads(file(self.getProjectFile(), 'r').read(), strict=False)

  def _get_drush_sup_args(self):
    return self.SETTINGS.get('drush_args')

  def _get_drush_sup_project_args(self):
    p_drush_args = self.getProjectJson()
    if 'settings' in p_drush_args:
      if 'Drush' in p_drush_args['settings']:
        if 'drush_args' in p_drush_args['settings']['Drush']:
          return p_drush_args['settings']['Drush']['drush_args']
    return ''
