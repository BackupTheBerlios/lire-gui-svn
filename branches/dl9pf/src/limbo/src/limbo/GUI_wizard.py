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
# GUI_wizard.py
# Wizard GUI
"""GUI_wizard - popup window for wizard"""


###########
# imports #
###########
import yui
import re
import GUI_warning_popup
import sys

######################
# class GUI_netzwerk #
######################
class GUI_wizard(object):
    """GUI_wizard(myFactory, myParent, myStateDict, myConfigDict), returns True/False
    
    GUI_wizard - popup window for wizard
    
    @param myFactory: widgetFactory to use
    @type myFactory: Instance of widgetFactory
    @param myParent: parent widget
    @type myParent: Instance of YDialog 
    @param myStateDict: stateDict
    @type myStateDict: Dictionary
    @param myConfigDict: configDict
    @type myConfigDict: Dictionary
    
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
        self.configDict = myConfigDict.copy()
        self.profileName = None
        self.profileDesc = None
        self.error = False

        #######
        # GUI #
        #######
        #
        # set parent for destruction of gui 
        self.wizardDialog = self.factory.createPopupDialog()
        if self.parent:
            self.wizardDialog.setParent(self.parent)
        #
        # VBox
        self.wizardVBox = self.factory.createVBox(self.wizardDialog)
        self.wizardVBox.setStretchable( 0, True )
        self.wizardVBox.setStretchable( 1, True )
        #
        # label
        #self.wizardLabel = self.factory.createLabel(self.wizardVBox, "Geben Sie einen Profilnamen und\neine kurze Beschreibung an.")
        self.wizardLabel = self.factory.createLabel(self.wizardVBox, "Geben Sie einen Profilnamen an.") 
        #
        # 2 input fields
        self.wizardProfileName = self.factory.createInputField(self.wizardVBox, "Name")
        #self.wizardProfileDesc = self.factory.createInputField(self.wizardVBox, "Kurzbeschreibung")
        #
        # Buttons
        self.bottomHBox = self.factory.createHBox(self.wizardVBox)
        self.wizardButtonCancel = self.factory.createPushButton(self.bottomHBox, u"Zurück".encode("utf-8"))
        #self.wizardButtonCheck = self.factory.createPushButton(self.bottomHBox, u"Prüfen".encode("utf-8"))
        self.wizardButtonWrite = self.factory.createPushButton(self.bottomHBox, "Speichern")
        #
        # empty event
        self.event = None
        
    def checkProfileName(self):
        """Check for valid ProfileName
        """
        self.profileName = self.wizardProfileName.value()
        #
        #regexp taken from regexp-database: URL = http://
        #regexp = r"(?:^|\s)([a-z]{3,6}(?=://))?(://)?((?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?))(?::(\d{2,5}))?(?:\s|$)"
        #if re.match(regexp, inputstring):
        #    return True  #good ip
        #else:
        #    return False #bad ip
     
    def checkProfileDescription(self):
        self.profileDesc = self.wizardProfileDesc.value()


    def handleEvent(self):
        """ Main event loop
        """
        while True:
            #
            # get event
            self.event = self.wizardDialog.waitForEvent()
            if not self.event:
                continue
            #
            # window got destroyed "x"
            if self.event.eventType() == yui.YEvent.CancelEvent:
                if self.parent: # we have a parent - just return saving old values
                    self.wizardDialog.deleteTopmostDialog()
                    return (None, None, True)
                else:
                    self.wizardDialog.destroy() # just destroy all
                    break
            #
            # "Abbruch" clicked
            if self.event.widget() == self.wizardButtonCancel:
                if self.parent:
                    self.wizardDialog.deleteTopmostDialog() # we have parent
                    return (None, None, True)
                #self.stateDict, self.configDictOrig
                else:
                    self.wizardDialog.destroy() # just destroy
                    break
            #
            # "Check"
            #if self.event.widget() == self.wizardButtonCheck:
            #    self.checkProfileDescription()
            #    self.checkProfileName()
            #
            # "Save"
            if self.event.widget() == self.wizardButtonWrite:
                #self.checkProfileDescription()
                # empty for now
                self.profileDesc=""
                self.checkProfileName()
                if not self.error:
                    if self.parent:
                        self.wizardDialog.deleteTopmostDialog() # we have parent
                        return (self.profileName, self.profileDesc, self.error) 
                    else:
                        self.wizardDialog.destroy() # just destroy
                        break
                else:
                    if self.parent:
                        self.wizardDialog.deleteTopmostDialog() # we have parent
                        return (None, None, True)
                    #self.stateDict, self.configDictOrig
                    else:
                        self.wizardDialog.destroy() # just destroy
                        break


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
    
    
    MY_NETWORK_GUI = GUI_wizard(factory, None, statedict, configdict)
    statedict, configdict = MY_NETWORK_GUI.handleEvent()
    
    print "statedict"
    print "#########"
    print statedict
    print
    print "configdict"
    print "##########"
    print configdict
                  