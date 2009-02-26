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
# GUI_main.py
# Main GUI
"""GUI_main

This is the Main GUI class of LImBO.
     L   I m   B   O           
     ire  |    y   |           
         aging     BS          

In GUI_main all the libyui-stuff/GUI-stuff is extensively 
documented for reference.

Gui_main(myFactory, myStateDict, myConfigDict), returns configDict, msg
"""

###########
# Imports #
###########
import yui                              # UI
import os                               # os.path
import socket
import httplib                          # host alive check
import sys                              # error output
#
import CORE_template                    # core_template / profile
import GUI_wizard                       # profile/wizard
import GUI_warning_popup                # Warning
import GUI_netzwerk                     # NETWORK
import GUI_software2 as GUI_software    # SOFTWARE
import GUI_repository                   # REPO
import GUI_xenomai                      # Xenomai
import GUI_dienste                      # Dienste
import GUI_erweitert                    # Erweitert
import GUI_timeout_popup                # Timeout popup for transfer
#
import IMAGEROOT_write                  # lire.conf and possilby others
import KIWI_write                       # XML output
import KIWI_transfer                    # Transfer to/from OBS
import pprint

class GUI_main(object):
    """Gui_main(myFactory, myStateDict, myConfigDict), returns configDict, msg
    
    @param myFactory: widgetFactory to use
    @type myFactory: Instance of widgetFactory
    @param myStateDict: stateDict
    @type myStateDict: Dictionary
    @param myConfigDict: configDict
    @type myConfigDict: Dictionary
    
    """
    def __init__(self, myFactory, myStateDict, myConfigDict):
        """__init__"""
        #
        # Variables
        self.factory        = myFactory         #: link widgetFactory
        self.stateDict      = myStateDict       #: link stateDict
        self.configExpert   = False             #: Boolean for expert mode 
        self.configWizard   = False             #: Boolean for wizard mode
        self.configDict     = myConfigDict      #: link configDict
        self.configDictOrig = myConfigDict.copy() #: copy of configDict
        self.cmdmsg         = None              #: msg to print after program termination
        self.Template = CORE_template.CORE_template() #: initialize template
        self.profileList = self.Template.getTemplateList() #: get list of profiles
        self.canTransfer              = False #: API available ?
        self.uploaded                 = False # Already uploaded ?
        self.textLireStd              = "Standard"
        self.textLireSelboxStart      = "Start"
        self.textLireSelboxNetzwerk   = "Netzwerk"
        self.textLireSelboxRepository = "Repository"
        self.textLireSelboxSoftware   = "Software"
        self.textLireSelboxXenomai    = "Xenomai"
        self.textLireSelboxErweitert  = "Erweitert"
        self.textLireSelboxDienste    = "Dienste"
    #######
    # GUI #
    #######
        #
        #: Main GUI
        self.mainDialog         = self.factory.createMainDialog()
        #: vertical 
        self.mainVBox           = self.factory.createVBox(self.mainDialog)
        # -----------------
        #  |      |      |
        # -----------------
        #: horizontal alignment
        self.mainHBox           = self.factory.createHBox(self.mainVBox)
        #
        #-------------------
        # | selbox |      |
        #-------------------
        #: Selectionbox auf der linken Seite
        self.leftSelBox         = self.factory.createSelectionBox(self.mainHBox, u"Haupt&menü".encode("utf-8"))
        #: Generate event
        self.leftSelBox.setNotify()
        #: Layoutoption (horizontal, weighting)
        self.leftSelBox.setWeight(0,20)
        #: Layoutoption (vertikal, weighting)
        self.leftSelBox.setWeight(1,20)
        self.leftSelBox.addItem(self.textLireSelboxStart)
        self.leftSelBox.addItem(self.textLireSelboxNetzwerk)
        # 
        #--------------------
        # | selbox | right |
        #--------------------
        #: Frame on the right side
        self.right = self.factory.createVBox(self.mainHBox)
        #: Layoutoption (horizontal, weighting)
        self.right.setWeight(0,60)
        #: Layoutoption (vertikal, weighting)
        self.right.setWeight(1,100)
        #
        #: Input frame
        self.rightFrame         = self.factory.createFrame(self.right, "Eingaben")
        #: Layoutoption (horizontal, weighting)
        self.rightFrame.setWeight(0,100)
        #
        #: Frame for the base layout
        self.rightFrameVBox     = self.factory.createVBox(self.rightFrame)
        self.rightFrameHBox1 = self.factory.createHBox(self.rightFrameVBox)
        self.rightFrameHBox2 = self.factory.createHBox(self.rightFrameVBox)
        self.rightFrameHBox3 = self.factory.createHBox(self.rightFrameVBox)
        #
        #: Combobox for "Zielkonfiguration"
        self.rightComboBox      = self.factory.createComboBox(self.rightFrameHBox1, "&Zielkonfiguration")
        self.rightComboBox.addItem(self.textLireStd)
        #: Insert known Profiles
        self.updateProfileList()
        #: Layoutoption - horizontal expansible
        self.rightComboBox.setStretchable(0,True)
        #: Layoutoption (horizontal, weighting)
        self.rightComboBox.setWeight(0,70)
        #: Generate event
        self.rightComboBox.setNotify()
        #
        #: Combobox für Ausgabeformat 
        self.rightComboBoxOutput = self.factory.createComboBox(self.rightFrameHBox2, "&Ausgabeformat")
        #: Layoutoption - horizontal expansible
        self.rightComboBoxOutput.setStretchable(0,True)
        #: Layoutoption (horizontal, weighting)
        self.rightComboBoxOutput.setWeight(0,70)
        #: Generate event
        self.rightComboBoxOutput.setNotify()
        #: Einfügen der Ausgabeformate
        for i in self.configDict['outputtype']:
            self.rightComboBoxOutput.addItem(i)
        #: select ext2 as default
        self.rightComboBoxOutput.selectItem(self.rightComboBoxOutput.findItem("ext2"))
        #
        #: Inputfield for API-URL
        self.rightInputAPI = self.factory.createInputField(self.rightFrameHBox3, "API-URL")
        #: Check input
        self.rightInputAPI.setValidChars("1234567890.abcdefghijklmnopqrstuvwxyz:/_-@")
        #: Layoutoption (horizontal, weighting)
        self.rightInputAPI.setWeight(0,50)
        self.rightInputAPI.setValue(str(self.configDict["api_url"]))
        #
        #
        self.rightFrameVBox1 = self.factory.createVBox(self.rightFrameHBox1)
        #: Layoutoption (horizontal, weighting)
        self.rightFrameVBox1.setWeight(0,30)
        #
        #: Checkbox for "Erweiterten Modus"
        self.rightCheckExpert = self.factory.createCheckBox(self.rightFrameVBox1, "&Erweitert")
        #: Generate event
        self.rightCheckExpert.setNotify()
        #
        #: Frame
        self.rightFrameVBox2 = self.factory.createVBox(self.rightFrameHBox2)
        #: Layoutoption (horizontal, weighting)
        self.rightFrameVBox2.setWeight(0,30)
        #
        #: Checkbox for Wizard
        self.rightCheckWizard = self.factory.createCheckBox(self.rightFrameVBox2, "Wizar&d   ")
        #: Generate event
        self.rightCheckWizard.setNotify()
        #
        #: this should not happen
        if not self.configDict.has_key('output_dir'): 
            mypath = os.path.expanduser("~/lire_out")
            #: user-dir (default)
            self.configDict['output_dir'] = mypath
        else:
            mypath = self.configDict['output_dir']
        #
        #: Inputfield for API-URL
        self.rightInput = self.factory.createInputField(self.rightFrameHBox3, "&Ausgabeort")
        #: Layoutoption (horizontal, weighting)
        self.rightInput.setWeight(0,50)
        self.rightInput.setValue(mypath)
        #: Layoutoption - horizontal expansible
        self.rightInput.setStretchable(0,True)
        #: Check input
        self.rightInput.setValidChars("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890._/-")
        #
        #: Log- and progress frame
        self.progressLogFrame1  = self.factory.createFrame(self.right, "Log/Fortschritt")
        #: Layoutoption (horizontal, weighting)
        self.progressLogFrame1.setWeight(0,100)
        #
        #: Subframe for Log
        self.progressLogFrame   = self.factory.createVBox(self.progressLogFrame1)
        #
        #: Logwindow
        self.mainLogView        = self.factory.createLogView(self.progressLogFrame, "Log", 2, 20)
        #
        #: Progressbar
        self.mainProgressBar    = self.factory.createProgressBar(self.progressLogFrame, "Fortschritt")
        # mainbuttons
        # ---------------------
        #  | selbox  | right |
        # ---------------------
        # [load] [save] [cancel]
        self.mainBottomHBox1    = self.factory.createHBox(self.mainVBox)
        # Help
        self.mainBottomLeft     = self.factory.createLeft(self.mainBottomHBox1)
        self.mainButtonHelp     = self.factory.createPushButton(self.mainBottomLeft, "&Hilfe")
        # Navigation
        self.mainBottomRight    = self.factory.createRight(self.mainBottomHBox1)
        self.mainBottomHBox     = self.factory.createHBox(self.mainBottomRight)
        self.mainCancel         = self.factory.createPushButton(self.mainBottomHBox, "&Quit!")
        self.mainClose          = self.factory.createPushButton(self.mainBottomHBox, "Close")
        self.mainCheck          = self.factory.createPushButton(self.mainBottomHBox, "Check/&Weiter")
        self.mainGo             = self.factory.createPushButton(self.mainBottomHBox, "&GO!")
        self.event              = None
        self.mainCheck.setDefaultButton()
        self.mainGo.setDisabled()
        #
        # Print welcome msg
        self.mainLogView.appendLines(u"\n".encode("utf-8"))
        self.mainLogView.appendLines(u"Willkommen zu LiRE_Limbo\n".encode("utf-8"))
        self.mainLogView.appendLines(u"Wählen Sie eine Zielkonfiguration,\n".encode("utf-8"))
        self.mainLogView.appendLines(u"einen Ausgabepfad und klicken Sie auf 'Weiter'!\n".encode("utf-8"))
        #
        # Setze verwendetes Profil nach der Variable "lastprofile"
        #print self.profileList
        if True:
            if self.configDict.has_key("lastprofile"):
                #print self.configDict["lastprofile"]
                if self.configDict["lastprofile"] in self.profileList:
                    msg = u"Wähle zuletzt verwendetes Profil: %s!\n".encode("utf-8") % (str(self.configDict["lastprofile"]),)
                    self.mainLogView.appendLines(msg) 
                    self.rightComboBox.selectItem(self.rightComboBox.findItem(self.configDict["lastprofile"]))
                    result = self.Template.getConfigDict(str(self.rightComboBox.selectedItem().label()), self.mainLogView)
                    if result:
                        #print self.configDict
                        self.configDict = result.copy()
                        #print self.configDict
            else:
                selected = self.rightComboBox.selectedItem()
                #if Std(empty/nothing/last) :
                if selected == self.textLireStd:
                    pass  # do nothing
                else:
                    result = self.Template.getConfigDict(selected, self.mainLogView)
                    if result:
                        #print self.configDict
                        self.configDict = result.copy()
                        #print self.configDict
    
    #############
    # functions #
    #############
    def updateProfileList(self):
        """
        Update rightComboBox with the available profiles
        
        @param self.textLireStd: Empty profile "Standard"
        @type self.textLireStd: String
        @param self.profileList: List of known profiles
        @type self.profileList: List of Strings
        """
        self.rightComboBox.deleteAllItems()
        self.rightComboBox.addItem(self.textLireStd)
        for i in self.profileList:
            if str(i) == str(self.textLireStd):
                # don't add twice
                continue
            self.rightComboBox.addItem(str(i))
        # possibly recalc the layout 
        #self.mainDialog.recalcLayout()
    
    def loadProfile(self):
        #
        # load the profile and update the fields !
        pass
    
    def saveProfile(self):
        #
        # save the profile and update the fields
        pass
    
    def expertOn(self):
        """setup expert view
        """
        #
        # switch button state
        self.mainGo.setDefaultButton(0)
        self.mainCheck.setEnabled()
        self.mainGo.setDisabled()
        self.mainCheck.setDefaultButton()
        self.leftSelBox.selectItem(self.leftSelBox.findItem(self.textLireSelboxStart) , True)
        self.mainLogView.appendLines(str(u"Erweiterter Modus ausgewählt.\n".encode("utf-8")))
        #
        # change the leftselbox to contain all ITEMS
        self.leftSelBox.deleteAllItems()
        self.configExpert = True
        self.leftSelBox.addItem(self.textLireSelboxStart)
        self.leftSelBox.addItem(self.textLireSelboxNetzwerk)
        self.leftSelBox.addItem(self.textLireSelboxRepository)
        self.leftSelBox.addItem(self.textLireSelboxSoftware)
        self.leftSelBox.addItem(self.textLireSelboxXenomai)
        self.leftSelBox.addItem(self.textLireSelboxErweitert)
        self.leftSelBox.addItem(self.textLireSelboxDienste)

    def expertOff(self):
        """setup expert view
        """
        #
        # switch button state
        self.mainGo.setDefaultButton(0)
        self.mainCheck.setEnabled()
        self.mainGo.setDisabled()
        self.mainCheck.setDefaultButton()
        self.leftSelBox.selectItem(self.leftSelBox.findItem(self.textLireSelboxStart) , True)
        self.mainLogView.appendLines(str(u"Erweiterter Modus abgewählt.\n".encode("utf-8")))
        #
        # change the leftselbox to contain all ITEMS
        self.leftSelBox.deleteAllItems()
        self.configExpert = False
        self.leftSelBox.addItem(self.textLireSelboxStart)
        self.leftSelBox.addItem(self.textLireSelboxNetzwerk)

    def wizardOn(self):
        """switch Wizard view on
        """
        #
        # switch button state
        self.mainGo.setDefaultButton(0)
        self.mainGo.setDisabled()
        self.mainCheck.setEnabled()
        self.mainCheck.setDefaultButton()
        self.leftSelBox.selectItem(self.leftSelBox.findItem(self.textLireSelboxStart) , True)
        self.mainLogView.appendLines(u"Assistent ausgewählt.\n".encode("utf-8"))
        #
        # change the leftselbox to contain all ITEMS
        self.leftSelBox.deleteAllItems()
        self.configExpert = True
        self.leftSelBox.addItem(self.textLireSelboxStart)
        self.leftSelBox.addItem(self.textLireSelboxNetzwerk)
        self.leftSelBox.addItem(self.textLireSelboxRepository)
        self.leftSelBox.addItem(self.textLireSelboxSoftware)
        self.leftSelBox.addItem(self.textLireSelboxXenomai)
        self.leftSelBox.addItem(self.textLireSelboxErweitert)
        self.leftSelBox.addItem(self.textLireSelboxDienste)

    def wizardOff(self):
        """switch wizard view off
        """
        #
        # switch button state
        self.mainGo.setDefaultButton(0)
        self.mainGo.setDisabled()
        self.mainCheck.setEnabled()
        self.mainCheck.setDefaultButton()
        self.leftSelBox.selectItem(self.leftSelBox.findItem(self.textLireSelboxStart) , True)
        self.mainLogView.appendLines(u"Assistent abgewählt.\n".encode("utf-8"))
        #
        # change the leftselbox to contain all ITEMS
        self.leftSelBox.deleteAllItems()
        self.configExpert = False
        self.leftSelBox.addItem(self.textLireSelboxStart)
        self.leftSelBox.addItem(self.textLireSelboxNetzwerk)

    def doNetwork(self):
        """network popup
        """
        #
        # open the network GUI
        MY_NETWORK_GUI = GUI_netzwerk.GUI_netzwerk(self.factory, self.mainDialog.this, self.stateDict, self.configDict)
        self.stateDict, self.configDict = MY_NETWORK_GUI.handleEvent()
        if self.configDict["net_input_ip"] == "DHCP":
            self.configDict["lire_target"]["config_lire_target_main_ip"]="DHCP"
            self.configDict["lire_target"]["config_lire_target_hostname"]=self.configDict["net_input_hostname"]
        else:
            if self.configDict.has_key("required"):
                for i in self.configDict["required"]:
                    if str(i).split("_")[0] == "net":
                        msg = u""+str(str(i).split("_")[2]+": "+str(self.configDict[i])+"\n")
                        self.mainLogView.appendLines(msg.encode("utf-8"))
                        self.configDict["lire_target"]["config_lire_target_main_ip"]=self.configDict["net_input_ip"]
                        self.configDict["lire_target"]["config_lire_target_hostname"]=self.configDict["net_input_hostname"]

            else:
                msg = str(u"Konfigurationsvariablen 'required' fehlen. Vollständigkeitsprüfung nicht möglich!")
                self.mainLogView.appendLines(msg.encode("utf-8"))
            
    
    def doRepositories(self):
        """repositories popup
        """
        #
        # open GUI for repositories
        MY_REPOSITORY_GUI = GUI_repository.GUI_repository(self.factory, self.mainDialog.this, self.stateDict, self.configDict)
        self.stateDict, self.configDict = MY_REPOSITORY_GUI.handleEvent()
        if not self.configDict.has_key("repo_active"):
            self.configDict["repo_active"] = []
        nr_repo = self.configDict["repo_active"].__len__()
        if nr_repo == 0:
            msg = u"Kein Repository hinzugefügt! Fehler!\n"
            self.mainLogView.appendLines(msg.encode("utf-8"))
        if nr_repo == 1:
            msg = u"Ein Repository hinzugefügt\n"
            self.mainLogView.appendLines(msg.encode("utf-8"))
        else:
            msg = u"".encode("utf-8")+str(str(nr_repo)+u" Repositories hinzugefügt\n".encode("utf-8"))
            self.mainLogView.appendLines(msg)
        for i in self.configDict["repo_active"]:
            key_url = str("repo_input_url_"+str(i))
            msg = u"Repository #".encode("utf-8")+str(i)+": ".encode("utf-8")+str(self.configDict[key_url]+"\n".encode("utf-8"))
            self.mainLogView.appendLines(msg)
        
    def doSoftware(self):
        """software popup
        """
        #
        # open GUI for software selection
        MY_SOFTWARE_GUI = GUI_software.GUI_software(self.factory, self.mainDialog.this, self.stateDict, self.configDict)
        self.stateDict, self.configDict = MY_SOFTWARE_GUI.handleEvent()
        if self.configDict.has_key("soft_to_install"):
            for i in self.configDict["soft_to_install"]:
                msg = str(u"Paket ".encode("utf-8")+str(i).encode("utf-8")+u" ausgewählt\n".encode("utf-8"))
                self.mainLogView.appendLines(msg)
        else:
            #
            # no software selected - set "SOFTWARE_DONE" to 0
            self.stateDict["SOFTWARE_DONE"] = 0
    
    def doXenomai(self):
        """xenomai popup
        """
        #
        # open GUI for xenomai
        MY_XENOMAI_GUI = GUI_xenomai.GUI_xenomai(self.factory, self.mainDialog.this, self.stateDict, self.configDict)
        self.stateDict, self.configDict = MY_XENOMAI_GUI.handleEvent()

    def doErweitert(self):
        """misc popup
        """
        MY_ERWEITERT_GUI = GUI_erweitert.GUI_erweitert(self.factory, self.mainDialog.this, self.stateDict, self.configDict)
        self.stateDict, self.configDict = MY_ERWEITERT_GUI.handleEvent()

    def doDienste(self):
        """services popup
        """
        MY_DIENSTE_GUI = GUI_dienste.GUI_dienste(self.factory, self.mainDialog.this, self.stateDict, self.configDict)
        self.stateDict, self.configDict = MY_DIENSTE_GUI.handleEvent()
    
    def doKiwiWrite(self):
        """Write the XML-file
        """
        output = self.rightComboBoxOutput.selectedItem().label()
 
        # TEMPORARY !!!
        # TODO: CD
