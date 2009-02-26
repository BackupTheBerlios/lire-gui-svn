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
# GUI_xenomai.py
# Ask for the xenomai options
"""GUI_xenomai - popup window for xenomai options"""
###########
# imports #
###########
import yui                  # GUI
import GUI_warning_popup    # popup
# import GUI_ask_insert       # ask_insert
# import GUI_ask_delete       # ask_delete 

######################
# class GUI_software #
######################
class GUI_xenomai(object):
    """ GUI_xenomai(myFactory, myParent, myStateDict, myConfigDict), returns stateDict, configDict
        
        GUI_xenomai - popup window for xenomai options
        
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
        self.xenomaiDialog = self.factory.createMainDialog()
        #
        # generate categories and sections
        self.xenomaiCategories = str(self.configDict["lire_target"]["cat_xenomai"]).split(",")
        self.xenomaiSections = {} # xenomaiSections[ITEM] = 
        x = self.configDict["lire_target"].copy()
        #
        # iterate over all config-values
        for i in x.keys():
            #
            # for all items i should work with
            for j in self.xenomaiCategories:
                # j part of i ?
                if j.lower() in i:
                    self.xenomaiSections[i] = self.configDict["lire_target"][i]
        #
        # check and handle "PREREQ" (software)
        for k in self.xenomaiSections.keys():
            if "prereq" in k:
                # PREREQ SECTION, remove it
                myprereq = str(self.xenomaiSections.pop(k)).split(",")
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
                            msg = str(u""+"Fehler!\nDie Kategorie %s erfordert das Softwarepaket %s.\nDies muss in der Paketauswahl vorgenommen werden!\nRückkehr ins Hauptmenu.".encode("utf-8")) %  (myCat, n)
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
        self.xenomaiMainVBox = self.factory.createVBox(self.xenomaiDialog)
        #
        # HBox
        self.xenomaiMainHBox = self.factory.createHBox(self.xenomaiMainVBox)
        self.xenomaiMainHBox.setStretchable(1,True)
        self.xenomaiMainHBox.setWeight(1,100)
        #
        # cat
        # minsize
        self.xenomaiCatSelectMinSize = self.factory.createMinSize(self.xenomaiMainHBox, 15, 15)
        # selectbox for category
        self.xenomaiCatSelectBox = self.factory.createSelectionBox(self.xenomaiCatSelectMinSize, "K&ategorien")
        self.xenomaiCatSelectBox.setWeight(0,50) # 0 = horiz
        self.xenomaiCatSelectBox.setStretchable(0,True)
        #self.xenomaiCatSelectBox.setWeight(1,25)
        #self.xenomaiCatSelectBox.setStretchable(1,True)
        self.xenomaiCatSelectBox.setNotify()
        self.xenomaiCatSelectBox.setImmediateMode()
        self.xenomaiCatSelectBox.setSendKeyEvents(True)
        #
        # sec
        # minsize
        self.xenomaiSecSelectMinSize = self.factory.createMinSize(self.xenomaiMainHBox, 30, 15)
        # selectbox for sec
        self.xenomaiSecSelectBox =  self.factory.createSelectionBox(self.xenomaiSecSelectMinSize, "&Optionen")
        self.xenomaiSecSelectBox.setWeight(0,50)
        self.xenomaiSecSelectBox.setStretchable(0,True)
        #self.xenomaiSecSelectBox.setWeight(1,20)
        #self.xenomaiSecSelectBox.setStretchable(1,True)
        self.xenomaiSecSelectBox.setNotify()
        self.xenomaiSecSelectBox.setImmediateMode()
        self.xenomaiCatSelectBox.setSendKeyEvents(True)
        #
        # right HBox
        self.xenomaiRightVBox = self.factory.createVBox(self.xenomaiMainHBox)
        self.xenomaiRightVBox.setWeight(0,10)
        self.xenomaiRightVBox.setStretchable(0, True)
        self.xenomaiRightVBox.setStretchable(1, True)
        self.xenomaiRightVBox.setWeight(1,10)
        #
        # replacepoint 1
        self.xenomaiRightStatusFrame = self.factory.createFrame(self.xenomaiRightVBox, "Wert")
        self.xenomaiRightStatusFrame.setWeight(0,100)
        self.xenomaiRightStatusFrame.setWeight(1,30)
        self.xenomaiRightStatusFrame.setStretchable(0, True)
        self.xenomaiRightStatusFrame.setStretchable(1, True)
        self.xenomaiRightReplacePoint1 = self.factory.createReplacePoint(self.xenomaiRightStatusFrame)
        self.xenomaiRightReplacePoint1.setWeight(0,100)
        self.xenomaiRightReplacePoint1.setStretchable(0, True)
        self.xenomaiRightReplacePoint1.setStretchable(1, True)
        #
        # dummy widgets for replacepoint1
        self.xenomaiRightVBox1 = self.factory.createVBox(self.xenomaiRightReplacePoint1)
        self.xenomaiRightVBox1.setWeight(0,100)
        self.xenomaiRightVBox1.setWeight(1,10)
        self.xenomaiRightVBox1.setStretchable(0, True)
        self.xenomaiRightVBox1.setStretchable(1, True)
        self.xenomaiRightHBox1 = self.factory.createHBox(self.xenomaiRightVBox1)
        self.xenomaiRightHBox1.setWeight(0,100)
        self.xenomaiRightHBox1.setWeight(1,100)
        self.xenomaiRightHBox1.setStretchable(0, True)
        self.xenomaiRightHBox1.setStretchable(1, True)
        self.xenomaiRightStatusNameLabel = self.factory.createLabel(self.xenomaiRightHBox1, "Name:")
        self.xenomaiRightStatusName = self.factory.createLabel(self.xenomaiRightHBox1, "Foo")
        self.xenomaiRightStatusName.setStretchable(0,True)
        self.xenomaiRightStatusValue = self.factory.createInputField(self.xenomaiRightVBox1, "Wert")
        self.xenomaiRightStatusValue.setStretchable(0,True)
        self.xenomaiRightStatusValue.setNotify(True)
        #
        # replacepoint 2
        self.xenomaiRightDescriptionFrame = self.factory.createFrame(self.xenomaiRightVBox, "Beschreibung")
        self.xenomaiRightDescriptionFrame.setWeight(0,100)
        self.xenomaiRightDescriptionFrame.setWeight(1,90)
        self.xenomaiRightDescriptionFrame.setStretchable(0, True)
        self.xenomaiRightDescriptionFrame.setStretchable(1, True)
        self.xenomaiRightReplacePoint2 = self.factory.createReplacePoint(self.xenomaiRightDescriptionFrame)
        self.xenomaiRightReplacePoint2.setStretchable(0, True)
        self.xenomaiRightReplacePoint2.setStretchable(1, True)
        self.xenomaiRightVBox2 = self.factory.createVBox(self.xenomaiRightReplacePoint2)
        self.xenomaiRightDescriptionOutDescription = self.factory.createRichText(self.xenomaiRightVBox2, "Beschreibung")
        self.xenomaiRightDescriptionOutDescription.setPlainTextMode(True)
        self.xenomaiRightDescriptionOutDescription.setText("")
        
        #
        # bottom
        self.xenomaiBottomHBox = self.factory.createHBox(self.xenomaiMainVBox)
        #
        # help
        self.xenomaiBottomHBox_left = self.factory.createLeft(self.xenomaiBottomHBox)
        self.xenomaiButtonHelp = self.factory.createPushButton(self.xenomaiBottomHBox_left, "&Hilfe")
        self.xenomaiBottomHBoxRight = self.factory.createRight(self.xenomaiBottomHBox)
        self.xenomaiBottomHBoxRight_hbox = self.factory.createHBox(self.xenomaiBottomHBox)
        #
        # Add item
        self.xenomaiButtonAdd = self.factory.createPushButton(self.xenomaiBottomHBoxRight_hbox, "H&inzufügen")
        #
        # Remove item
        self.xenomaiButtonRemove = self.factory.createPushButton(self.xenomaiBottomHBoxRight_hbox, "&Entfernen")
        #
        # cancel
        self.xenomaiButtonCancel = self.factory.createPushButton(self.xenomaiBottomHBoxRight_hbox, "&Zurück")
        #
        # next
        self.xenomaiButtonNext = self.factory.createPushButton(self.xenomaiBottomHBoxRight_hbox, "&Weiter")
        #
        # add categories
        tosort = []
        for i in self.xenomaiCategories:
            tosort.append(i)
        tosort.sort()
        for i in tosort:
            self.xenomaiCatSelectBox.addItem(i)
        del i
        del tosort
        #
        # update checkbox
        self.secUpdate(self.xenomaiCatSelectBox.selectedItem())
        #
        # update "last" category
        self.oldCategory = self.xenomaiCatSelectBox.selectedItem()
        #
        # update pkg display area
        if self.xenomaiSecSelectBox.selectedItem():
            self.dataUpdate(self.xenomaiSecSelectBox.selectedItem().label())
        #
        # update "last" pkg
        self.oldSec = self.xenomaiSecSelectBox.selectedItem()
        #
        # recalc the layout
        self.xenomaiDialog.recalcLayout()
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
        self.xenomaiSecSelectBox.deleteAllItems()
        #
        # iterate over names in self.xenomaiCategories
        mylist = []
        for i in self.xenomaiSections.keys():
            if str(str(label)+"_target_") in i:
                k = str(i).split(str(str(label)+"_target_"))[1]
                mylist.append(str(k))
        # sort it
        mylist.sort()
        for j in mylist:
            self.xenomaiSecSelectBox.addItem(str(j))
        self.appl.redrawScreen() # redraw
        if self.xenomaiSecSelectBox.selectedItem():
            selected = self.xenomaiSecSelectBox.selectedItem().label()
            self.dataUpdate(selected)

    def dataUpdate(self, selected_item):
        for i in self.xenomaiSections.keys():
            if str("_target_"+str(selected_item)) in i:
                self.xenomaiRightStatusName.setText(i.split("config_lire_")[1].split(str("target_"))[1])
                self.xenomaiRightStatusValue.setValue(str(self.xenomaiSections[i]))
        return
        self.xenomaiRightStatusName.setText(str(selected_item))
        self.xenomaiRightStatusVersion.setText(self.xenomaiDict[selected_item]["Version"])
        if selected_item in self.toInstall:
            self.xenomaiRightStatusInstall.setChecked(True)
        else:
            self.xenomaiRightStatusInstall.setChecked(False)
        self.xenomaiRightDescriptionOutSummary.setText(self.xenomaiDict[selected_item]["Summary"])
        self.xenomaiRightDescriptionOutDescription.setText(self.xenomaiDict[selected_item]["Description"])

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
        self.xenomaiSections[mySec] = self.xenomaiRightStatusValue.value()
        self.xenomaiRightStatusValue.value()
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
            self.event = self.xenomaiDialog.waitForEvent()
            #self.xenomaiRightDescriptionOutDescription.setText(str(self.event.eventType()))
            if self.event.eventType == yui.YEvent.KeyEvent:
                #
                # ncurses
                if self.event.widget == self.xenomaiCatSelectBox:
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
                    self.xenomaiDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    #
                    # destroy for test
                    self.xenomaiDialog.destroy()
                    return self.stateDict, self.configDictOrig
                return self.stateDict, self.configDictOrig
            #
            # category selected
            if self.event.widget() == self.xenomaiCatSelectBox:
                # 
                # read Input ...
                self.evalInput()
                #
                # todo: dependency resolution
                #self.resolveDependency()
                #
                # update right frame / checkboxes
                self.secUpdate(self.xenomaiCatSelectBox.selectedItem())
                self.oldCategory = self.xenomaiCatSelectBox.selectedItem()
                self.oldSec = self.xenomaiSecSelectBox.selectedItem()
            #
            # pkg selected
            if self.event.widget() == self.xenomaiSecSelectBox:
                # 
                # read selected boxes ...
                self.evalInput()
                self.dataUpdate(self.xenomaiSecSelectBox.selectedItem().label())
                self.oldSec = self.xenomaiSecSelectBox.selectedItem()
            #
            # cancel
            if self.event.widget() == self.xenomaiButtonCancel:
                if self.parent:
                    #
                    # return to parent and return old values
                    self.xenomaiDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    #
                    # destroy for test
                    self.xenomaiDialog.destroy()
                    return self.stateDict, self.configDictOrig
            #
            # next
            if self.event.widget() == self.xenomaiButtonNext:
                # TODO:  fetch values into configdict
                self.evalInput()
                # statedict
                self.stateDict["XENOMAI_DONE"] = 1
                self.stateDict["ERWEITERT"] = 1
                if self.parent:
                    self.xenomaiDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDict
                else:
                    self.xenomaiDialog.destroy()
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
    configdict["lire_target"]["cat_xenomai"] = "rtnet,rack"
    configdict["lire_target"]["config_lire_rack_prereq"] = ""
    configdict["lire_target"]["config_lire_rack_target_tims_router_log_level"] = "0"
    configdict["lire_target"]["config_lire_rtnet_prereq"] = ""
    configdict["lire_target"]["config_lire_rtnet_target_autostart"] = "None"
    
    MY_GUI = GUI_xenomai(factory, None, statedict, configdict)
    statedict, configdict = MY_GUI.handleEvent()


    print "statedict"
    print "#########"
    print statedict
    print ""
    print "configdict"
    print "##########"    
    print configdict
    print ""
