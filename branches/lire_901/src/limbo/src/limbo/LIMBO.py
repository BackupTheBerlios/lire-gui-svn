# -*- coding: utf-8 -*-
#
# (c) 2008 Jan-Simon Möller
# (c) 2008 Leibniz Universität Hannover
# Released under the GPLv2.
# 
# #############################
# #                           #
# #  L   I m   B   O          #
# #  ire  |    y   |          #
# #      aging     BS         #
# #                           #
# #                           #
# #############################
#
#===============================================================================
# Copyright (C) [2008]  Jan-Simon Möller
#           (C) [2008]  Leibniz Universität Hannover 
# This program is free software; you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation; either version 2 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
# for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, see <http://www.gnu.org/licenses/>. 
#===============================================================================
#
# LIMBO.py
# START THE PROGRAM
"""Application startup and initial configuration"""
###########
# imports #
###########
import yui               # libyui
import GUI_main          # main gui
import locale            # locale support (mainly console)
import os                # filesystem
import sys               # error messages
import CORE_settings     # config file
import GUI_warning_popup # error popup
from optparse import OptionParser # cmdline options
import shutil            # file operations

###########
# CMDLINE #
###########
# evaluate the cmdline arguments
# TODO:
# Evaluate cmdline-options
# --clear forget settings

parser = OptionParser()
parser.add_option("-C", "--clear", help="Loeschen aller persoenlichen Einstellungen", action="store_true", dest="clear")
parser.add_option("-b", "--backup", help="Backup aller persoenlichen Einstellungen", action="store_true", dest="backup")
parser.add_option("-r", "--restore", help="Wiederherstellung aller persoenlichen Einstellungen", action="store_true", dest="restore")
parser.add_option("-c", "--cleanup", help="Aufraumen des Ausgabeordners", action="store_true", dest="cleanup")

#
# parse args
(options, args) = parser.parse_args()

#
# execute args
if options.restore:
    src=os.path.join(os.path.expanduser("~/.limbo_backup"))
    dst=os.path.join(os.path.expanduser("~/.limbo"))
    # remove destination
    if os.path.exists(src):
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(src, dst)
        print "Ordner wiederhergestellt!\n"
    else:
        print "Kein Backupordner vorhanden!\n"
    sys.exit(0)
if options.backup:
    dst=os.path.join(os.path.expanduser("~/.limbo_backup"))
    src=os.path.join(os.path.expanduser("~/.limbo"))
    # remove destination
    if os.path.exists(src):
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(src, dst)
        print "Ordner gesichert!\n"
    else:
        print "Kein Ordner zu sichern!\n"
    sys.exit(0)
if options.clear:
    dst=os.path.join(os.path.expanduser("~/.limbo"))
    # remove destination
    shutil.rmtree(dst, ignore_errors=True)
    print "Einstellungen geloescht\n"
    sys.exit(0)

    # cleanup needs to know the folder - its after settings !

#
# create settings-dir
if not os.path.exists(os.path.expanduser("~/.limbo")):
    os.makedirs(os.path.expanduser("~/.limbo"))


####################################
# LOCALE (important for TERMINAL!) #
####################################
#
# set the locale to de/utf-8
locale.setlocale(locale.LC_ALL, "")
log = yui.YUILog.instance()
log.setLogFileName(os.path.expanduser("~/.limbo/debug.log"))
log.enableDebugLogging( True )
appl = yui.YUI.application()
appl.setLanguage( "de_DE", "" )
# relevant for the correct drawing when executed through winssh !!
#
# appl.setConsoleFont(magic, font, screenMap, unicodeMap, language)
# see /usr/share/YaST2/data/consolefonts.ycp
#===============================================================================
#      // LANG           font                unicode map screen map,     console magic
#      "de_DE@euro"      : [ "lat9w-16.psfu",    "",     "trivial",      "(B" ],
#      "de_DE"           : [ "lat1-16.psfu",     "",     "none",         "(B" ],
#      "de_CH"           : [ "lat1-16.psfu",     "",     "none",         "(B" ],
#      "de"              : [ "lat1-16.psfu",     "",     "none",         "(B" ],
#      "de_DE.UTF-8"     : [ "lat9w-16.psfu",    "",     "trivial",      "(K" ],
#      "de_CH.UTF-8"     : [ "lat9w-16.psfu",    "",     "trivial",      "(K" ],
#      "de_AT.UTF-8"     : [ "lat9w-16.psfu",    "",     "trivial",      "(K" ],
#===============================================================================
appl.setConsoleFont("(B", "lat9w-16.psfu", "trivial", "", "de_DE@euro")


############
# SETTINGS #
############
# Create Settings-DIR, if not available
# Load Settings, if available
#
#
# create configfile and default sections
configFile = os.path.expanduser("~/.limbo/config") # starting config/last used config
mySettings = CORE_settings.CORE_settings(configFile)

