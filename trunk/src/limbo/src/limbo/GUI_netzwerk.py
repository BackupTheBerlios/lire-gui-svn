#coding:utf-8
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
# GUI_netzwerk.py
# NETWORK GUI
"""GUI_netzwerk - POPUP for network data"""


###########
# imports #
###########
import yui
import re
import GUI_warning_popup

######################
# class GUI_netzwerk #
######################
class GUI_netzwerk(object):
    """GUI_netzwerk(myFactory, myParent, myStateDict, myConfigDict), returns stateDict, configDict
    
    @param myFactory: widgetFactory to use
    @type myFactory: Instance of widgetFactory
    @param myParent: parent widget
    @type myParent: Instance of YDialog 
    @param myStateDict: stateDict
    @type myStateDict: Dictionary
    @param myConfigDict: configDict
    @type myConfigDict: Dictionary
    @return: stateDict, configDict
    @rtype: Dictionary, Dictionary
    """
    def __init__(self, myFactory, myParent, myStateDict, myConfigDict):
        """__init__ for GUI_netzwerk
        """
        #############
        # variables #
        #############
        self.factory = myFactory
        self.parent = myParent
        self.stateDict = myStateDict
        self.configDictOrig = myConfigDict.copy()
        self.configDict = myConfigDict.copy()
        self.msgWarningIP = u"Bitte geben Sie eine gültige\nIPv4-Adresse ein!\n(z.B. 192.168.1.2)".encode("utf-8")
        self.msgWarningNetmask = u"Bitte geben Sie eine gültige\nIPv4-Netzmaske ein!\n(z.B. 255.255.255.0)".encode("utf-8")
        self.msgWarningDefaultRoute = u"Bitte geben Sie eine gültige\nIPv4-Standardroute ein!\n(z.B. 192.168.1.1)".encode("utf-8")
        self.msgWarningHostname = u"Bitte geben Sie einen gültigen\nHostnamen ein!\n(z.B. spb132)".encode("utf-8")

        #######
        # GUI #
        #######
        #
        # set parent for destruction of gui 
        self.networkDialog = self.factory.createPopupDialog()
        if self.parent:
            self.networkDialog.setParent(self.parent)
        #
        # VBox
        self.netVBox = self.factory.createVBox(self.networkDialog)
        self.netVBox.setStretchable( 0, True )
        self.netVBox.setStretchable( 1, True )
        #
        # "net_input_ip"
        self.netInputIP = self.factory.createInputField(self.netVBox, "IP")
        self.netInputIP.setValidChars("1234567890.DHCP")
        self.netInputIP.setInputMaxLength(15)
        self.netInputIP.setStretchable( 0, True )
        if self.configDict["net_input_ip"]=="DHCP":
            self.netInputIP.setDisabled()
        #
        # "net_input_netmask"
        self.netInputNetmask = self.factory.createInputField(self.netVBox, "Netzmaske")
        self.netInputNetmask.setValidChars("1234567890.")
        self.netInputNetmask.setInputMaxLength(15)
        self.netInputNetmask.setStretchable( 0, True )
        if self.configDict["net_input_ip"]=="DHCP":
            self.netInputNetmask.setDisabled()
        #
        # "net_input_defaultroute"
        self.netInputDefaultRoute = self.factory.createInputField(self.netVBox, "Standardroute")
        self.netInputDefaultRoute.setValidChars("1234567890.")
        self.netInputDefaultRoute.setInputMaxLength(15)
        self.netInputDefaultRoute.setStretchable( 0, True )
        if self.configDict["net_input_ip"]=="DHCP":
            self.netInputDefaultRoute.setDisabled()
        #
        # "net_input_hostname"
        self.netInputHostname = self.factory.createInputField(self.netVBox, "Hostname")
        self.netInputHostname.setValidChars("abcdefghijklmnopqrstuvwxyz1234567890.")
        self.netInputHostname.setStretchable( 0, True )
        #
        #
        self.netDHCPHBox = self.factory.createHBox(self.netVBox)
        self.netDHCP = self.factory.createCheckBox(self.netDHCPHBox, "DHCP aktivieren")
        self.netDHCP.setNotify()
        if self.configDict["net_input_ip"]=="DHCP":
            self.netDHCP.setChecked()
        #
        # Buttons down
        self.netBottomHBox = self.factory.createHBox(self.netVBox)
        self.netButtonCancel = self.factory.createPushButton(self.netBottomHBox, "Abbruch")
        self.netButtonNext = self.factory.createPushButton(self.netBottomHBox, "Weiter")
        self.netButtonNext.setDefaultButton(1)
        #
        # empty event
        self.event = None
        #
        # call update to fill in defaults/current values
        self.update()
        
    def checkIpString(self, inputstring):
        """Check for valid IP
        """
        #
        #regexp taken from regexp-database: URL = http://
        regexp = r"(?:^|\s)([a-z]{3,6}(?=://))?(://)?((?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?))(?::(\d{2,5}))?(?:\s|$)"
        if re.match(regexp, inputstring):
            return True  #good ip
        else:
            return False #bad ip
     
    def checkInput(self):
        """Check for valid input
        """
        inputOK = False
        #
        # check net_input_hostname
        hostname = self.netInputHostname.value()
        if not hostname.isalnum():
            WARNING_IP_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.networkDialog.this, self.msgWarningHostname)
            WARNING_IP_GUI.handleEvent()
            inputOK = False
            return inputOK
        else:
            self.configDict["net_input_hostname"] = hostname
            inputOK = True
        #
        # if DHCP don't check other values
        if self.netDHCP.isChecked():
            self.configDict["net_input_ip"]="DHCP"
            return inputOK
        #
        # check net_input_ip
        ip = self.netInputIP.value()
        if not self.checkIpString(ip):
            WARNING_IP_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.networkDialog.this, self.msgWarningIP)
            WARNING_IP_GUI.handleEvent()
            inputOK = False
            return inputOK
        else:
            self.configDict["net_input_ip"] = ip
            inputOK = True
        #
        # check net_input_netmask
        netmask = self.netInputNetmask.value()
        if not self.checkIpString(netmask):
            WARNING_IP_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.networkDialog.this, self.msgWarningNetmask)
            WARNING_IP_GUI.handleEvent()
            inputOK = False
            return inputOK
        else:
            self.configDict["net_input_netmask"] = netmask
            inputOK = True
        #
        # check net_input_defaultroute
        defaultroute = self.netInputDefaultRoute.value()
        if not self.checkIpString(defaultroute):
            WARNING_IP_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.networkDialog.this, self.msgWarningDefaultRoute)
            WARNING_IP_GUI.handleEvent()
            inputOK = False
            return inputOK
        else:
            inputOK = True
        #
        # check if ip == defaultroute
        if ip == defaultroute:
            WARNING_IP_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.networkDialog.this, "IP und Standardroute gleich!")
            WARNING_IP_GUI.handleEvent()
            inputOK = False
            return inputOK
        else:
            self.configDict["net_input_defaultroute"] = defaultroute
            inputOK = True
        return inputOK

    def update(self):
        """update InputFiels from configDict
        """
        #
        # check for "net_input_hostname"
        if self.configDict.has_key("net_input_hostname"):
            self.netInputHostname.setValue(str(self.configDict["net_input_hostname"]))
        else:
            self.netInputHostname.setValue("spb11") # set if no default
        #
        # if DHCP -> we're done
        if self.netDHCP.isChecked():
            return
        #
        # check for "net_input_ip"
        if self.configDict.has_key("net_input_ip"):
            self.netInputIP.setValue(str(self.configDict["net_input_ip"]))
        else:
            self.netInputIP.setValue("192.168.1.2") # set if no default
        #
        # check for "net_input_netmask"
        if self.configDict.has_key("net_input_netmask"):
            self.netInputNetmask.setValue(str(self.configDict["net_input_netmask"]))
        else:
            self.netInputNetmask.setValue("255.255.255.0") # set if no default
        #
        # check for "net_input_defaultroute"
        if self.configDict.has_key("net_input_defaultroute"):
            self.netInputDefaultRoute.setValue(str(self.configDict["net_input_defaultroute"]))
        else:
            self.netInputDefaultRoute.setValue("192.168.1.1") # set if no default
        
    def handleEvent(self):
        """ Main event loop
        """
        while True:
            #
            # get event
            self.event = self.networkDialog.waitForEvent()
            if not self.event:
                continue
            #
            # window got destroyed "x"
            if self.event.eventType() == yui.YEvent.CancelEvent:
                if self.parent: # we have a parent - just return saving old values
                    self.networkDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    self.networkDialog.destroy() # just destroy all
                    break
            #
            # "Abbruch" clicked
            if self.event.widget() == self.netButtonCancel:
                if self.parent:
                    self.networkDialog.deleteTopmostDialog() # we have parent
                    return self.stateDict, self.configDictOrig
                else:
                    self.networkDialog.destroy() # just destroy
                    break
            if self.event.widget() == self.netDHCP:
                if self.netDHCP.isChecked():
                    #deactivate fields
                    self.netInputDefaultRoute.setDisabled()
                    self.netInputIP.setDisabled()
                    self.netInputNetmask.setDisabled()
                else:
                    #activate fields again
                    self.netInputDefaultRoute.setEnabled()
                    self.netInputIP.setEnabled()
                    self.netInputNetmask.setEnabled()
                    # check for "net_input_ip"
                    if self.configDict.has_key("net_input_ip"):
                        self.netInputIP.setValue(str(self.configDict["net_input_ip"]))
                    else:
                        self.netInputIP.setValue("192.168.1.2") # set if no default
                    #
                    # check for "net_input_netmask"
                    if self.configDict.has_key("net_input_netmask"):
                        self.netInputNetmask.setValue(str(self.configDict["net_input_netmask"]))
                    else:
                        self.netInputNetmask.setValue("255.255.255.0") # set if no default
                    #
                    # check for "net_input_defaultroute"
                    if self.configDict.has_key("net_input_defaultroute"):
                        self.netInputDefaultRoute.setValue(str(self.configDict["net_input_defaultroute"]))
                    else:
                        self.netInputDefaultRoute.setValue("192.168.1.1") # set if no default
            #
            # "Weiter" clicked
            if self.event.widget() == self.netButtonNext:
                if not self.checkInput(): # if check fails fill in sane default / last value
                    # need to inform the user
                    self.update()
                    continue
                else: # all green, go ahead
                    self.stateDict["NETZWERK_DONE"] = 1
                    self.stateDict["REPOSITORY"] = 1
                    if self.parent: # we have parent - go to it
                        self.networkDialog.deleteTopmostDialog()
                        return self.stateDict, self.configDict
                    else: # destroy all for standalone test
                        self.networkDialog.destroy()
                        return self.stateDict, self.configDict


if __name__ == "__main__":
    """Standalone test
    """
    import locale
    locale.setlocale(locale.LC_ALL, "")

    factory = yui.YUI.widgetFactory()
    statedict = {}
    statedict["START"] = 1
    statedict["NETZWERK"] = 1
    statedict["NETZWERK_DONE"] = 0
    configdict = {}
    configdict["net_input_ip"] = "192.168.1.3"
    
    
    MY_NETWORK_GUI = GUI_netzwerk(factory, None, statedict, configdict)
    statedict, configdict = MY_NETWORK_GUI.handleEvent()
    import pprint 
    print "statedict"
    print "#########"
    pprint.pprint(statedict)
    print
    print "configdict"
    print "##########"
    pprint.pprint(configdict)
                  