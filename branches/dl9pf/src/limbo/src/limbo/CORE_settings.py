# coding=utf-8
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
"""CORE_settings

This is the CORE_setting class of LImBO.
     L   I m   B   O           
     ire  |    y   |           
         aging     BS          


        Handle the Settings
        Subclasses ConfigParser
"""
from ConfigParser import ConfigParser


class CORE_settings(ConfigParser):
    def __init__(self, filename):
        """
        Handle the Settings
        Subclasses ConfigParser
        extends with  sync()
        mySettings = Settings('/tmp/configfile.test2')
        mySettings.read(mySettings.filename)
        for section in mySettings.sections():
            print section
            for option in mySettings.options(section):
                print " ", option, "=", mySettings.get(section, option)
        if not mySettings.has_section("test"):
            mySettings.add_section("test")
        if not mySettings.has_option("test", "testoption"):
            mySettings.set("test", "testoption" , "testvalue")
        mySettings.sync()
        @param filename: full path to the configfile
        @type filename: String
        """
        ConfigParser.__init__(self, None)
        self.filename = filename
        self.read(filename)
    
    def checkset(self, section, option, value):
        """Simple check and set if not available
        @param section: section
        @type section: String
        @param option: option
        @type option: String
        @param value: value
        @type value: String

        """
        #
        # check, insert if not available
        if not self.has_section(section):
            self.add_section(section)
        if not self.has_option(section, option):
            self.set(section, option, value)

    
    def sync(self):
        """Write config to disk
        """
        fd = open(self.filename, 'w')
        self.write(fd)
        fd.close()

    def limboDefaults(self):
        """load some default values, only if empty
        """
        #
        # default (some basic settings and predefined inputs 
        # - set to default if not available)
        #self.checkset("default", "lastprofile" , "lire")
        self.checkset("mydefault", "net_input_ip", "130.75.137.200")
        self.checkset("mydefault", "api_url", "http://lire-api.rts.uni-hannover.de/")
        self.checkset("mydefault", "description", "default settings to start the program")
        self.checkset("mydefault", "repo_input_checkbox_2", "1")
        self.checkset("mydefault", "repo_input_checkbox_3", "1")
        # later: for i in repo_active : repo_input_url_$i  repo_input_alias_$i !
        self.checkset("mydefault", "repo_input_url_1", "http://lire-repo.rts.uni-hannover.de/base_toolchain/standard/")
        self.checkset("mydefault", "repo_input_alias_1", "base_toolchain")
        self.checkset("mydefault", "repo_input_url_2", "http://lire-repo.rts.uni-hannover.de/lire/base_toolchain/")
        self.checkset("mydefault", "repo_input_alias_2", "lire")
        self.checkset("mydefault", "repo_input_url_3", "http://lire-repo.rts.uni-hannover.de/lire_own/standard/")
        self.checkset("mydefault", "repo_input_alias_3", "lire_own")
        #
        # output types
        self.checkset("outputtype", "description", "available output targets")
        self.checkset("outputtype", "ext2", "1")
        self.checkset("outputtype", "ext3", "1")
        self.checkset("outputtype", "vmdk", "0")
        self.checkset("outputtype", "iso9660", "0")
        self.checkset("outputtype", "pxe", "0")
        #
        # profiles 
        self.checkset("profiles", "description" , "List of available/detected profiles. <nickname> = <description>")
        self.checkset("profiles", "standard" , "Standard")
        #
        # lastprofile
        self.checkset("lastprofile", "description" , "last used profile")
        self.checkset("lastprofile", "lastprofile" , "Standard")

        #self.checkset("profiles", "lire_exp" , "LiRE_exp")
        #
        # required (for completeness-check)
        #
        # configuration items which need to be set
        self.checkset("required", "description", "These variables need to be present before imaging can start. 1 = set, 0 = ignored")
        self.checkset("required", "net_input_ip", "1")
        self.checkset("required", "net_input_hostname", "1")
        self.checkset("required", "net_input_netmask", "1")
        self.checkset("required", "net_input_defaultroute", "1")
        self.checkset("required", "soft_to_install", "1")
        self.checkset("required", "repo_active", "1, 2, 3")
        self.checkset("required", "output_dir", "1")
        self.checkset("required", "repo_input_checkbox_2", "1")
        self.checkset("required", "repo_input_checkbox_3", "1")
        #self.checkset("required", "", "1")
        #
        # software predefined for installation as base for profiles and others   
        #
        # software items which need to be installed / template for new profiles
        self.checkset("defaultinstalledsoft", "description", "Software items which are always needed. 1 = set, 0 = ignored")
        self.checkset("defaultinstalledsoft", "busybox-linuxrc", "1")
        self.checkset("defaultinstalledsoft", "kernel-xenomai", "1")
        self.checkset("defaultinstalledsoft", "xenomai", "1")
        self.checkset("defaultinstalledsoft", "openvpn", "1")
        self.checkset("defaultinstalledsoft", "openssh", "1")
        self.checkset("defaultinstalledsoft", "grub", "1")
        self.checkset("defaultinstalledsoft", "libdc1394", "1")
        self.checkset("defaultinstalledsoft", "libraw1394", "1")
        self.checkset("defaultinstalledsoft", "libpng12-0", "1")
        self.checkset("defaultinstalledsoft", "nano", "1")
        self.checkset("defaultinstalledsoft", "opencv", "1")
        self.checkset("defaultinstalledsoft", "lire-tweak-dependencies", "1")
        self.checkset("defaultinstalledsoft", "lire-runtime", "1")
        self.checkset("defaultinstalledsoft", "busybox", "1")
        self.checkset("defaultinstalledsoft", "busybox", "1")
        self.checkset("defaultinstalledsoft", "glibc", "1")
        #self.checkset("defaultinstalledsoft", "selinux-tools", "1")
        self.checkset("defaultinstalledsoft", "lire-devs", "1")
        #
        # defautl items
        self.checkset("lire_target", "description", "Values for runtime-config")
        self.checkset("lire_target", "CONFIG_LIRE_LTP_PREREQ", "")
        self.checkset("lire_target", "CONFIG_LIRE_LTP_TARGET_LTP_START", "0")    
        self.checkset("lire_target", "CONFIG_LIRE_LTP_TARGET_LPT_TEST", "")
        self.checkset("lire_target", "CONFIG_LIRE_LTP_TARGET_LPT_RHOST", "")    
        self.checkset("lire_target", "CONFIG_LIRE_LTP_TARGET_LPT_PASSWORD", "")
        self.checkset("lire_target", "CONFIG_LIRE_ATMEL_PREREQ", "")    
        self.checkset("lire_target", "CONFIG_LIRE_ATMEL_TARGET_START", "None")
        self.checkset("lire_target", "CONFIG_LIRE_ATMEL_TARGET_DRIVER_WAIT", "3")
        self.checkset("lire_target", "CONFIG_LIRE_ATMEL_TARGET_DEVICE_NAME", "wlan0")
        self.checkset("lire_target", "CONFIG_LIRE_ATMEL_TARGET_IPADDR", "DHCP")
        self.checkset("lire_target", "CONFIG_LIRE_ATMEL_TARGET_SSID", "SPBnet")
        self.checkset("lire_target", "CONFIG_LIRE_ATMEL_TARGET_CHANNEL", "11")
        self.checkset("lire_target", "CONFIG_LIRE_ATMEL_TARGET_MODE", "ad-hoc")
        self.checkset("lire_target", "CONFIG_LIRE_ATMEL_TARGET_KEY", "1234123412")
        self.checkset("lire_target", "CONFIG_LIRE_MADWIFI_PREREQ", "")    
        self.checkset("lire_target", "CONFIG_LIRE_MADWIFI_TARGET_START", "None")
        self.checkset("lire_target", "CONFIG_LIRE_MADWIFI_TARGET_DRIVER_WAIT", "1")
        self.checkset("lire_target", "CONFIG_LIRE_MADWIFI_TARGET_DEVICE_NAME", "ath0")
        self.checkset("lire_target", "CONFIG_LIRE_MADWIFI_TARGET_IPADDR", "DHCP")
        self.checkset("lire_target", "CONFIG_LIRE_MADWIFI_TARGET_SSID", "SPBnet")
        self.checkset("lire_target", "CONFIG_LIRE_MADWIFI_TARGET_CHANNEL", "11")
        self.checkset("lire_target", "CONFIG_LIRE_MADWIFI_TARGET_MODE", "ad-hoc")
        self.checkset("lire_target", "CONFIG_LIRE_MADWIFI_TARGET_KEY", "1234123412")
        self.checkset("lire_target", "CONFIG_LIRE_RTNET_PREREQ", "")
        self.checkset("lire_target", "CONFIG_LIRE_RTNET_TARGET_AUTOSTART", "None")
        self.checkset("lire_target", "CONFIG_LIRE_RTNET_TARGET_DRIVER", "rt_eepro100")
        self.checkset("lire_target", "CONFIG_LIRE_RTNET_TARGET_IP", "10.0.0.1")
        self.checkset("lire_target", "CONFIG_LIRE_RTNET_TARGET_TDMA_MODE_MASTER", "y")
        self.checkset("lire_target", "CONFIG_LIRE_RTNET_TARGET_TDMA_MODE_SLAVE", "None")
        self.checkset("lire_target", "CONFIG_LIRE_RTNET_TARGET_SLAVES", "10.0.0.2")
        self.checkset("lire_target", "CONFIG_LIRE_RTNET_TARGET_SLAVES", "10.0.0.3")
        self.checkset("lire_target", "CONFIG_LIRE_RTNET_TARGET_NORMAL_NET", "y")
        self.checkset("lire_target", "CONFIG_LIRE_RTNET_TARGET_ROUTING", "y")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_PREREQ", "")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_RTNET_CONFIG", "")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_MSG_SIZE", "8192")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_MSG_SLOTS", "2")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_DRIVER_LOG_LEVEL", "2")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_CLOCK_SYNC_MODE", "0")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_CLOCK_SYNC_DEV", "")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_CLOCK_SYNC_CAN_ID", "0")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_CLIENT_START", "y")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_CLIENT_ROUTER_IP", "127.0.0.1")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_CLIENT_ROUTER_PORT", "2000")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_CLIENT_LOG_LEVEL", "0")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_ROUTER_START", "y")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_ROUTER_LISTEN_IP", "")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_ROUTER_PORT", "2000")
        self.checkset("lire_target", "CONFIG_LIRE_RACK_TARGET_TIMS_ROUTER_LOG_LEVEL", "0")
        self.checkset("lire_target", "CONFIG_LIRE_PREREQ", "")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_HOSTNAME", "SPB_GENERIC")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_INIT_ETHERNET", "y")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_MAIN_IP", "DHCP")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_ETH_DRIVERS", "e100")
        #self.checkset("lire_target", "CONFIG_LIRE_TARGET_ETH_DRIVERS", "8139too")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_KEYMAP", "DE")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_RUN_spb_pack_manager", "y")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_LAUNCH_HTTPD", "y")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_LAUNCH_SYSLOGD", "y")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_SYSLOGCONSOLE", "9")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_IMAGE_SIZE", "100")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_TMPFS_SUPPORT", "y")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_TMPFS_DIRS", "/var/log;/var/lock;/etc/dhcpc;/tmp")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_REMOUNT_ROOT_RW", "None")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_NR_READY_BEEPS", "1")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_NR_HALT_BEEPS", "2")
        self.checkset("lire_target", "CONFIG_LIRE_TARGET_DEV_ON_TMPFS", "y")
        self.checkset("lire_target", "CAT_XENOMAI", "rtnet,rack")
        self.checkset("lire_target", "CAT_ERWEITERT", "atmel,madwifi,ltp")
        self.checkset("lire_target", "CAT_DIENSTE", "config_lire_target_")
        self.sync()
        
    def limboConfigDict(self, configDict=None):
        """ return the current configDict 
        @param configDict: known configDict
        @type configDict: Dictionary
        @return: configDict
        @rtype: Dictionary

        """
        #configDict=None => return to defaults
        #print self.sections()
        if not self.sections():
            print "returning to defaults"
            configDict = {}
            configDict["profiles"] = {} # available profiles
            configDict["required"] = [] # variables present before GO
            configDict["defaultlist"] = [] # list of default variables
            configDict["defaultinstalledsoft"] = [] # mandatory software
            configDict["lire_target"] = {} # lire.conf options
            configDict["outputtype"] = [] # variables present before GO
            configDict["lastprofile"] = "Standard"
            self.limboDefaults()
            self.sync()

        #
        # import defaults and profiles into configDict
        for section in self.sections():
            for option in self.options(section):
                # filter out descriptions
                if option == "description":
                    continue
                #
                # import "default", list of imported in "defaultlist"
                if section == "mydefault":
                    configDict["defaultlist"].append(option)
                    configDict[option] = self.get(section, option)
                #
                # import profiles
                if section == "profiles":
                    configDict["profiles"][option] = self.get(section,option)
                #
                # import list of required variables
                if section == "required":
                    if self.get(section,option) == "1":
                        configDict["required"].append(option)
                #
                # import list of outputtype
                if section == "outputtype":
                    if self.get(section,option) == "1":
                        configDict["outputtype"].append(option)
                #
                # import list of mandantory packages
                if section == "defaultinstalledsoft":
                    if self.get(section,option) == "1":
                        configDict["defaultinstalledsoft"].append(option)
                #
                # import runtime settings
                if section == "lire_target":
                    configDict["lire_target"][str(option).lower()] =  self.get(section,option)
                #
                # import lastprofile
                if section == "lastprofile":
                    if self.get(section,option) == "1":
                        configDict["lastprofile"] = option
        return configDict
#------------------------------------------------------------------------------ 
if __name__ == "__main__":

    mySettings2 = CORE_settings('/tmp/configfile.test2')
    for section in mySettings2.sections():
        print section
        for option in mySettings2.options(section):
            print " ", option, "=", mySettings2.get(section, option)
    if not mySettings2.has_section("test"):
        mySettings2.add_section("test")
    if not mySettings2.has_option("test", "testoption"):
        mySettings2.set("test", "testoption" , "testvalue")
    mySettings2.sync()
    
    import pprint
    pprint.pprint(mySettings2.items("test"))
    
    mySettings2.limboDefaults()
    for section in mySettings2.sections():
        pprint.pprint(mySettings2.items(section))