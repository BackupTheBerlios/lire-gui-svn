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
"""GUI_software - POPUP for software selection"""
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
        self.error = False
        self.oldCategory = None  # last active category
        #
        # already selected software
        if not self.configDict.has_key("soft_to_install"):
            self.toInstall = []
        else:
            self.toInstall = self.configDict["soft_to_install"] 
        self.event = None
        self.softwareCategories = {} 
        self.softwareDict = {}
        self.tableItems_not_ = {}
        self.tableItems_set_ = {}
        if not self.configDict.has_key("softwareDict"):
            #
            # without software (repositories) no choice
            # huh, we have no software to select from ?!?!
            # popup and exit
            msg = str("Fehler!\nKeine Softwarepakete bekannt.\nÜberprüfen Sie die Repositories!")
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.parent, msg)
            WARNING_URL_GUI.handleEvent()
            self.stateDict["REPOSITORY_DONE"] = 0
            self.error = True
            return #self.stateDict, self.configDictOrig
        else: 
            #  self.configDict["softwareDict"] available
            #
            # import known software
            self.softwareDict = self.configDict["softwareDict"]
            #print self.softwareDict
            
        # after check ... 
        self.softwareDialog = self.factory.createMainDialog()
        if self.parent:
            self.softwareDialog.setParent(self.parent)

        #
        # extract Categories from softwareDict ;)
        for i in self.softwareDict.values():
            self.softwareCategories[i]=[]
            for j in self.softwareDict.keys():
                if self.softwareDict[j] == i:
                    self.softwareCategories[i].append(j)
                    self.tableItems_not_[j] = yui.YTableItem("", str(j), "ver", "fasel")  # bug in libyui: all YTableItems must be persistent :(
                    self.tableItems_not_[j].setLabel(str(j))
                    self.tableItems_set_[j] = yui.YTableItem("X", str(j), "ver", "fasel")
                    print str(j)
                    self.tableItems_set_[j].setLabel(str(j)+"+X")
        print "3"
        #TODO: handle dependencies ! need to be done with zypper
        #
        # construct gui
        #
        # VBox
        self.softwareMainVBox = self.factory.createVBox(self.softwareDialog)
        self.softwareMainVBox.setStretchable( 1, True )
        self.softwareMainVBox.setStretchable( 0, True )
        #
        # Frame
        self.softwareMainFrame = self.factory.createFrame(self.softwareMainVBox, "Softwareauswahl")
        self.softwareMainFrame.setWeight(0,80)
        self.softwareMainFrame.setWeight(1,100)
        #         |   |   |
        # HBox    |   |   |
        self.softwareMainHBox = self.factory.createHBox(self.softwareMainFrame)
        #
        # minsize
        self.softwareSelectMinSize = self.factory.createMinSize(self.softwareMainHBox, 10, 8)
        #
        # selectbox for category
        self.softwareSelectBox = self.factory.createSelectionBox(self.softwareSelectMinSize, "K&ategorien")
        self.softwareSelectBox.setWeight(0,10)
        self.softwareSelectBox.setWeight(1,10)
        self.softwareSelectBox.setNotify()
        #
        # Diplay
        self.softwareDisplayFrameSize = self.factory.createMinSize(self.softwareMainHBox, 10, 20)
        self.softwareDisplayFrame = self.factory.createFrame(self.softwareDisplayFrameSize, "&Paketauswahl")
        self.softwareDisplayFrame.setWeight(0,90)
        self.softwareDisplayFrame.setWeight(1,90)
        self.softwareDisplayFrame.setStretchable( 1, True )
        self.softwareDisplayFrame.setStretchable( 0, True )
        #
        # replacepoint
        # dynamic list for software_items (updated later - checkboxframe_update) -
