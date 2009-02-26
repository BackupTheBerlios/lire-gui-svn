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
# GUI_repository.py
# Ask for the repositories
"""GUI_software - popup window for software selection"""
###########
# imports #
###########
import yui                  # GUI
import GUI_warning_popup    # popup
#import GUI_software_select

######################
# class GUI_software #
######################
class GUI_software(object):
    """ GUI_software(myFactory, myParent, myStateDict, myConfigDict), returns stateDict, configDict
    
    GUI_software - popup window for software selection
    
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
        self.toInstall = []
        self.mandatory = []
        self.error = False
        self.errormsg = None
        self.oldCategory = None  # last active category
        #
        # already selected software
        if not self.configDict.has_key("soft_to_install"):
            self.toInstall = []
        else:
            self.toInstall = self.configDict["soft_to_install"]
        #
        # variable declarations 
        self.event = None
        self.softwareCategories = {} 
        self.softwareDict = {}
        if not self.configDict.has_key("softwareDict"):
            #
            # without software (repositories) no choice
            # huh, we have no software to select from ?!?!
            # popup and exit
            self.errormsg = str(u"Fehler!\nKeine Softwarepakete bekannt.\nÜberprüfen Sie die Repositories!".encode("utf-8"))
            #WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.parent, msg) needs to be done later!
            #WARNING_URL_GUI.handleEvent()
            self.stateDict["REPOSITORY_DONE"] = 0
            self.error = True
            return #self.stateDict, self.configDictOrig
        else: 
            #  self.configDict["softwareDict"] available
            #
            # import known software
            self.softwareDict = self.configDict["softwareDict"]
        #
        # mandatory software ?!
        if not self.configDict.has_key("defaultinstalledsoft"):
            #
            # no mandatory software ?!
            pass
        else:
            self.mandatory = self.configDict["defaultinstalledsoft"]
            #
            # update self.toInstall
            x = set(self.toInstall)
            x.update(set(self.mandatory))
            self.toInstall = x
        #
        # after check ... 
        self.softwareDialog = self.factory.createMainDialog()
        if self.parent:
            self.softwareDialog.setParent(self.parent)
        #
        # extract "Group" Categories from softwareDict ;)
        list = []
        for i in self.softwareDict.keys():
            list.append(self.softwareDict[i]["Group"])
        list.sort()
        #
        # remove HIDDEN category
        if "HIDE" in list:
            list.remove("HIDE")
        for i in list:
            self.softwareCategories[i]=[]
            for j in self.softwareDict.keys():
                if self.softwareDict[j]["Group"] == i:
                    self.softwareCategories[i].append(j)
            self.softwareCategories[i].sort()
            
        #TODO: handle dependencies ! need to be done with zypper
        #
        # construct gui
        #
        # ###################
        # #     #     # [x] #
        # #  c  #  p  # ver #
        # #  a  #  k  #######
        # #  t  #  g  # de  #
        # #     #     #  sc #
        # ###################
        # # <>         <> <>#
        # ###################
        #
        # VBox
        self.softwareMainVBox = self.factory.createVBox(self.softwareDialog)
        #
        # HBox
        self.softwareMainHBox = self.factory.createHBox(self.softwareMainVBox)
        self.softwareMainHBox.setStretchable(1,True)
        self.softwareMainHBox.setWeight(1,100)
        #
        # cat
        # minsize
        self.softwareCatSelectMinSize = self.factory.createMinSize(self.softwareMainHBox, 15, 15)
        # selectbox for category
        self.softwareCatSelectBox = self.factory.createSelectionBox(self.softwareCatSelectMinSize, "K&ategorien")
        self.softwareCatSelectBox.setWeight(0,50) # 0 = horiz
        self.softwareCatSelectBox.setStretchable(0,True)
        #self.softwareCatSelectBox.setWeight(1,25)
        #self.softwareCatSelectBox.setStretchable(1,True)
        self.softwareCatSelectBox.setNotify()
        self.softwareCatSelectBox.setImmediateMode()
        self.softwareCatSelectBox.setSendKeyEvents(True)
        #
        # pkg
        # minsize
        self.softwarePkgSelectMinSize = self.factory.createMinSize(self.softwareMainHBox, 25, 15)
        # selectbox for pkg
        self.softwarePkgSelectBox =  self.factory.createSelectionBox(self.softwarePkgSelectMinSize, "&Pakete")
        self.softwarePkgSelectBox.setWeight(0,50)
        self.softwarePkgSelectBox.setStretchable(0,True)
        #self.softwarePkgSelectBox.setWeight(1,20)
        #self.softwarePkgSelectBox.setStretchable(1,True)
        self.softwarePkgSelectBox.setNotify()
        self.softwarePkgSelectBox.setImmediateMode()
        #self.softwareCatSelectBox.setSendKeyEvents(True)
        #
        # right HBox
        self.softwareRightVBox = self.factory.createVBox(self.softwareMainHBox)
        self.softwareRightVBox.setWeight(0,10)
        self.softwareRightVBox.setStretchable(0, True)
        self.softwareRightVBox.setStretchable(1, True)
        self.softwareRightVBox.setWeight(1,10)
        #
        # replacepoint 1
        self.softwareRightStatusFrame = self.factory.createFrame(self.softwareRightVBox, "Version/Status")
        self.softwareRightStatusFrame.setWeight(0,100)
        self.softwareRightStatusFrame.setWeight(1,30)
        self.softwareRightStatusFrame.setStretchable(0, True)
        self.softwareRightStatusFrame.setStretchable(1, True)
        self.softwareRightReplacePoint1 = self.factory.createReplacePoint(self.softwareRightStatusFrame)
        self.softwareRightReplacePoint1.setWeight(0,100)
        self.softwareRightReplacePoint1.setStretchable(0, True)
        self.softwareRightReplacePoint1.setStretchable(1, True)
        #
        # dummy widgets for replacepoint1
        self.softwareRightVBox1 = self.factory.createVBox(self.softwareRightReplacePoint1)
        self.softwareRightVBox1.setWeight(0,100)
        self.softwareRightVBox1.setWeight(1,10)
        self.softwareRightVBox1.setStretchable(0, True)
        self.softwareRightVBox1.setStretchable(1, True)
        self.softwareRightHBox1 = self.factory.createHBox(self.softwareRightVBox1)
        self.softwareRightHBox1.setWeight(0,100)
        self.softwareRightHBox1.setWeight(1,10)
        self.softwareRightHBox1.setStretchable(0, True)
        self.softwareRightHBox1.setStretchable(1, True)
        self.softwareRightStatusNameLabel = self.factory.createLabel(self.softwareRightHBox1, "Name:")
        self.softwareRightStatusName = self.factory.createLabel(self.softwareRightHBox1, "Foo")
        self.softwareRightStatusName.setStretchable(0,True)
        self.softwareRightHBox2 = self.factory.createHBox(self.softwareRightVBox1)
        self.softwareRightHBox2.setWeight(0,100)
        self.softwareRightHBox2.setWeight(1,10)
        self.softwareRightHBox2.setStretchable(0, True)
        self.softwareRightHBox2.setStretchable(1, True)
        self.softwareRightStatusVersionLabel = self.factory.createLabel(self.softwareRightHBox2, "Version:")
        self.softwareRightStatusVersion = self.factory.createLabel(self.softwareRightHBox2, "1.1.1b1" )
        self.softwareRightStatusVersion.setStretchable(0,True)
        self.softwareRightStatusInstallLeft = self.factory.createLeft(self.softwareRightVBox1)
        self.softwareRightStatusInstall = self.factory.createCheckBox(self.softwareRightStatusInstallLeft, "Installieren")
        self.softwareRightStatusInstall.setNotify()
        #
        # replacepoint 2
        self.softwareRightDescriptionFrame = self.factory.createFrame(self.softwareRightVBox, "Beschreibung")
        self.softwareRightDescriptionFrame.setWeight(0,100)
        self.softwareRightDescriptionFrame.setWeight(1,90)
        self.softwareRightDescriptionFrame.setStretchable(0, True)
        self.softwareRightDescriptionFrame.setStretchable(1, True)
        self.softwareRightReplacePoint2 = self.factory.createReplacePoint(self.softwareRightDescriptionFrame)
        self.softwareRightReplacePoint2.setStretchable(0, True)
        self.softwareRightReplacePoint2.setStretchable(1, True)
        self.softwareRightVBox2 = self.factory.createVBox(self.softwareRightReplacePoint2)
        self.softwareRightDescriptionOutSummary = self.factory.createRichText(self.softwareRightVBox2, "Paketübersicht")
        self.softwareRightDescriptionOutSummary.setPlainTextMode(True)
        self.softwareRightDescriptionOutSummary.setText("Summary")        
        self.softwareRightDescriptionOutDescription = self.factory.createRichText(self.softwareRightVBox2, "Paketdarstellung")
        self.softwareRightDescriptionOutDescription.setPlainTextMode(True)
        self.softwareRightDescriptionOutDescription.setText("Description")
        
        #
        # bottom
        self.softwareBottomHBox = self.factory.createHBox(self.softwareMainVBox)
        #
        # help
        self.softwareBottomHBox_left = self.factory.createLeft(self.softwareBottomHBox)
        self.softwareButtonHelp = self.factory.createPushButton(self.softwareBottomHBox_left, "&Hilfe")
        self.softwareBottomHBoxRight = self.factory.createRight(self.softwareBottomHBox)
        self.softwareBottomHBoxRight_hbox = self.factory.createHBox(self.softwareBottomHBox)
        #
        # cancel
        self.softwareButtonCancel = self.factory.createPushButton(self.softwareBottomHBoxRight_hbox, "Zurück")
        #
        # next
        self.softwareButtonNext = self.factory.createPushButton(self.softwareBottomHBoxRight_hbox, "&Weiter")
        #
        # add categories
        for i in self.softwareCategories.keys():
            self.softwareCatSelectBox.addItem(i)
        #
        # update checkbox
        self.pkgUpdate(self.softwareCatSelectBox.selectedItem())
        #
        # update "last" category
        self.oldCategory = self.softwareCatSelectBox.selectedItem()
        #
        # update pkg display area
        if self.softwarePkgSelectBox.selectedItem():
            self.dataUpdate(self.softwarePkgSelectBox.selectedItem().label())
        #
        # update "last" pkg
        self.oldPkg = self.softwarePkgSelectBox.selectedItem()
        #
        # recalc the layout
        self.softwareDialog.recalcLayout()
#===============================================================================


    #############
    # functions #
    #############
    def checkAvail(self):
        #
        # check if all mandatory software is available
        remaining = set(self.mandatory)
        available = []
        if self.stateDict["REPOSITORY_DONE"] == 0:
            self.errormsg = str(u"Fehler!\nÜberprüfen Sie die Repositories!\n".encode("utf-8"))
            self.error = True
            return
        for i in self.softwareCategories.keys():
            for j in self.softwareCategories[i]:
                if j in remaining:
                    remaining.remove(j)
        if not remaining.__len__() == 0:
            # missing mandatory software !
            txt = ""
            for i in remaining:
                txt = str(txt)+" "+str(i)
            self.errormsg = str(u"Fehler!\nEines oder mehrere obligatorische Softwarepakete konnten in\nden Paketquellen nicht gefunden werden.\nÜberprüfen Sie die Repositories!\nPakete: %s".encode("utf-8")) % txt
            self.stateDict["REPOSITORY_DONE"] = 0
            self.error = True
            return #self.stateDict, self.configDictOrig

    def pkgUpdate(self, selected_item):
        """update the checkbox frame
        """
        #
        # label of the selected category
        label = selected_item.label()
        #
        # delete the old items
        self.softwarePkgSelectBox.deleteAllItems()
        #
        # iterate over packagenames
        for i in self.softwareCategories[label]:
            self.softwarePkgSelectBox.addItem(i)
        self.appl.redrawScreen() # redraw
        if self.softwarePkgSelectBox.selectedItem():
            selected = self.softwarePkgSelectBox.selectedItem().label()
            self.dataUpdate(selected)

    def dataUpdate(self, selected_item):
        self.softwareRightStatusName.setText(str(selected_item))
        self.softwareRightStatusVersion.setText(self.softwareDict[selected_item]["Version"])
        if selected_item in self.toInstall:
            self.softwareRightStatusInstall.setChecked(True)
        else:
            self.softwareRightStatusInstall.setChecked(False)
        self.softwareRightDescriptionOutSummary.setText(self.softwareDict[selected_item]["Summary"])
        self.softwareRightDescriptionOutDescription.setText(self.softwareDict[selected_item]["Description"])

        self.appl.redrawScreen()
    
    def evalChecked(self):
        """evaluate checked/unchecked boxes
        """
        pass
        tmp = []
        catLabel = self.oldCategory.label()  # category to evaluate
        pkgLabel = self.oldPkg.label()
        #
        # checked -> add to install
        if self.softwareRightStatusInstall.isChecked():
            tmp.append(pkgLabel)
            tmp2 = set(tmp)
            tmp2.update(set(self.toInstall))
            self.toInstall = tmp2
        #
        # unchecked
        else:
            if pkgLabel in self.toInstall:
                if pkgLabel in self.mandatory:
                    #
                    # nag about "Cant remove mandatory software"
                    msg = str(u"Fehler!\nDas Paket %s ist zwingend erforderlich.\nAbwahl nicht möglich!".encode("utf-8")) %  pkgLabel
                    WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.parent, msg)
                    WARNING_URL_GUI.handleEvent()
                    #
                    # will be checked on next reload, just handle direct checkbox click
                    if self.event.widget() == self.softwareRightStatusInstall:
                        self.softwareRightStatusInstall.setChecked(True)
                else:
                    #
                    # deselect
                    self.toInstall.remove(pkgLabel)
        
    def resolveDependency(self):
        """Dependency resolver
        """    
        pass # nothing up to now - kiwi does resolve later
        
    #############
    # eventloop #
    #############
    def handleEvent(self):
        """Event loop
        """
        self.checkAvail()
        if self.error:
            # bail out (from "no software/repo" screen)
            if self.errormsg:
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, None, self.errormsg) 
                WARNING_URL_GUI.handleEvent()
                if self.parent:
                    #
                    # return to parent and return old values
                    self.softwareDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
            else:
                #
                # destroy for test
                self.softwareDialog.destroy()
                return self.stateDict, self.configDictOrig
        while True:
            #
            # get event
            self.event = self.softwareDialog.waitForEvent()


            #self.softwareRightDescriptionOutDescription.setText(str(self.event.eventType()))
            if self.event.eventType == yui.YEvent.KeyEvent:
                #
                # ncurses
                if self.event.widget == self.softwareCatSelectBox:
                    #
                    # possibly change to pkgselectbox if rightarrow
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
                    self.softwareDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    #
                    # destroy for test
                    self.softwareDialog.destroy()
                    return self.stateDict, self.configDictOrig
                return self.stateDict, self.configDictOrig
            #
            # category selected
            if self.event.widget() == self.softwareCatSelectBox:
                # 
                # read selected boxes ...
                self.evalChecked()
                #
                # todo: dependency resolution
                #self.resolveDependency()
                #
                # update right frame / checkboxes
                self.pkgUpdate(self.softwareCatSelectBox.selectedItem())
                self.oldCategory = self.softwareCatSelectBox.selectedItem()
                self.oldPkg = self.softwarePkgSelectBox.selectedItem()
            #
            # pkg selected
            if self.event.widget() == self.softwarePkgSelectBox:
                # 
                # read selected boxes ...
                if self.oldPkg == self.softwarePkgSelectBox.selectedItem():
                    if self.softwareRightStatusInstall.isChecked():
                        self.softwareRightStatusInstall.setChecked(False)
                    else:
                        self.softwareRightStatusInstall.setChecked(True)
                self.evalChecked()
                self.dataUpdate(self.softwarePkgSelectBox.selectedItem().label())
                self.oldPkg = self.softwarePkgSelectBox.selectedItem()
            #
            # checkbox
            if self.event.widget() == self.softwareRightStatusInstall:
                self.evalChecked()
                
            #
            # cancel
            if self.event.widget() == self.softwareButtonCancel:
                if self.parent:
                    #
                    # return to parent and return old values
                    self.softwareDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    #
                    # destroy for test
                    self.softwareDialog.destroy()
                    return self.stateDict, self.configDictOrig
            #
            # next
            if self.event.widget() == self.softwareButtonNext:
                # TODO:  fetch values into configdict
                self.evalChecked()
                self.configDict["soft_to_install"] = set(self.toInstall)
                self.stateDict["SOFTWARE_DONE"] = 1
                self.stateDict["XENOMAI"] = 1
                if self.parent:
                    self.softwareDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDict
                else:
                    self.softwareDialog.destroy()
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
    
    MY_GUI = GUI_software(factory, None, statedict, configdict)
    statedict, configdict = MY_GUI.handleEvent()


    print "statedict"
    print "#########"
    print statedict
    print ""
    print "configdict"
    print "##########"    
    print configdict
    print ""
    print "softwaredict"
    print "############"
    print configdict["softwareDict"]
    print ""
    print "soft_to_install"
    print "#########"
    print configdict["soft_to_install"]   











# OLD GARBAGE
#===============================================================================
# 
# 
#    def test(self):
#        self.software_select_checkboxframe = self.factory.createFrame(self.software_select_hbox, "Auswahl")
#        self.software_select_checkboxframe.setWeight(0,80)
#        self.software_select_checkboxframe.setWeight(1,80)
#        self.software_select_checkboxframe.setStretchable(1,True)
#        self.software_select_checkboxframe.setStretchable(0,True)
#        self.software_select_checkboxframe_vbox = self.factory.createVBox(self.software_select_checkboxframe)
#        self.software_select_checkboxframe_vbox2 = self.factory.createVBox(self.software_select_checkboxframe_vbox)
#        self.software_select_checkbox_ = {}
#        self.software_select_checkbox_alignment_ = {}
#        self.checkboxframe_update(self.softwareSelectBox.selectedItem())
#        
#    def checkboxframe_update(self, selected_item):
#        #print "1"
#        label = selected_item.label()
#        self.software_select_checkboxframe_vbox2.deleteChildren()
#        self.software_select_checkboxframe_vbox2_replacepoint = self.factory.createReplacePoint(self.software_select_checkboxframe_vbox2)
#        self.software_select_checkbox_ = {}
#        self.software_select_checkbox_alignment_ = {}
# 
#        for i in self.softwareCategories[label]:
#            #print label
#            #print i
#            self.software_select_checkbox_alignment_[i] = self.factory.createLeft(self.software_select_checkboxframe_vbox2)
#            self.software_select_checkbox_[i] = self.factory.createCheckBox(self.software_select_checkbox_alignment_[i], i)
#            self.software_select_checkbox_[i].setEnabled(True) 
#        self.software_select_checkboxframe_vbox2.setEnabled(True)
#        self.softwareDialog.recalcLayout()
#        appl.redrawScreen()
#===============================================================================
