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
# GUI_erweitert.py
# Ask for the erweitert options
"""GUI_erweitert - popup window for 'erweitert' options"""
###########
# imports #
###########
import yui                  # GUI
import GUI_warning_popup    # popup

######################
# class GUI_software #
######################
class GUI_erweitert(object):
    """ GUI_erweitert(myFactory, myParent, myStateDict, myConfigDict), returns stateDict, configDict

        GUI_erweitert - popup window for 'erweitert' options
    
        @param myFactory: widgetFactory to use
        @type myFactory: Instance of widgetFactory
        @param myParent: parent widget
        @type myParent: Instance of YDialog 
        @param myStateDict: stateDict
        @type myStateDict: Dictionary
        @param myConfigDict: configDict
        @type myConfigDict: Dictionary
    
        @return: (stateDict, configDict)
        @rtype: (Dictionary, Dictionary)
    """
    def __init__(self, myFactory, myParent, myStateDict, myConfigDict):
        """__init__
        """
        #
        # variables
        self.factory = myFactory
        self.appl = yui.YUI.application()
        self.stateDict = myStateDict.copy()
        self.configDictOrig = myConfigDict.copy()
        self.configDict = myConfigDict.copy()
        self.parent = myParent
        self.error = False
        self.erweitertDialog = self.factory.createMainDialog()
        #
        # generate categories and sections
        self.erweitertCategories = str(self.configDict["lire_target"]["cat_erweitert"]).split(",")
        self.erweitertSections = {} # erweitertSections[ITEM] = 
        x = self.configDict["lire_target"].copy()
        #
        # iterate over all config-values
        for i in x.keys():
            #
            # for all items i should work with
            for j in self.erweitertCategories:
                # j part of i ?
                if j.lower() in i:
                    self.erweitertSections[i] = self.configDict["lire_target"][i]
        #
        # check and handle "PREREQ" (software)
        for k in self.erweitertSections.keys():
            if "prereq" in k:
                # PREREQ SECTION, remove it
                myprereq = str(self.erweitertSections.pop(k)).split(",")
                # empty prereq - continue
                if myprereq == ["",]: # empty list ;)
                    continue
                else:
                #prereq not empty, we need to check it!
                    for n in myprereq:
                        if n in self.configDict["soft_to_install"]:
                            # software marked for installation - good
                            continue
                        else:
                            # we miss software "n" to handle category k
                            # nag popup
                            myCat = str(k.split("config_lire_")[1].split("_prereq")[0])
                            msg = str(u"Fehler!\nDie Kategorie %s erfordert das Softwarepaket %s.\nDies muss in der Paketauswahl vorgenommen werden!\nRückkehr ins Hauptmenu.".encode("utf-8")) %  (myCat, n)
                            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.parent, msg)
                            WARNING_URL_GUI.handleEvent()
                            self.stateDict["SOFTWARE_DONE"] = 0
                            self.stateDict["REPOSITORY"] = 0
                            self.error = True
        if self.error:
            return # bail out, will stop event at once
        #
        # construct gui
        #
        # ###################
        # #     #     # [x] #
        # #  c  #  s  # ver #
        # #  a  #  e  #######
        # #  t  #  c  # de  #
        # #     #     #  sc #
        # ###################
        # # <>         <> <>#
        # ###################
        #
        # VBox
        self.erweitertMainVBox = self.factory.createVBox(self.erweitertDialog)
        #
        # HBox
        self.erweitertMainHBox = self.factory.createHBox(self.erweitertMainVBox)
        self.erweitertMainHBox.setStretchable(1,True)
        self.erweitertMainHBox.setWeight(1,100)
        #
        # cat
        # minsize
        self.erweitertCatSelectMinSize = self.factory.createMinSize(self.erweitertMainHBox, 15, 15)
        # selectbox for category
        self.erweitertCatSelectBox = self.factory.createSelectionBox(self.erweitertCatSelectMinSize, "K&ategorien")
        self.erweitertCatSelectBox.setWeight(0,50) # 0 = horiz
        self.erweitertCatSelectBox.setStretchable(0,True)
        #self.erweitertCatSelectBox.setWeight(1,25)
        #self.erweitertCatSelectBox.setStretchable(1,True)
        self.erweitertCatSelectBox.setNotify()
        self.erweitertCatSelectBox.setImmediateMode()
        self.erweitertCatSelectBox.setSendKeyEvents(True)
        #
        # sec
        # minsize
        self.erweitertSecSelectMinSize = self.factory.createMinSize(self.erweitertMainHBox, 30, 15)
        # selectbox for sec
        self.erweitertSecSelectBox =  self.factory.createSelectionBox(self.erweitertSecSelectMinSize, "&Optionen")
        self.erweitertSecSelectBox.setWeight(0,50)
        self.erweitertSecSelectBox.setStretchable(0,True)
        #self.erweitertSecSelectBox.setWeight(1,20)
        #self.erweitertSecSelectBox.setStretchable(1,True)
        self.erweitertSecSelectBox.setNotify()
        self.erweitertSecSelectBox.setImmediateMode()
        self.erweitertCatSelectBox.setSendKeyEvents(True)
        #
        # right HBox
        self.erweitertRightVBox = self.factory.createVBox(self.erweitertMainHBox)
        self.erweitertRightVBox.setWeight(0,10)
        self.erweitertRightVBox.setStretchable(0, True)
        self.erweitertRightVBox.setStretchable(1, True)
        self.erweitertRightVBox.setWeight(1,10)
        #
        # replacepoint 1
        self.erweitertRightStatusFrame = self.factory.createFrame(self.erweitertRightVBox, "Wert")
        self.erweitertRightStatusFrame.setWeight(0,100)
        self.erweitertRightStatusFrame.setWeight(1,30)
        self.erweitertRightStatusFrame.setStretchable(0, True)
        self.erweitertRightStatusFrame.setStretchable(1, True)
        self.erweitertRightReplacePoint1 = self.factory.createReplacePoint(self.erweitertRightStatusFrame)
        self.erweitertRightReplacePoint1.setWeight(0,100)
        self.erweitertRightReplacePoint1.setStretchable(0, True)
        self.erweitertRightReplacePoint1.setStretchable(1, True)
        #
        # dummy widgets for replacepoint1
        self.erweitertRightVBox1 = self.factory.createVBox(self.erweitertRightReplacePoint1)
        self.erweitertRightVBox1.setWeight(0,100)
        self.erweitertRightVBox1.setWeight(1,10)
        self.erweitertRightVBox1.setStretchable(0, True)
        self.erweitertRightVBox1.setStretchable(1, True)
        self.erweitertRightHBox1 = self.factory.createHBox(self.erweitertRightVBox1)
        self.erweitertRightHBox1.setWeight(0,100)
        self.erweitertRightHBox1.setWeight(1,100)
        self.erweitertRightHBox1.setStretchable(0, True)
        self.erweitertRightHBox1.setStretchable(1, True)
        self.erweitertRightStatusNameLabel = self.factory.createLabel(self.erweitertRightHBox1, "Name:")
        self.erweitertRightStatusName = self.factory.createLabel(self.erweitertRightHBox1, "Foo")
        self.erweitertRightStatusName.setStretchable(0,True)
        self.erweitertRightStatusValue = self.factory.createInputField(self.erweitertRightVBox1, "Wert")
        self.erweitertRightStatusValue.setStretchable(0,True)
        self.erweitertRightStatusValue.setNotify(True)
        #
        # replacepoint 2
        self.erweitertRightDescriptionFrame = self.factory.createFrame(self.erweitertRightVBox, "Beschreibung")
        self.erweitertRightDescriptionFrame.setWeight(0,100)
        self.erweitertRightDescriptionFrame.setWeight(1,90)
        self.erweitertRightDescriptionFrame.setStretchable(0, True)
        self.erweitertRightDescriptionFrame.setStretchable(1, True)
        self.erweitertRightReplacePoint2 = self.factory.createReplacePoint(self.erweitertRightDescriptionFrame)
        self.erweitertRightReplacePoint2.setStretchable(0, True)
        self.erweitertRightReplacePoint2.setStretchable(1, True)
        self.erweitertRightVBox2 = self.factory.createVBox(self.erweitertRightReplacePoint2)
        self.erweitertRightDescriptionOutDescription = self.factory.createRichText(self.erweitertRightVBox2, "Beschreibung")
        self.erweitertRightDescriptionOutDescription.setPlainTextMode(True)
        self.erweitertRightDescriptionOutDescription.setText("")
        
        #
        # bottom
        self.erweitertBottomHBox = self.factory.createHBox(self.erweitertMainVBox)
        #
        # help
        self.erweitertBottomHBox_left = self.factory.createLeft(self.erweitertBottomHBox)
        self.erweitertButtonHelp = self.factory.createPushButton(self.erweitertBottomHBox_left, "&Hilfe")
        self.erweitertBottomHBoxRight = self.factory.createRight(self.erweitertBottomHBox)
        self.erweitertBottomHBoxRight_hbox = self.factory.createHBox(self.erweitertBottomHBox)
        #
        # Add item
        self.erweitertButtonAdd = self.factory.createPushButton(self.erweitertBottomHBoxRight_hbox, "H&inzufügen")
        #
        # Remove item
        self.erweitertButtonRemove = self.factory.createPushButton(self.erweitertBottomHBoxRight_hbox, "&Entfernen")
        #
        # cancel
        self.erweitertButtonCancel = self.factory.createPushButton(self.erweitertBottomHBoxRight_hbox, "&Zurück")
        #
        # next
        self.erweitertButtonNext = self.factory.createPushButton(self.erweitertBottomHBoxRight_hbox, "&Weiter")
        #
        # add categories
        tosort = []
        for i in self.erweitertCategories:
            tosort.append(i)
        tosort.sort()
        for i in tosort:        
            self.erweitertCatSelectBox.addItem(i)
        del tosort
        del i
        #
        # update checkbox
        self.secUpdate(self.erweitertCatSelectBox.selectedItem())
        #
        # update "last" category
        self.oldCategory = self.erweitertCatSelectBox.selectedItem()
        #
        # update pkg display area
        if self.erweitertSecSelectBox.selectedItem():
            self.dataUpdate(self.erweitertSecSelectBox.selectedItem().label())
        #
        # update "last" pkg
        self.oldSec = self.erweitertSecSelectBox.selectedItem()
        #
        # recalc the layout
        self.erweitertDialog.recalcLayout()