#        if not output == "ext2":
#            print output
#            msg = str(u"Fehler!\n Ausgabe nur für ext2 implementiert!".encode("utf-8"))
#            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
#            WARNING_URL_GUI.handleEvent()
#            return False
        myKiwiWrite = KIWI_write.KIWI_write(self.factory, self.mainDialog.this, self.configDict)
        # write std kiwi config
        result = myKiwiWrite.writeXml(output)
        if result:
            # write OBS kiwi config
            result2 = myKiwiWrite.writeKiwi(output)
        if result2:
            return True
        return False

    def doImageRootWrite(self):
        """Write the lire.conf and others
        """
        myImageRoot = IMAGEROOT_write.IMAGEROOT_write(self.factory, self.mainDialog.this, self.configDict)
        # write
        result = myImageRoot.write()
        if not result:
            return False # error
        # compress for obs-transfer
        result = myImageRoot.compress()
        return result
    
    def checkPath(self):
        """Check if output path exists
        """
        testPath = self.rightInput.value()
        if os.path.exists(testPath):
            if os.path.isdir(testPath):
                self.configDict["output_dir"] = testPath
                msg = str(u"Ordner "+str(testPath)+" vorhanden.\n")
                self.mainLogView.appendLines(msg.encode("utf-8"))
                return True
            else:
                msg = str(u"Fehler!\n"+str(testPath)+u" ist vorhanden, jedoch kein Ordner!".encode("utf-8"))
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
                WARNING_URL_GUI.handleEvent()
                return False
        else:
            try:
                os.makedirs(testPath)
            except:
                msg = str(u"Fehler!\nKonnte Verzeichnis "+str(testPath)+u" nicht anlegen!".encode("utf-8"))
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
                WARNING_URL_GUI.handleEvent()
                return False
            msg = str(u"Ordner ".encode("utf-8")+str(testPath)+u" erstellt.\n".encode("utf-8"))
            self.mainLogView.appendLines(msg)
            self.configDict["output_dir"] = testPath
            return True
        
    def doTimeoutLoop(self, myTransfer):
        """ Loop after transfer to OBS
        """
        MY_TIMEOUT_POPUP = GUI_timeout_popup.GUI_timeout_popup(self.factory, self.mainDialog.this, myTransfer)
        result = MY_TIMEOUT_POPUP.handleEvent()
        return result
        
    def valueCheck(self):
        """Check for mandatory variables
        """
        result = True
        for i in self.configDict["required"]:
            if self.configDict.has_key(i):
                # and not None
                if self.configDict["net_input_ip"]=="DHCP":
                    if i == "net_input_defaultroute":
                        continue
                    if i == "net_input_netmask":
                        continue
                    if i == "net_input_defaultroute":
                        continue
                if self.configDict[i] == None:
                    msg = str(u"Fehler!\nDie Variable %s ist vorhanden, aber leer. Führen Sie eine vollständige Konfiguration durch!".encode("utf-8")) % str(i)
                    WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
                    WARNING_URL_GUI.handleEvent()
                    result = False
                # shouldn't be empty
                if self.configDict[i] == "":
                    msg = str(u"Fehler!\nDie Variable %s ist vorhanden, aber leer. Führen Sie eine vollständige Konfiguration durch!".encode("utf-8")) % str(i)
                    WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
                    WARNING_URL_GUI.handleEvent()
                    result = False
            else:
                if self.configDict["net_input_ip"]=="DHCP":
                    if i == "net_input_defaultroute":
                        continue
                    if i == "net_input_netmask":
                        continue
                    if i == "net_input_defaultroute":
                        continue
                msg = str(u"Fehler!\nDie Variable %s ist nicht gesetzt. Führen Sie eine vollständige Konfiguration durch!".encode("utf-8")) % str(i)
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
                WARNING_URL_GUI.handleEvent()
                result = False
        return result

    def checkAPI(self):
        """Check if API-Server is available
        """
        # some string conversions
        tmpURL = self.rightInputAPI.value()
        if "http:" in tmpURL:
            tmpURL1a = str(tmpURL).split("http://")[1]
            tmpURL1 = tmpURL1a
        else:
            tmpURL1 = tmpURL
            tmpURL = "http://"+tmpURL1        
        if "/" in tmpURL1:
            tmpURL2 = str(tmpURL1).split("/")[0]
        else:
            tmpURL2 = tmpURL1
            tmpURL = tmpURL+"/"
        self.rightInputAPI.setValue(str(tmpURL))
        self.configDict["api_url"] = str(tmpURL) 
        result = False
        # simple test for availabilty
        # check port 80 / request url which should be returned by the api
        try:
            conn = httplib.HTTPConnection(str(tmpURL2))
            conn.request("GET", "/public")
            r1 = conn.getresponse()
            # status should be 200 - also seen 500 - could depend on version
            if not ((r1.status == 200) | (r1.status == 500)):
                msg = str(u"Error:\nAPI-Server nicht erreichbar!\nÜberprüfen Sie die URL.\n\n(Lokaler Aufruf von KIWI möglich!)".encode("utf-8")+"\nStatus: "+r1.status+"\nResult: "+r1.result)
                #
                # error popup 
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
                WARNING_URL_GUI.handleEvent()
                result = False
            else:
                msg = str(u"\nAPI-Server erreichbar\n".encode("utf-8"))
                self.mainLogView.appendLines(msg)
                result = True
        except httplib.InvalidURL:
            e = sys.exc_info()[1]
            msg = "Error:\n "+str(e)+"\n"+u"API-Server nicht erreichbar!\nÜberprüfen Sie die URL.\n\n(Lokaler Aufruf von KIWI möglich!)".encode("utf-8")
            #
            # error popup 
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
            WARNING_URL_GUI.handleEvent()
            result = False
        except   socket.error:
            e = sys.exc_info()[1][1]
            msg = "Error:\n "+str(e)+"\n"+u"API-Server nicht erreichbar!\nÜberprüfen Sie die URL. (Socket error)\n\n(Lokaler Aufruf von KIWI möglich!)".encode("utf-8")
            #
            # error popup 
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
            WARNING_URL_GUI.handleEvent()
            result = False
        except: # anything i can't think of :(
            e = sys.exc_info()[1]
            msg = "Error:\n "+str(e)+"\n"+u"API-Server nicht erreichbar!\nÜberprüfen Sie die URL.\n\n(Lokaler Aufruf von KIWI möglich!)".encode("utf-8")
            #
            # error popup 
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
            WARNING_URL_GUI.handleEvent()
            result = False
        return result


    #############
    # eventloop #
    #############
    def handleEvent(self):
        """Eventloop
        """
        while True:
            #
            # big parachute to keep application running
            try:
                #
                #: get event and evaluate
                self.event = self.mainDialog.waitForEvent()
                if not self.event:
                    continue
                #
                # Window closed ? == yui.YEvent.CancelEvent
                if self.event.eventType() == yui.YEvent.CancelEvent:
                    self.mainDialog.destroy() # do nothing and just quit
                    break
                #
                # "Check"/"Weiter" button Question is to only use this for wizard and check-run.
                if self.event.widget() == self.mainCheck:
                    #
                    # We are at the beginning E.g. Wizard/Expert/normal run
                    if self.stateDict["START"] == 0:
                        #
                        # set START=1 and go to NETWORK
                        if not self.checkPath():
                            continue
                        self.stateDict["START"] = 1
                        self.leftSelBox.selectItem(self.leftSelBox.findItem(self.textLireSelboxNetzwerk) , True)
                        self.stateDict["NETZWERK"] = 1
                    #
                    # We can run the NETWORK setup
                    if (self.stateDict["NETZWERK"] == 1) and (self.stateDict["NETZWERK_DONE"] == 0):
                        self.doNetwork()
                    #
                    # Switch small/big config 
                    if self.stateDict["NETZWERK_DONE"] == 1:
                        #
                        # check if "GO!" or "REPOSITORY"
                        if (self.configExpert or self.configWizard):
                            if self.stateDict["REPOSITORY_DONE"] == 0:
                                self.stateDict["REPOSITORY"] = 1
                                self.leftSelBox.selectItem(self.leftSelBox.findItem(self.textLireSelboxRepository) , True)
                        else: # we're ready (default profiles)
                            #
                            # small config
                            # unhide "GO!"
                            if (self.valueCheck()):
                                self.canTransfer = self.checkAPI()
                                if self.canTransfer:
                                    self.mainCheck.setDisabled()
                                    self.stateDict["READY"] = 1
                                self.mainGo.setEnabled()
                                self.mainCheck.setDefaultButton(0)
                                self.mainGo.setDefaultButton()
                                continue
                            else:
                                # check went wrong, need to check setup
                                continue
                    #
                    # ask for REPOSITORY
                    if (self.stateDict["REPOSITORY"] == 1) and (self.stateDict["REPOSITORY_DONE"] == 0):
                        self.doRepositories()
                        if self.stateDict["SOFTWARE"] == 1:
                            self.leftSelBox.selectItem(self.leftSelBox.findItem(self.textLireSelboxSoftware) , True)
                        if self.configWizard:
                            pass
                        else:
                            continue
                    #
                    # Ask for software
                    if (self.stateDict["SOFTWARE"] == 1) & (self.stateDict["SOFTWARE_DONE"] == 0):
                        self.doSoftware()
                        if self.stateDict["XENOMAI"] == 1:
                            self.leftSelBox.selectItem(self.leftSelBox.findItem(self.textLireSelboxXenomai) , True)
                        if self.configWizard:
                            pass
                        else:
                            continue
                    #
                    # get values for xenomai
                    if (self.stateDict["XENOMAI"] == 1) & (self.stateDict["XENOMAI_DONE"] == 0):
                        self.doXenomai()
                        if self.stateDict["ERWEITERT"] == 1:
                            self.leftSelBox.selectItem(self.leftSelBox.findItem(self.textLireSelboxErweitert) , True)
                        #self.doKiwiWrite()
                        if not self.configWizard:
                            continue
                    #
                    # get misc values
                    if (self.stateDict["ERWEITERT"] == 1) & (self.stateDict["ERWEITERT_DONE"] == 0):
                        self.doErweitert()
                        if self.stateDict["DIENSTE"] == 1:
                            self.leftSelBox.selectItem(self.leftSelBox.findItem(self.textLireSelboxDienste) , True)
                        if not self.configWizard:
                            continue
                    #
                    # get values for services
                    if (self.stateDict["DIENSTE"] == 1) & (self.stateDict["DIENSTE_DONE"] == 0):
                        self.doDienste()
                        if not self.configWizard:
                            continue
                    #
                    # we're ready ?
                    result = True
                    for i in self.stateDict.keys():
                        if "_DONE" in i:
                            if not self.stateDict[i] == 1:
                                result = False
                    if result:
                        self.stateDict["READY"] = 1
                    else:
                        continue
                    #
                    # we're ready !
                    if self.stateDict["READY"] == 1:
                        if (self.valueCheck()):
                            if self.configWizard:
                                #
                                # wizard mode
                                MY_WIZARD_GUI = GUI_wizard.GUI_wizard(self.factory, self.mainDialog.this, self.stateDict, self.configDict)
                                (name, desc, error) = MY_WIZARD_GUI.handleEvent()
                                if name == None:
                                    continue
                                if desc == None:
                                    continue
                                if error:
                                    continue
                                #
                                # write
                                self.configDict["profile"] = name
                                self.configDict["templatedesc"] = desc
                                self.configDict["lastprofile"] = name
                                result = self.Template.saveConfigDict(name, self.configDict)
                                if result:
                                    # wrote dump
                                    # don't ask again
                                    self.configWizard = False
                                    # reload and update
                                    self.profileList = self.Template.getTemplateList()
                                    self.updateProfileList()
                                    msg = str(u"Speicherung des Profils erfolgreich!\n".encode("utf-8"))
                                    self.mainLogView.appendLines(msg)
                                    self.rightComboBox.selectItem(self.rightComboBox.findItem(name))
                                    continue 
                                else:
                                    # didn't write
                                    msg = str(u"Speicherung des Profils fehlgeschlagen!\n".encode("utf-8"))
                                    self.mainLogView.appendLines(msg)
                                    continue
                            else:
                                #
                                # expert mode
                                self.canTransfer = self.checkAPI()
                                if self.canTransfer:
                                    self.mainCheck.setDisabled()
                                    self.stateDict["READY"] = 1
                                self.mainGo.setEnabled()
                                self.mainCheck.setDefaultButton(0)
                                self.mainGo.setDefaultButton()
                        else:
                            # check went wrong, need to change values
                            self.stateDict["READY"] = 0
                            continue
                #
                # mainGo
                if self.event.widget() == self.mainGo:
                    result1 = self.doKiwiWrite()
                    if not result1:
                        msg = str(u"Speicherung der KIWI-Konfiguration fehlgeschlagen!\n".encode("utf-8"))
                        self.mainLogView.appendLines(msg)
                        continue # stay open, error was displayed
                    msg = str(u"Speicherung der KIWI-Konfiguration erfolgreich!\n".encode("utf-8"))
                    self.mainLogView.appendLines(msg)
                    self.mainProgressBar.setValue(10)
                    result2 = self.doImageRootWrite()
                    if not result2:
                        msg = str(u"Speicherung des root-Ordners fehlgeschlagen!\n".encode("utf-8"))
                        self.mainLogView.appendLines(msg)
                        continue # stay
                    self.mainProgressBar.setValue(20)
                    msg = str(u"Speicherung des root-Ordners erfolgreich beeindet!\n".encode("utf-8"))
                    self.mainLogView.appendLines(msg)
                    #
                    #: call transfer to server
                    if self.canTransfer:
                        msg = str(u"Starte Übertragung\n".encode("utf-8"))
                        self.mainLogView.appendLines(msg)
                        myTransfer = KIWI_transfer.KIWI_transfer(self.factory, self.mainDialog.this, self.configDict)
                        if myTransfer.test(self.mainLogView):
                            if myTransfer.checkOut(self.mainLogView):
                                if myTransfer.checkIn(self.mainLogView):
                                    msg = str(u"\nÜbertragung erfolgreich abgeschlossen.\n".encode("utf-8"))
                                    self.mainLogView.appendLines(msg)
                                    self.mainProgressBar.setValue(100)
                                    #self.mainProgressBar
                                    #
                                    self.uploaded = True 
                                else:
                                    #
                                    # checkin failed
                                    msg = str(u"\nCheckin fehlgeschlagen.\n".encode("utf-8"))
                                    self.mainLogView.appendLines(msg)
                                    self.mainProgressBar.setValue(0)
                                    continue
                            else:
                                #
                                # checkout failed
                                msg = str(u"\nCheckout fehlgeschlagen.\n".encode("utf-8"))
                                self.mainLogView.appendLines(msg)
                                continue
                        else:
                            #
                            # repo test failed
                            msg = str(u"\nAnlegen des Projekts/Repository fehlgeschlagen.\n".encode("utf-8"))
                            self.mainLogView.appendLines(msg)
                            continue
                    else:
                        msg = str(u"Übertragung an Server nicht möglich!\n\nKIWI kann dennoch lokal aufgerufen werden.\nVerlassen Sie dazu das Programm und\nrufen Sie KIWI direkt auf!\n".encode("utf-8"))
                        self.mainLogView.appendLines(msg)
                        continue
                        
                    # only transfer once ??
                    #self.mainGo.setDisabled()
                    #
                    # TODO: POPUP GUI FOR TRANSFER/CHECK
                    if self.canTransfer and self.uploaded:
                        obsresult = self.doTimeoutLoop(myTransfer)
                        print obsresult
                        if obsresult == "succeeded":
                            msg = str(u"Laden der Abbilddatei erfolgreich beendet!\n".encode("utf-8"))
                            self.mainLogView.appendLines(msg)
                        else:
                            #
                            msg = str(u"Abbilderstellung fehlgeschlagen!\n".encode("utf-8"))
                            self.mainLogView.appendLines(msg)
                #
                # cancel
                if self.event.widget() == self.mainCancel:
                    self.mainDialog.destroy()
                    return None, self.cmdmsg
                #
                # close
                if self.event.widget() == self.mainClose:
                    self.configDict["lastprofile"]= str(self.rightComboBox.selectedItem().label())
                    self.mainDialog.destroy()
                    return self.configDict, self.cmdmsg
                #
                # select step in config
                if self.event.widget() == self.leftSelBox:
                    # 
                    # single item selected
                    selectedItemLabel = self.leftSelBox.selectedItem().label()
                    if selectedItemLabel == self.textLireSelboxNetzwerk:
                        #
                        # call Network
                        self.doNetwork()
                    if selectedItemLabel == self.textLireSelboxRepository:
                        #
                        # call repository
                        self.doRepositories()
                    if selectedItemLabel == self.textLireSelboxSoftware:
                        #
                        # call Software
                        self.doSoftware()
                    if selectedItemLabel == self.textLireSelboxXenomai:
                        #
                        # call Xenomai
                        self.doXenomai()
                    if selectedItemLabel == self.textLireSelboxDienste:
                        #
                        # call Dienste
                        self.doDienste()
                    if selectedItemLabel == self.textLireSelboxErweitert:
                        #
                        # call misc
                        self.doErweitert()
                #
                # expert
                if self.event.widget() == self.rightCheckExpert:
                    if self.rightCheckExpert.isChecked():
                        self.expertOn()
                    else:
                        if not self.rightCheckWizard.isChecked():
                            self.expertOff()
                #
                # wizard
                if self.event.widget() == self.rightCheckWizard:
                    if self.rightCheckWizard.isChecked():
                        self.wizardOn()
                        self.configWizard = True
                    else:
                        self.configWizard = False
                        if not self.rightCheckExpert.isChecked():
                            self.wizardOff()            
                #
                # combobox for profile
                if self.event.widget() == self.rightComboBox:
                    #
                    # default
                    if self.rightComboBox.selectedItem().label() == "Standard":
                        continue
                    self.profileList = self.Template.getTemplateList()
                    #self.mainLogView.appendLines(str(self.profileList))
                    if self.rightComboBox.selectedItem().label() in self.profileList:
                        #
                        # can update
                        # 
                        result = self.Template.getConfigDict(str(self.rightComboBox.selectedItem().label()), self.mainLogView)
                        if result:
                            #
                            # change folder also
                            # self.Template.changeRootFolder
                            #self.mainLogView.appendLines(str(type(result)))
                            #self.mainLogView.appendLines(str(result))
                            self.configDict = result.copy()
                            self.configDict["lastprofile"] = str(self.rightComboBox.selectedItem().label())
                        #
                        # TODO: update statedict ?
                        # TODO: update wizard/expert ?
                        # TODO: update GO/Cancel ?
                    elif str(self.rightComboBox.selectedItem().label()) == str(self.textLireStd):
                        #reset - can be improved
                        self.configDict = self.configDictOrig.copy()
                    else:
                        # just stay alive - shouldn't really happen
                        continue 
            except:
                e = sys.exc_info()[1]
                import traceback
                for line in traceback.format_tb(sys.exc_traceback):
                    e = str(e) + "\n" + str(line)
                msg = "Kritischer Fehler:\n "+str(e)+u"\nSpeichern Sie ihr Profil und\nstarten Sie das Programm neu!".encode("utf-8")
                #
                # error popup 
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.mainDialog.this, msg)
                WARNING_URL_GUI.handleEvent()
                continue
            
if __name__ == "__main__":
    """ Standalone check
    """
    import locale
    locale.setlocale(locale.LC_ALL, "")
    
    factory = yui.YUI.widgetFactory()
    state = "START"
    configdict = {}
    configdict["lastprofile"] = ""
    configdict["api_url"] = "http://192.168.10.246" 
    statedict = {}
    statedict["START"]          = 1
    statedict["NETZWERK"]       = 0
    statedict["NETZWERK_DONE"]  = 0
    statedict["REPOSITORY"]     = 0
    statedict["REPOSITORY_DONE"]= 0
    statedict["SOFTWARE"]       = 0
    statedict["SOFTWARE_DONE"]  = 0
    statedict["XENOMAI"]        = 0
    statedict["XENOMAI_DONE"]   = 0
    statedict["DIENSTE"]        = 0
    statedict["DIENSTE_DONE"]   = 0
    statedict["ERWEITERT"]      = 0
    statedict["ERWEITERT_DONE"] = 0
    statedict["READY"]          = 0    
    MY_MAIN_GUI = GUI_main(factory, statedict, configdict)
    MY_MAIN_GUI.handleEvent()
    
