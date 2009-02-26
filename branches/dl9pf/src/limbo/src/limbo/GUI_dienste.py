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
# GUI_dienste.py
# Ask for the dienste options
"""GUI_xenomai - popup window for 'dienste' options"""
###########
# imports #
###########
import yui                  # GUI
import GUI_warning_popup    # popup

######################
# class GUI_software #
######################
class GUI_dienste(object):
    """ GUI_dienste(myFactory, myParent, myStateDict, myConfigDict), returns stateDict, configDict
    
    GUI_xenomai - popup window for 'dienste' options
    
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
        self.diensteDialog = self.factory.createMainDialog()
        #
        # generate categories and sections
        self.diensteCategories = ["Dienste",] #str(self.configDict["lire_target"]["cat_dienste"])
        self.diensteSections = {} # diensteSections[ITEM] = 
        x = self.configDict["lire_target"].copy()
        #
        # iterate over all config-values
        for i in x.keys():
            #
            # for all items i should work with
            # j part of i ?
            if str("config_lire_target_").lower() in i:
                #print i
                self.diensteSections[i] = self.configDict["lire_target"][i]
            if str("config_lire_prereq").lower() in i:
                #print i
                self.diensteSections[i] = self.configDict["lire_target"][i]
        #
        # check and handle "PREREQ" (software)
        for k in self.diensteSections.keys():
            if "prereq" in k:
                # PREREQ SECTION, remove it
                myprereq = str(self.diensteSections.pop(k)).split(",")
                print myprereq
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
        self.diensteMainVBox = self.factory.createVBox(self.diensteDialog)
        #
        # HBox
        self.diensteMainHBox = self.factory.createHBox(self.diensteMainVBox)
        self.diensteMainHBox.setStretchable(1,True)
        self.diensteMainHBox.setWeight(1,100)
        #
        # cat
        # minsize
        self.diensteCatSelectMinSize = self.factory.createMinSize(self.diensteMainHBox, 15, 15)
        # selectbox for category
        self.diensteCatSelectBox = self.factory.createSelectionBox(self.diensteCatSelectMinSize, "K&ategorien")
        self.diensteCatSelectBox.setWeight(0,50) # 0 = horiz
        self.diensteCatSelectBox.setStretchable(0,True)
        #self.diensteCatSelectBox.setWeight(1,25)
        #self.diensteCatSelectBox.setStretchable(1,True)
        self.diensteCatSelectBox.setNotify()
        self.diensteCatSelectBox.setImmediateMode()
        self.diensteCatSelectBox.setSendKeyEvents(True)
        #
        # sec
        # minsize
        self.diensteSecSelectMinSize = self.factory.createMinSize(self.diensteMainHBox, 30, 15)
        # selectbox for sec
        self.diensteSecSelectBox =  self.factory.createSelectionBox(self.diensteSecSelectMinSize, "&Optionen")
        self.diensteSecSelectBox.setWeight(0,50)
        self.diensteSecSelectBox.setStretchable(0,True)
        #self.diensteSecSelectBox.setWeight(1,20)
        #self.diensteSecSelectBox.setStretchable(1,True)
        self.diensteSecSelectBox.setNotify()
        self.diensteSecSelectBox.setImmediateMode()
        self.diensteCatSelectBox.setSendKeyEvents(True)
        #
        # right HBox
        self.diensteRightVBox = self.factory.createVBox(self.diensteMainHBox)
        self.diensteRightVBox.setWeight(0,10)
        self.diensteRightVBox.setStretchable(0, True)
        self.diensteRightVBox.setStretchable(1, True)
        self.diensteRightVBox.setWeight(1,10)
        #
        # replacepoint 1
        self.diensteRightStatusFrame = self.factory.createFrame(self.diensteRightVBox, "Wert")
        self.diensteRightStatusFrame.setWeight(0,100)
        self.diensteRightStatusFrame.setWeight(1,30)
        self.diensteRightStatusFrame.setStretchable(0, True)
        self.diensteRightStatusFrame.setStretchable(1, True)
        self.diensteRightReplacePoint1 = self.factory.createReplacePoint(self.diensteRightStatusFrame)
        self.diensteRightReplacePoint1.setWeight(0,100)
        self.diensteRightReplacePoint1.setStretchable(0, True)
        self.diensteRightReplacePoint1.setStretchable(1, True)
        #
        # dummy widgets for replacepoint1
        self.diensteRightVBox1 = self.factory.createVBox(self.diensteRightReplacePoint1)
        self.diensteRightVBox1.setWeight(0,100)
        self.diensteRightVBox1.setWeight(1,10)
        self.diensteRightVBox1.setStretchable(0, True)
        self.diensteRightVBox1.setStretchable(1, True)
        self.diensteRightHBox1 = self.factory.createHBox(self.diensteRightVBox1)
        self.diensteRightHBox1.setWeight(0,100)
        self.diensteRightHBox1.setWeight(1,100)
        self.diensteRightHBox1.setStretchable(0, True)
        self.diensteRightHBox1.setStretchable(1, True)
        self.diensteRightStatusNameLabel = self.factory.createLabel(self.diensteRightHBox1, "Name:")
        self.diensteRightStatusName = self.factory.createLabel(self.diensteRightHBox1, "Foo")
        self.diensteRightStatusName.setStretchable(0,True)
        self.diensteRightStatusValue = self.factory.createInputField(self.diensteRightVBox1, "Wert")
        self.diensteRightStatusValue.setStretchable(0,True)
        self.diensteRightStatusValue.setNotify(True)
        #
        # replacepoint 2
        self.diensteRightDescriptionFrame = self.factory.createFrame(self.diensteRightVBox, "Beschreibung")
        self.diensteRightDescriptionFrame.setWeight(0,100)
        self.diensteRightDescriptionFrame.setWeight(1,90)
        self.diensteRightDescriptionFrame.setStretchable(0, True)
        self.diensteRightDescriptionFrame.setStretchable(1, True)
        self.diensteRightReplacePoint2 = self.factory.createReplacePoint(self.diensteRightDescriptionFrame)
        self.diensteRightReplacePoint2.setStretchable(0, True)
        self.diensteRightReplacePoint2.setStretchable(1, True)
        self.diensteRightVBox2 = self.factory.createVBox(self.diensteRightReplacePoint2)
        self.diensteRightDescriptionOutDescription = self.factory.createRichText(self.diensteRightVBox2, "Beschreibung")
        self.diensteRightDescriptionOutDescription.setPlainTextMode(True)
        self.diensteRightDescriptionOutDescription.setText("")
        
        #
        # bottom
        self.diensteBottomHBox = self.factory.createHBox(self.diensteMainVBox)
        #
        # help
        self.diensteBottomHBox_left = self.factory.createLeft(self.diensteBottomHBox)
        self.diensteButtonHelp = self.factory.createPushButton(self.diensteBottomHBox_left, "&Hilfe")
        self.diensteBottomHBoxRight = self.factory.createRight(self.diensteBottomHBox)
        self.diensteBottomHBoxRight_hbox = self.factory.createHBox(self.diensteBottomHBox)
        #
        # Add item
        self.diensteButtonAdd = self.factory.createPushButton(self.diensteBottomHBoxRight_hbox, "H&inzufügen")
        #
        # Remove item
        self.diensteButtonRemove = self.factory.createPushButton(self.diensteBottomHBoxRight_hbox, "&Entfernen")
        #
        # cancel
        self.diensteButtonCancel = self.factory.createPushButton(self.diensteBottomHBoxRight_hbox, "&Zurück")
        #
        # next
        self.diensteButtonNext = self.factory.createPushButton(self.diensteBottomHBoxRight_hbox, "&Weiter")
        #
        # add categories
        tosort = []
        for i in self.diensteCategories:
            tosort.append(i)
        tosort.sort()
        for i in tosort:
            self.diensteCatSelectBox.addItem(i)
        del i
        del tosort
        #
        # update checkbox
        self.secUpdate(self.diensteCatSelectBox.selectedItem())
        #
        # update "last" category
        self.oldCategory = self.diensteCatSelectBox.selectedItem()
        #
        # update pkg display area
        if self.diensteSecSelectBox.selectedItem():
            self.dataUpdate(self.diensteSecSelectBox.selectedItem().label())
        #
        # update "last" pkg
        self.oldSec = self.diensteSecSelectBox.selectedItem()
        #
        # recalc the layout
        self.diensteDialog.recalcLayout()
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
        self.diensteSecSelectBox.deleteAllItems()
        #
        # iterate over names in self.diensteCategories
        mylist = []
        for i in self.diensteSections.keys():
            if str("config_lire"+"_target_") in i:
                k = str(i).split("config_lire"+"_target_")[1]
                mylist.append(str(k))
        # sort it
        mylist.sort()
        for k in mylist:    
            self.diensteSecSelectBox.addItem(str(k))
        self.appl.redrawScreen() # redraw
        if self.diensteSecSelectBox.selectedItem():
            selected = self.diensteSecSelectBox.selectedItem().label()
            self.dataUpdate(selected)

    def dataUpdate(self, selected_item):
        for i in self.diensteSections.keys():
            if str("_target_"+str(selected_item)) in i:
                print i
                self.diensteRightStatusName.setText(i.split("config_lire_target_")[1])
                self.diensteRightStatusValue.setValue(str(self.diensteSections[i]))
        return
        self.diensteRightStatusName.setText(str(selected_item))
        self.diensteRightStatusVersion.setText(self.diensteDict[selected_item]["Version"])
        if selected_item in self.toInstall:
            self.diensteRightStatusInstall.setChecked(True)
        else:
            self.diensteRightStatusInstall.setChecked(False)
        self.diensteRightDescriptionOutSummary.setText(self.diensteDict[selected_item]["Summary"])
        self.diensteRightDescriptionOutDescription.setText(self.diensteDict[selected_item]["Description"])

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
        mySec = "config_lire_target_"+str(secLabel)
        print mySec
        self.diensteSections[mySec] = self.diensteRightStatusValue.value()
        self.diensteRightStatusValue.value()
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
            self.event = self.diensteDialog.waitForEvent()
            #self.diensteRightDescriptionOutDescription.setText(str(self.event.eventType()))
            if self.event.eventType == yui.YEvent.KeyEvent:
                #
                # ncurses
                if self.event.widget == self.diensteCatSelectBox:
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
                    self.diensteDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    #
                    # destroy for test
                    self.diensteDialog.destroy()
                    return self.stateDict, self.configDictOrig
                return self.stateDict, self.configDictOrig
            #
            # category selected
            if self.event.widget() == self.diensteCatSelectBox:
                # 
                # read Input ...
                self.evalInput()
                #
                # todo: dependency resolution
                #self.resolveDependency()
                #
                # update right frame / checkboxes
                self.secUpdate(self.diensteCatSelectBox.selectedItem())
                self.oldCategory = self.diensteCatSelectBox.selectedItem()
                self.oldSec = self.diensteSecSelectBox.selectedItem()
            #
            # pkg selected
            if self.event.widget() == self.diensteSecSelectBox:
                # 
                # read selected boxes ...
                self.evalInput()
                self.dataUpdate(self.diensteSecSelectBox.selectedItem().label())
                self.oldSec = self.diensteSecSelectBox.selectedItem()
            #
            # cancel
            if self.event.widget() == self.diensteButtonCancel:
                if self.parent:
                    #
                    # return to parent and return old values
                    self.diensteDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    #
                    # destroy for test
                    self.diensteDialog.destroy()
                    return self.stateDict, self.configDictOrig
            #
            # next
            if self.event.widget() == self.diensteButtonNext:
                # TODO:  fetch values into configdict
                self.evalInput()
                # statedict
                self.stateDict["DIENSTE_DONE"] = 1
                self.stateDict["READY"] = 1
                if self.parent:
                    self.diensteDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDict
                else:
                    self.diensteDialog.destroy()
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
    configdict["lire_target"]["cat_dienste"] = "config_lire_target_,"
    configdict["lire_target"]["config_lire_prereq"] = ""
    configdict["lire_target"]["config_lire_target_tims_router_log_level"] = "0"
    configdict["lire_target"]["config_lire_target_autostart"] = "None"
    
    MY_GUI = GUI_dienste(factory, None, statedict, configdict)
    statedict, configdict = MY_GUI.handleEvent()


    print "statedict"
    print "#########"
    print statedict
    print ""
    print "configdict"
    print "##########"    
    print configdict
    print ""
