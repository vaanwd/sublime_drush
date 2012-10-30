import platform
import sublime
import sublime_plugin
import os

os.environ["TERM"] = "dumb"
PLATFORM_IS_WINDOWS = platform.system() is 'Windows'

class DrushCommand(sublime_plugin.TextCommand):
  working_dirs = ''
  path = ''
  folders = []
  DEFAULT_DRUSH_EXECUTABLE = 'drush.bat' if PLATFORM_IS_WINDOWS else 'drush'
  DEFAULT_DRUSH_ARGS = ''
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
      drush = str(self._get_drush_executable().strip())
      drush_args = str(self._get_drush_sup_args().strip())
      command_splitted = ''
      import shlex
      if drush_args != '':
        command_splitted = [drush] + [drush_args] + shlex.split(str(text)) + [str('--root=' + self.path)]
      else:
        command_splitted = [drush] + shlex.split(str(text)) + [str('--root=' + self.path)]
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

  def _get_drush_sup_args(self):
    return self.SETTINGS.get('drush_args') or self.DEFAULT_DRUSH_ARGS