#===============================================================================


    #############
    # functions #
    #############
    def secUpdate(self, selected_item):
        """update the checkbox frame
        """
        #
        # label of the selected category
        label = selected_item.label()
        #
        # delete the old items
        self.erweitertSecSelectBox.deleteAllItems()
        #
        # iterate over names in self.erweitertCategories
        mylist = []
        for i in self.erweitertSections.keys():
            if str(str(label)+"_target_") in i:
                k = str(i).split(str(str(label)+"_target_"))[1]
                mylist.append(str(k))
        del i
        del k
        #sort it
        mylist.sort()
        for k in mylist:
            self.erweitertSecSelectBox.addItem(str(k))
        
        self.appl.redrawScreen() # redraw
        if self.erweitertSecSelectBox.selectedItem():
            selected = self.erweitertSecSelectBox.selectedItem().label()
            self.dataUpdate(selected)

    def dataUpdate(self, selected_item):
        for i in self.erweitertSections.keys():
            if str("_target_"+str(selected_item)) in i:
                self.erweitertRightStatusName.setText(i.split("config_lire_")[1])
                self.erweitertRightStatusValue.setValue(str(self.erweitertSections[i]))
        return
        self.erweitertRightStatusName.setText(str(selected_item))
        self.erweitertRightStatusVersion.setText(self.erweitertDict[selected_item]["Version"])
        if selected_item in self.toInstall:
            self.erweitertRightStatusInstall.setChecked(True)
        else:
            self.erweitertRightStatusInstall.setChecked(False)
        self.erweitertRightDescriptionOutSummary.setText(self.erweitertDict[selected_item]["Summary"])
        self.erweitertRightDescriptionOutDescription.setText(self.erweitertDict[selected_item]["Description"])

        self.appl.redrawScreen()
    
    def evalInput(self):
        """evaluate Input
        """
        tmp = []
        catLabel = self.oldCategory.label()  # category to evaluate
        secLabel = self.oldSec.label()
        print 2
        print catLabel
        print secLabel
        mySec = "config_lire_"+str(catLabel)+"_target_"+str(secLabel)
        print mySec
        self.erweitertSections[mySec] = self.erweitertRightStatusValue.value()
        self.erweitertRightStatusValue.value()
        #
        # just read InputField and assign to configDict
        
        
    #############
    # eventloop #
    #############
    def handleEvent(self):
        """Event loop
        """
        if self.error:
            # bail out (from "no software/repo" screen)
            return self.stateDict, self.configDictOrig
        while True:
            #
            # get event
            self.event = self.erweitertDialog.waitForEvent()
            #self.erweitertRightDescriptionOutDescription.setText(str(self.event.eventType()))
            if self.event.eventType == yui.YEvent.KeyEvent:
                #
                # ncurses
                if self.event.widget == self.erweitertCatSelectBox:
                    #
                    # possibly change to secselectbox if rightarrow
                    self.event
                    pass
            if not self.event:
                continue
            #
            # app destroyed [x]
            if self.event.eventType() == yui.YEvent.CancelEvent:
                if self.parent:
                    #
                    # return to parent and return old values
                    self.erweitertDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    #
                    # destroy for test
                    self.erweitertDialog.destroy()
                    return self.stateDict, self.configDictOrig
                return self.stateDict, self.configDictOrig
            #
            # category selected
            if self.event.widget() == self.erweitertCatSelectBox:
                # 
                # read Input ...
                self.evalInput()
                #
                # todo: dependency resolution
                #self.resolveDependency()
                #
                # update right frame / checkboxes
                self.secUpdate(self.erweitertCatSelectBox.selectedItem())
                self.oldCategory = self.erweitertCatSelectBox.selectedItem()
                self.oldSec = self.erweitertSecSelectBox.selectedItem()
            #
            # pkg selected
            if self.event.widget() == self.erweitertSecSelectBox:
                # 
                # read selected boxes ...
                self.evalInput()
                self.dataUpdate(self.erweitertSecSelectBox.selectedItem().label())
                self.oldSec = self.erweitertSecSelectBox.selectedItem()
            #
            # cancel
            if self.event.widget() == self.erweitertButtonCancel:
                if self.parent:
                    #
                    # return to parent and return old values
                    self.erweitertDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    #
                    # destroy for test
                    self.erweitertDialog.destroy()
                    return self.stateDict, self.configDictOrig
            #
            # next
            if self.event.widget() == self.erweitertButtonNext:
                # TODO:  fetch values into configdict
                self.evalInput()
                # statedict
                self.stateDict["ERWEITERT_DONE"] = 1
                self.stateDict["DIENSTE"] = 1
                if self.parent:
                    self.erweitertDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDict
                else:
                    self.erweitertDialog.destroy()
                    return self.stateDict, self.configDict