# old: mySettings.limboDefaults()
#
# configdict  access: configDict["nameOfValue"]
configDict = {}
configDict["profiles"] = {} # available profiles
configDict["required"] = [] # variables present before GO
configDict["defaultlist"] = [] # list of default variables
configDict["defaultinstalledsoft"] = [] # mandatory software
configDict["lire_target"] = {} # lire.conf options
configDict["outputtype"] = []

#
# import defaults and profiles into configDict
configDict = mySettings.limboConfigDict(configDict.copy())
#

#
# last cmdline option - need to know configDict["output_dir"] 
if options.cleanup:
    dst=os.path.join(os.path.expanduser(configDict["output_dir"]))
    # remove destination
    shutil.rmtree(dst, ignore_errors=True)
    print "Ausgabeordner geloescht\n"
    sys.exit(0)


#########
# STATE #
#########
# STATUS, ACTIONS TO DO DURING GUI -> CONFIG READY FOR EXECUTION 
# (WIZARD, CHECK FOR OTHERS)
stateDict = {}
stateDict["START"]          = 0
stateDict["NETZWERK"]       = 0
stateDict["NETZWERK_DONE"]  = 0
stateDict["REPOSITORY"]     = 0
stateDict["REPOSITORY_DONE"]= 0
stateDict["SOFTWARE"]       = 0
stateDict["SOFTWARE_DONE"]  = 0
stateDict["XENOMAI"]        = 0
stateDict["XENOMAI_DONE"]   = 0
stateDict["ERWEITERT"]      = 0
stateDict["ERWEITERT_DONE"] = 0
stateDict["DIENSTE"]        = 0
stateDict["DIENSTE_DONE"]   = 0
stateDict["READY"]          = 0


############
# GUI_main #
############
#
# big parachute - to debug/catch errors
try:
    #
    # create widget-factory
    factory = yui.YUI.widgetFactory()
    #
    # all set, start main gui
    myGuiMain = GUI_main.GUI_main(factory, stateDict, configDict)
    #
    # start the big loop
    configDict, cmdmsg = myGuiMain.handleEvent()
    #del configDict['softwareDict']
    #pprint.pprint(configDict)
    #del factory
    if not cmdmsg is None:
        # print cmds to konsole (e.g. hints for kiwi local exec)
        print cmdmsg
except:
    e = str(sys.exc_info()) #[1])+str(" "+)
    msg = "Kritischer Fehler:\n "+str(e)+"\nProgramm wird beendet".encode("utf-8")+"\n"
    #
    # error popup 
    WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(factory, None, msg)
    WARNING_URL_GUI.handleEvent()