#        self.software_select_checkboxframe_vbox2_replacepoint = self.factory.createReplacePoint(self.softwareDisplayFrame)
#        self.software_select_checkboxframe_vbox2 = self.factory.createVBox(self.software_select_checkboxframe_vbox2_replacepoint)
        # table header 
        self.yTableHeader = yui.YTableHeader()
        self.yTableHeader.addColumn("Selected")
        self.yTableHeader.addColumn("Name")
        self.yTableHeader.addColumn("Version")
        self.yTableHeader.addColumn("Description")
        self.myTableMinSize = self.factory.createMinSize(self.softwareDisplayFrame, 50, 12)
        self.myTableReplace = self.factory.createReplacePoint(self.myTableMinSize)
        self.myTable = self.factory.createTable(self.myTableReplace, self.yTableHeader, True)
        self.myTable.setNotify(True)

        #
        # bottom
        self.softwareBottomHBox = self.factory.createHBox(self.softwareMainVBox)
        self.softwareBottomHBox.setWeight(0,10)
        self.softwareBottomHBox.setWeight(1,10)
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
        self.softwareButtonNext = self.factory.createPushButton(self.softwareBottomHBoxRight_hbox, "Fertig")
        #
        # add categories
        for i in self.softwareCategories.keys():
            self.softwareSelectBox.addItem(i)
        self.software_select_item_ = {}
        #
        # update checkbox
        print "2"
        self.checkboxframe_update(self.softwareSelectBox.selectedItem())
        print "2a"
        #
        # update "last" category
        self.oldCategory = self.softwareSelectBox.selectedItem()
        #
        # recalc the layout
        self.softwareDialog.recalcLayout()



    #############
    # functions #
    #############
    def checkboxframe_update(self, selected_item):
        """update the checkbox frame
        """
        #
        # label of the selected category
        print "1"
        self.myTableReplace.startMultipleChanges()
        label = selected_item.label()
#        if self.myTable.hasItems():
#            self.myTable.clearAllItems()
        #
        # iterate over packagenames
#        for i in self.softwareCategories[label]:
#            self.myTable.addItem(self.tableItems_not_[i])

#        self.myTable.deselectAllItems()
#        for i in self.softwareCategories[label]:
#            if i in self.toInstall:
#                self.myTable.selectItem(self.tableItems_not_[i])

        self.myTableReplace.doneMultipleChanges()
        self.appl.redrawScreen() # redraw
    
    def evalChecked(self):
        """evaluate checked/unchecked boxes
        """
        return # needs rewrite for table !!
#===============================================================================
#    
#        tmp = []
#        label = self.oldCategory.label()  # category to evaluate
#        #
#        # iterate software in list
#        for i in self.softwareCategories[label]:
#            #
#            # -> checked
#            if self.software_select_checkbox_[i].isChecked():
#                tmp.append(i)
#                tmp2 = set(tmp)
#                tmp2.update(set(self.toInstall))
#                self.toInstall = tmp2
#            #
#            # unchecked
#            else:
#                if i in self.toInstall:
#                    self.toInstall.remove(i)
#===============================================================================
        
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
        if self.error:
            # bail out (from "no software/repo" screen)
            return self.stateDict, self.configDictOrig
        while True:
            #
            # get event
            self.event = self.softwareDialog.waitForEvent()
            print self.event.widget()
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
            if self.event.widget() == self.softwareSelectBox:
                # 
                # read selected boxes ...
                self.evalChecked()
                #
                # todo: dependency resolution
                self.resolveDependency()
                #
                # update right frame / checkboxes
                self.checkboxframe_update(self.softwareSelectBox.selectedItem())
                self.oldCategory = self.softwareSelectBox.selectedItem()
            #
            # tableItem selected
            if self.event.widget() == self.myTable:
                selected = self.myTable.selectedItem()
                print selected.label()
#                if self.myTable.hasSelectedItem():
#                    print self.myTable.selectedItems()
#                    if not selected in self.myTable.selectedItems():
#                        self.myTable.selectItem(selected, True)
#                    else:
#                        self.myTable.selectItem(selected, False)
                continue
                #if self.tableItems_not_[]
                pass
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
    softwaredict = {'openssl-doc': 'Productivity', 'libopenssl0_9_8': 'Productivity', 'libdc1394-22': 'Hardware', 'libpng12-0': 'System', 'ed': 'Productivity', 'libraw1394-devel': 'Development'}
    configdict["softwareDict"] = softwaredict
    configdict["toInstall"] = ["openssl-doc", ]
    
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
    print "toInstall"
    print "#########"
    print configdict["toInstall"]   
