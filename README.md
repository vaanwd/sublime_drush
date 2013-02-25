# Sublime Text 2 Drush Package

A simple package to run Drupal drush from Sublime Text editor.

##Screenshots
<br/>
![Drush Insert Command](http://www.vaanwebdesign.ro/includes/images/sublime_drush_1.png)
<br/>
Open command bar with `alt`+`shift`+`d` (Windows)
<br/>
<br/>
![Drush Results]
(http://www.vaanwebdesign.ro/includes/images/sublime_drush_2.png)
<br/>
Drush results

For a complete list of drush commands, please visit the [official site](http://drush.ws/).

## Installation

Easiest way to install the plugin is to use [Package Control](http://wbond.net/sublime_packages/package_control).

Alternatively you can clone with git directly into `Packages` directory in the Sublime Text 2 application settings area. The directory name must be `Drush` without quotes.

### Using Git

Go to your Sublime Text 2 `Packages` directory and clone the repository using the command below:

    git clone https://github.com/vaanwd/sublime_drush "Drush"

### Download Manually

* Download the files using the GitHub .zip download option
* Unzip the files and rename the folder to `Drush`
* Copy the folder to your Sublime Text 2 `Packages` directory

## Usage

Sublime Drush is a simple plugin that allows execution of drush commands from Sublime Text Editor.

To use, you must enable input console with `alt` + `shift` + `d` (Win / Linux) or `shift` + `super` + `d` (Mac).

From the Sublime menu `Preferences`->`Package Settings`->`Drush`->`Settings - User` you can set the path to drush utility and other arguments.

For example you can set answer `"yes"` to all questions required by drush adding:

    "drush_args": "--yes",


You can also set the arguments used by drush for each Sublime project accesed from Sublime menu `Project`->`Edit Project`.

An example for **PROJECT.sublime-project**:

    {
      "folders":
      [
        {
          "path": "/E/UwAmp/www/drupal7"
        }
      ],
      "settings":
      {
        "Drush":
        {
          "drush_args": "--uri=http://d7.com"
        }
      }
    }

**NOTE:** You should avoid introducing identical parameters in **Drush.sublime-settings** file and **PROJECT.sublime-project**
to avoid incorrect operations.

[&copy; 2012 Vaan Web Design](http://www.vaanwebdesign.ro)
