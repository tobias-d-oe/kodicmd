# kodicmd

kodicmd is an interactive commandline tool for kodi mediacenter.
Its main purpose is to manage one or more kodi installations remote via commandline.
With the current version it's possible to remotecontrol kodi, browse movies also you can gather or change video library. 
Settings can be managed too and Library-Scan can be triggered.
The main goal of the tool is a easy way to automate tasks on kodi and to bring it into monitoring.
With this tool in background you are/will be able to create scripts to make special configurations and or setup a new installed kodi.

Installation:
-------------

1. check out the code:

  $ git clone https://github.com/tobias-d-oe/kodicmd.git

2. install it:

  $ cd kodicmd
  $ sudo python setup.py install


Usage:
------

There are multiple ways to use kodicmd. The easyest way is to start kodi without any parameter and use the interactive shell.
Within this interactive shell you can use the tab-key to autocomplete commands and content.

Example:
--------
-------------------------------------------------------------------------
  $ kodicmd
  Welcome to kodicmd, a command-line interface to kodi.
  
  Type: 'help' for a list of commands
        'help <cmd>' for command-specific help
        'quit' to quit
  
  kodicmd> whoamitalkingto
  osmc @ 192.168.0.40 (http://192.168.0.40:80/jsonrpc)
  kodicmd> system_getplatform
  RaspberryPi
  kodicmd> system_setvolume 77
  kodicmd> system_getvolume
  77
  kodicmd> settings_getsettings locale.timezone
  locale.timezone = Europe/Berlin
  kodicmd> settings_getsettings debug.extralogging
  debug.extralogging = True
  kodicmd> settings_setsettings debug.extralogging false
  {"id":1,"jsonrpc":"2.0","result":true}
  kodicmd> settings_getsettings debug.extralogging
  debug.extralogging = False
  kodicmd> system_getproperty Window(home).Property(NewsCenter.Bundesland)
  Bayern
  kodicmd> exit
-------------------------------------------------------------------------


An other way is to start kodicmd with commandline optinons:

Example:
--------
-------------------------------------------------------------------------
  $ kodicmd system_setvolume 55
  $ kodicmd system_getvolume
    55
  $
-------------------------------------------------------------------------

Third way is to pipe in commands:

Example:
--------
-------------------------------------------------------------------------
  $ echo -e "system_setvolume 63\nsystem_getvolume\nexit\n" | kodicmd
-------------------------------------------------------------------------


It is still in developement state, comitters are welcome!

Already implemented subcommands:
--------------------------------
 - addon_count
 - addon_detail
 - addon_enabled
 - addon_execute
 - addon_getnamebyid
 - addon_getpropertybyid
 - addon_list
 - addon_listbroken
 - addon_listdisabled
 - gui_activatewindow
 - gui_getproperty
 - media_exportvideolibrary
 - media_scanvideosources
 - media_sourceslist
 - movie_count
 - movie_getdetails
 - movie_list
 - movie_listgenre
 - movie_play
 - movie_setdetail
 - player_getactiveplayer
 - player_playpause
 - player_stop
 - rc
 - rc_text
 - settings_getsettings
 - settings_resetsettings
 - settings_setsettings
 - system_connect
 - system_getapiversion
 - system_getbuild
 - system_getkernel
 - system_getname
 - system_getplatform
 - system_getproperty
 - system_gettime
 - system_getversion
 - system_getvolume
 - system_ismuted
 - system_mutetoggle
 - system_ping
 - system_quit
 - system_setvolume
 - whoamitalkingto