#================= c o n f i g D i c t =========================================
# {'api_url': 'http://192.168.10.246/',
# 'defaultinstalledsoft': ['busybox',
#                          'grub',
#                          'lire-devs',
#                          'libdc1394',
#                          'busybox-linuxrc',
#                          'libpng12-0',
#                          'nano',
#                          'libraw1394',
#                          'openssh',
#                          'glibc',
#                          'opencv',
#                          'openvpn',
#                          'xenomai',
#                          'kernel-xenomai',
#                          'lire-tweak-dependencies'],
# 'defaultlist': ['net_input_ip',
#                 'repo_input_checkbox_3',
#                 'repo_input_checkbox_2',
#                 'api_url'],
# 'lastprofile': 'jsm',
# 'lire_target': {'cat_dienste': 'config_lire_target_',
#                 'cat_erweitert': 'atmel,madwifi',
#                 'cat_xenomai': 'rtnet,rack',
#                 'config_lire_atmel_prereq': '',
#                 'config_lire_atmel_target_channel': '11',
#                 'config_lire_atmel_target_device_name': 'wlan0',
#                 'config_lire_atmel_target_driver_wait': '3',
#                 'config_lire_atmel_target_ipaddr': 'DHCP',
#                 'config_lire_atmel_target_key': '1234123412',
#                 'config_lire_atmel_target_mode': 'ad-hoc',
#                 'config_lire_atmel_target_ssid': 'SPBnet',
#                 'config_lire_atmel_target_start': 'None',
#                 'config_lire_madwifi_prereq': '',
#                 'config_lire_madwifi_target_channel': '11',
#                 'config_lire_madwifi_target_device_name': 'ath0',
#                 'config_lire_madwifi_target_driver_wait': '1',
#                 'config_lire_madwifi_target_ipaddr': 'DHCP',
#                 'config_lire_madwifi_target_key': '1234123412',
#                 'config_lire_madwifi_target_mode': 'ad-hoc',
#                 'config_lire_madwifi_target_ssid': 'SPBnet',
#                 'config_lire_madwifi_target_start': 'None',
#                 'config_lire_prereq': '',
#                 'config_lire_rack_prereq': '',
#                 'config_lire_rack_target_tims_client_log_level': '0',
#                 'config_lire_rack_target_tims_client_router_ip': '127.0.0.1',
#                 'config_lire_rack_target_tims_client_router_port': '2000',
#                 'config_lire_rack_target_tims_client_start': 'y',
#                 'config_lire_rack_target_tims_clock_sync_can_id': '0',
#                 'config_lire_rack_target_tims_clock_sync_dev': '',
#                 'config_lire_rack_target_tims_clock_sync_mode': '0',
#                 'config_lire_rack_target_tims_driver_log_level': '2',
#                 'config_lire_rack_target_tims_msg_size': '8192',
#                 'config_lire_rack_target_tims_msg_slots': '2',
#                 'config_lire_rack_target_tims_router_listen_ip': '',
#                 'config_lire_rack_target_tims_router_log_level': '0',
#                 'config_lire_rack_target_tims_router_port': '2000',
#                 'config_lire_rack_target_tims_router_start': 'y',
#                 'config_lire_rack_target_tims_rtnet_config': '',
#                 'config_lire_rtnet_prereq': '',
#                 'config_lire_rtnet_target_autostart': 'None',
#                 'config_lire_rtnet_target_driver': 'rt_eepro100',
#                 'config_lire_rtnet_target_ip': '10.0.0.1',
#                 'config_lire_rtnet_target_normal_net': 'y',
#                 'config_lire_rtnet_target_routing': 'y',
#                 'config_lire_rtnet_target_slaves': '10.0.0.2',
#                 'config_lire_rtnet_target_tdma_mode_master': 'y',
#                 'config_lire_rtnet_target_tdma_mode_slave': 'None',
#                 'config_lire_target_dev_on_tmpfs': 'y',
#                 'config_lire_target_eth_drivers': 'e100',
#                 'config_lire_target_hostname': 'SPB_GENERIC',
#                 'config_lire_target_init_ethernet': 'y',
#                 'config_lire_target_keymap': 'DE',
#                 'config_lire_target_launch_httpd': 'y',
#                 'config_lire_target_launch_syslogd': 'y',
#                 'config_lire_target_main_ip': 'DHCP',
#                 'config_lire_target_nr_halt_beeps': '2',
#                 'config_lire_target_nr_ready_beeps': '1',
#                 'config_lire_target_remount_root_rw': 'None',
#                 'config_lire_target_run_spb_pack_manager': 'y',
#                 'config_lire_target_syslogconsole': '10',
#                 'config_lire_target_tmpfs_dirs': '/var/log;/var/lock;/etc/dhcpc;/tmp',
#                 'config_lire_target_tmpfs_support': 'y'},
# 'net_input_defaultroute': '192.168.1.1',
# 'net_input_hostname': 'spb11',
# 'net_input_ip': '192.168.1.5',
# 'net_input_netmask': '255.255.255.0',
# 'output_dir': '/home/dl9pf/lire_out',
# 'outputtype': ['ext3', 'iso9660', 'vmdk', 'pxe', 'ext2'],
# 'profile': 'jsm',
# 'profiles': {'standard': 'Standard'},
# 'repo_active': [1, 2, 3],
# 'repo_input_alias_1': 'beispiel',
# 'repo_input_alias_2': 'beispiel2',
# 'repo_input_alias_3': 'beispiel3',
# 'repo_input_checkbox_1': True,
# 'repo_input_checkbox_2': True,
# 'repo_input_checkbox_3': True,
# 'repo_input_url_1': 'http://192.168.10.247/lire/base_toolchain/',
# 'repo_input_url_2': 'http://192.168.10.247/lire_own/standard/',
# 'repo_input_url_3': 'http://192.168.10.247/base_toolchain/standard/',
# 'required': ['net_input_ip',
#              'net_input_hostname',
#              'soft_to_install',
#              'output_dir',
#              'net_input_defaultroute',
#              'net_input_netmask'],
# 'soft_to_install': set(['busybox', 'grub', 'libpng12-0', 'libraw1394', 'openssh', 'glibc', 'libdc1394', 'opencv', 'busybox-linuxrc', 'openvpn', 'xenomai', 'kernel-xenomai', 'lire-tweak-dependencies', 'lire-devs', 'nano']),
# 'templatedesc': ''}
#===============================================================================




#################
# SAVE SETTINGS #
#################
#
# save profile-names
if configDict is not None: # cancel !
    for i,j in configDict["profiles"].iteritems():
        mySettings.set("profiles",i,j)
    del configDict["profiles"]
#    #
#    # save defaults
#    list = set(configDict["defaultlist"])
#    for  i in list:
#        mySettings.set("mydefault",i, configDict[i])
#        #print i," ",configDict[i]
#        del configDict[i]
    del configDict["defaultlist"]
    #
#    # save required
#    for i in set(configDict["required"]):
#        mySettings.set("required",i, 1)
    del configDict["required"]
    #
    # save lastprofile
    if configDict.has_key("lastprofile"):
        mySettings.set("lastprofile", "lastprofile", configDict["lastprofile"])
    #
    # write do disk
#    for i in set(configDict["lire_target"].keys()):
#        mySettings.set("lire_target", i, configDict["lire_target"][i])
#        del configDict["lire_target"][i]
#    del configDict["lire_target"]
    mySettings.sync()
    
########
# EXIT #
########