#
# Licensed under the GNU General Public License Version 3
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#

# NOTE: the 'self' variable is an instance of KodiShell

# wildcard import
# pylint: disable=W0401,W0614

# unused argument
# pylint: disable=W0613

# invalid function name
# pylint: disable=C0103

import logging
import readline
import shlex
from getpass import getpass
from ConfigParser import NoOptionError
#from spacecmd.utils import *
from kodicmd.utils import *
from time import sleep
import xmlrpclib

from jsonrpc import JSONRPC

SEPARATOR = '\n' + '#' * 30 + '\n'

####################

def help_clear(self):
    print 'clear: clear the screen'
    print 'usage: clear'


def do_clear(self, args):
    os.system('clear')

####################

def help_help(self):
    print 'help: Show help for the given command'
    print 'usage: help COMMAND'

####################

def help_history(self):
    print 'history: List your command history'
    print 'usage: history'


def do_history(self, args):
    for i in range(1, readline.get_current_history_length()):
        print '%s  %s' % (str(i).rjust(4), readline.get_history_item(i))

####################

def help_toggle_confirmations(self):
    print 'toggle_confirmations: Toggle confirmation messages on/off'
    print 'usage: toggle_confirmations'


def do_toggle_confirmations(self, args):
    if self.options.yes:
        self.options.yes = False
        print 'Confirmation messages are enabled'
    else:
        self.options.yes = True
        logging.warning('Confirmation messages are DISABLED!')

####################

def help_whoamitalkingto(self):
    print 'whoamitalkingto: Print the name of the server'
    print 'usage: whoamitalkingto'


def do_whoamitalkingto(self, args):
    try:
        res = self.ph.GetSSetting('services.devicename')
        print "%s @ %s (http://%s:%s/jsonrpc)" % (res,self.ph.host,self.ph.host,self.ph.port)
    except:
        print "Nobody! There is no connection to kodi"

####################

#
#def tab_complete_errata(self, text):
#    options = self.do_errata_list('', True)
#    options.append('search:')
#
#    return tab_completer(options, text)
#
#
#def tab_complete_systems(self, text):
#    if re.match('group:', text):
#        # prepend 'group' to each item for tab completion
#        groups = ['group:%s' % g for g in self.do_group_list('', True)]
#
#        return tab_completer(groups, text)
#    elif re.match('channel:', text):
#        # prepend 'channel' to each item for tab completion
#        channels = ['channel:%s' % s
#                    for s in self.do_softwarechannel_list('', True)]
#
#        return tab_completer(channels, text)
#    elif re.match('search:', text):
#        # prepend 'search' to each item for tab completion
#        fields = ['search:%s:' % f for f in self.SYSTEM_SEARCH_FIELDS]
#        return tab_completer(fields, text)
#    else:
#        options = self.get_system_names()
#
#        # add our special search options
#        options.extend(['group:', 'channel:', 'search:'])
#
#        return tab_completer(options, text)
#

def remove_last_history_item(self):
    last = readline.get_current_history_length() - 1

    if last >= 0:
        readline.remove_history_item(last)



def user_confirm(self, prompt='Is this ok [y/N]:', nospacer=False,
                 integer=False, ignore_yes=False):

    if self.options.yes and not ignore_yes:
        return True

    if nospacer:
        answer = prompt_user('%s' % prompt)
    else:
        answer = prompt_user('\n%s' % prompt)

    if re.match('y', answer, re.I):
        if integer:
            return 1
        else:
            return True
    else:
        if integer:
            return 0
        else:
            return False


# replace the current line buffer
def replace_line_buffer(self, msg=None):
    # restore the old buffer if we weren't given a new line
    if not msg:
        msg = readline.get_line_buffer()

    # don't print a prompt if there wasn't one to begin with
    if len(readline.get_line_buffer()):
        new_line = '%s%s' % (self.prompt, msg)
    else:
        new_line = '%s' % msg

    # clear the current line
    self.stdout.write('\r'.ljust(len(self.current_line) + 1))
    self.stdout.flush()

    # write the new line
    self.stdout.write('\r%s' % new_line)
    self.stdout.flush()

    # keep track of what is displayed so we can clear it later
    self.current_line = new_line


def load_config_section(self, section):
    config_opts = ['host','port']

    if not self.config_parser.has_section(section):
        logging.debug('Configuration section [%s] does not exist', section)
        return

    logging.debug('Loading configuration section [%s]', section)

    for key in config_opts:
        # don't override command-line options
        if self.options.__dict__[key]:
            # set the config value to the command-line argument
            self.config[key] = self.options.__dict__[key]
            if key == 'host':
                self.ph.host = self.config[key]
            if key == 'port':
                self.ph.port = self.config[key]
        else:
            try:
                self.config[key] = self.config_parser.get(section, key)
            except NoOptionError:
                pass
    if str(self.config['host']) != "":
        self.ph.host = self.config['host']
    if str(self.config['port']) != "":
        self.ph.port = self.config['port']

    # handle the nossl boolean
    if self.config.has_key('nossl') and isinstance(self.config['nossl'], str):
        if re.match('^1|y|true$', self.config['nossl'], re.I):
            self.config['nossl'] = True
        else:
            self.config['nossl'] = False

    # Obfuscate the password with asterisks
    config_debug = self.config.copy()
    if config_debug.has_key('password'):
        config_debug['password'] = "*" * len(config_debug['password'])

    logging.debug('Current Configuration: %s', config_debug)
