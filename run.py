#!/usr/bin/python

from optparse import OptionParser
import os
import ConfigParser
from lib.ost import OST
from slackbot.bot import respond_to
import re


@respond_to('help', re.IGNORECASE)
def help(message):
    message.reply("Hello! I'm your friendly neighborhood OpenStack Slack bot. "
                  "You can say, 'list', 'list states', 'start the_instance', 'stop the_instance', "
                  "and 'reboot the_instance'. Pretty cool right!"
                  "Please be sure to replace the_instance with the actual instance name.")


@respond_to('list', re.IGNORECASE)
def list(message):
    message.reply("Fetching instances for you...")
    message.reply(nova.get_instance_names_string())
    message.reply("That's all of them.  Enjoy!")


@respond_to('list states', re.IGNORECASE)
def list(message):
    message.reply("Fetching instances with current states for you...")
    message.reply(nova.get_instances_with_states_string())
    message.reply("That's all of them.  Enjoy!")


@respond_to('start (.*)', re.IGNORECASE)
def start(message, instance):
    if nova.poweron_server_by_name(instance):
        message.reply("Attempted to start %s for you. Enjoy!" % instance)
    else:
        message.reply("Sorry, I could not find %s.  Maybe you should try running 'list states" % instance)


@respond_to('stop (.*)', re.IGNORECASE)
def stop(message, instance):
    if nova.shutdown_server_by_name(instance):
        message.reply("Attempted to stop %s for you. Enjoy!" % instance)
    else:
        message.reply("Sorry, I could not find %s.  Maybe you should try running 'list states" % instance)


@respond_to('reboot (.*)', re.IGNORECASE)
def reboot(message, instance):
    if nova.reboot_server_by_name(instance):
        message.reply("Attempted to reboot %s for you. Enjoy!" % instance)
    else:
        message.reply("Sorry, I could not find %s.  Maybe you should try running 'list states" % instance)

# Always run local to the run.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))

parser = OptionParser(usage="usage: %prog [options] filename",
                      version="%prog 1.0")

parser.add_option("-c", "--config",
                  action="store",
                  dest="config",
                  default="settings.ini",
                  help="Path to the settings file",)
(options, args) = parser.parse_args()

configfile = options.config
config = ConfigParser.ConfigParser()
config.read(configfile)

# Set up Nova client api
section             = 'OpenStack Configuration'
ost_version         = config.get(section, 'version')
ost_username        = config.get(section, 'username')
ost_password        = config.get(section, 'password')
ost_project_name    = config.get(section, 'project_name')
ost_auth_url        = config.get(section, 'auth_url')
ost_insecure        = config.get(section, 'insecure')

nova = OST(version=ost_version, username=ost_username, password=ost_password, project_name=ost_project_name,
           auth_url=ost_auth_url, insecure=ost_insecure)

# Set up Slack client api
section         = 'Slack Configuration'
slack_api_token = config.get(section, 'api_token')
with open('slackbot_settings.py', 'w') as f:
    f.write("API_TOKEN = '%s' \n"
            "DEFAULT_REPLY = 'I did not understand that.  For help you can say, Help' \n"
            "PLUGINS = []"
            % slack_api_token)

# This import has to happen after the settings file exists.
# That's just the way this module works.
from slackbot.bot import Bot
bot = Bot()
bot.run()