if __name__ == "__main__":
    import locale
    locale.setlocale(locale.LC_ALL, "")



    factory = yui.YUI.widgetFactory()
    statedict = {}
    configdict = {}
    softwaredict = {}
    softwaredict['openssl-doc'] = {}
    softwaredict['openssl-doc']["Group"] = 'Productivity'
    softwaredict['openssl-doc']["Version"] = '1.1.2.2'
    softwaredict['openssl-doc']["Summary"] = 'mySummary'
    softwaredict['openssl-doc']["Description"] = 'myDescription'
    softwaredict['openssl-doc1'] = {}
    softwaredict['openssl-doc1']["Group"] = 'Productivity1'
    softwaredict['openssl-doc1']["Version"] = '1.1.2.2'
    softwaredict['openssl-doc1']["Summary"] = 'mySummary'
    softwaredict['openssl-doc1']["Description"] = 'myDescription'
    configdict["softwareDict"] = softwaredict
    configdict["soft_to_install"] = ["openssl-doc1", ]
    configdict["defaultinstalledsoft"] = ["openssl-doc", ]
    configdict["lire_target"] = {}
    configdict["lire_target"]["cat_erweitert"] = "rtnet,rack"
    configdict["lire_target"]["config_lire_rack_prereq"] = ""
    configdict["lire_target"]["config_lire_rack_target_tims_router_log_level"] = "0"
    configdict["lire_target"]["config_lire_rtnet_prereq"] = ""
    configdict["lire_target"]["config_lire_rtnet_target_autostart"] = "None"
    
    MY_GUI = GUI_erweitert(factory, None, statedict, configdict)
    statedict, configdict = MY_GUI.handleEvent()


    print "statedict"
    print "#########"
    print statedict
    print ""
    print "configdict"
    print "##########"    
    print configdict
    print ""
