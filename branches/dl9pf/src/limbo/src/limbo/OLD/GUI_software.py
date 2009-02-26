#coding:utf-8
import yui
import locale
import GUI_software_select
locale.setlocale(locale.LC_ALL, "")

appl = yui.YUI.application()

class GUI_software(object):
    def __init__(self, myFactory, myParent, myStateDict, myConfigDict):
        self.factory = myFactory
        self.stateDict = myStateDict.copy()
        self.configDictOrig = myConfigDict.copy()
        self.configDict = myConfigDict.copy()
        self.parent = myParent
        self.event = None

        #construct gui
        self.softwareDialog = self.factory.createPopupDialog()
        if self.parent:
            self.softwareDialog.setParent(self.parent)
        self.softwareCategories = {} 
        #["Libraries", "System", "Netzwerk", "Realtime", "SELinux"]
        #self.softwareItems_libraries = ["opencv", "openvpn", "openssh", "openssl", "nano", "gdb", "wireless-tools", "madwifi", "RTNet", "USB4RT", "SPCA5xx", "Stereo-CAM", "RACK", "RACK_RTS", "libstdc++", "libdc1394", "libraw1394", "libjpeg", "libpng", "zlib", "libsepol", "libselinux", "policycoreutils", "policy"]
#        self.softwareCategories["Libraries"]=["libstdc++", "libdc1394", "libraw1394", "libjpeg", "libpng", "zlib"]
#        self.softwareCategories["System"]=["opencv", "openvpn", "openssh", "openssl", "nano", "gdb"]
#        self.softwareCategories["Netzwerk"]=["wireless-tools", "madwifi"]
#        self.softwareCategories["Realtime"]=["RTNet", "USB4RT", "SPCA5xx", "Stereo-CAM", "RACK", "RACK_RTS"]
#        self.softwareCategories["SELinux"]=["libsepol", "libselinux", "policycoreutils", "policy"]

        self.softwareDict = self.configDict["softwareDict"]
        for i in self.softwareDict.values():
            self.softwareCategories[i]=[]
            for j in self.softwareDict.keys():
                if self.softwareDict[j] == i:
                    self.softwareCategories[i].append(j)
        #self.softwareItems = {} # dict, format "paketname" : [abhängigkeit1, abhängigkeit2]
        #TODO: read this from configfile
        # e.g. file:  
        # kernel-xenomai xenomai
        # kernel-xenomai busybox
        # 
        # dann
        # for x,y :
        #   if softwareItems.haskey(x):
        #     softwareItems[x].append(y)
        #   else:
        #     softwareItems[x] = []
        #     softwareItems[x].append(y)
        #self.softwareItems["kernel-xenomai"] = ["xenomai","busybox"]
        # opencv
        # openvpn
        # openssh
        # openssl
        # nano
        # gdb
        # wireless-tools
        # Atmel 76c503a

        self.softwareMainVBox = self.factory.createVBox(self.softwareDialog)
        self.softwareMainVBox.setStretchable( 1, True )
        self.softwareMainVBox.setStretchable( 0, True )
        self.softwareMainVBox.setWeight(0,100)
        self.softwareMainVBox.setWeight(1,100)
        
        self.softwareLabel = self.factory.createLabel(self.softwareMainVBox, 
                                                       '''Wählen Sie eine Kategorie aus und drücken Sie "Enter" oder "Auswählen".''')

        self.softwareSelectSize = self.factory.createMinSize(self.softwareMainVBox, 10, 8)
        self.softwareSelectBox = self.factory.createSelectionBox(self.softwareSelectSize, "K&ategorien")
        self.softwareSelectBox.setWeight(0,100)
        self.softwareSelectBox.setWeight(1,100)
        self.softwareSelectBox.setNotify()

        self.softwareBottomHBox = self.factory.createHBox(self.softwareMainVBox)
        self.softwareBottomHBox_left = self.factory.createLeft(self.softwareBottomHBox)
        self.softwareButtonHelp = self.factory.createPushButton(self.softwareBottomHBox_left, "&Hilfe")
        self.softwareBottomHBoxRight = self.factory.createRight(self.softwareBottomHBox)
        self.softwareBottomHBoxRight_hbox = self.factory.createHBox(self.softwareBottomHBox)
        self.softwareButtonCancel = self.factory.createPushButton(self.softwareBottomHBoxRight_hbox, "Zurück")
        self.softwareButtonSelect = self.factory.createPushButton(self.softwareBottomHBoxRight_hbox, "Auswählen")
        self.softwareButtonNext = self.factory.createPushButton(self.softwareBottomHBoxRight_hbox, "Fertig")
        for i in self.softwareCategories.keys():
            self.softwareSelectBox.addItem(i)
        self.softwareDialog.recalcLayout()

       
    def handleEvent(self):
        while True:
            self.event = self.softwareDialog.waitForEvent()
            if not self.event:
                continue
            if self.event.eventType() == yui.YEvent.CancelEvent:
                if self.parent:
                    self.softwareDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    self.softwareDialog.destroy()
                    break
                return self.stateDict, self.configDictOrig
            if self.event.widget() == self.softwareButtonCancel:
                if self.parent:
                    self.softwareDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                else:
                    self.softwareDialog.destroy()
                    break
                return self.stateDict, self.configDictOrig
            
            if self.event.widget() == self.softwareButtonSelect:
                selection = self.softwareSelectBox.selectedItem().label()
                items = self.softwareCategories[selection]
                MY_SOFTWARE_GUI_SELECT = GUI_software_select.GUI_software_select(self.factory, self.softwareDialog.this, selection, items, self.configDict)
                MY_SOFTWARE_GUI_SELECT.handleevent()
            
            if self.event.widget() == self.softwareButtonNext:
                # TODO:  fetch values into configdict
                if self.parent:
                    self.softwareDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDict
                else:
                    self.softwareDialog.destroy()
                    break
                return self.stateDict, self.configDict
            if self.event.widget() == self.softwareSelectBox:
                #self.checkboxframe_update(self.softwareSelectBox.selectedItem())

if __name__ == "__main__":
    factory = yui.YUI.widgetFactory()
    statedict = {}
    configdict = {}
    
    MY_GUI = GUI_software(factory, None, statedict, configdict)
    MY_GUI.handleEvent()

















    def test(self):
        self.software_select_checkboxframe = self.factory.createFrame(self.software_select_hbox, "Auswahl")
        self.software_select_checkboxframe.setWeight(0,80)
        self.software_select_checkboxframe.setWeight(1,80)
        self.software_select_checkboxframe.setStretchable(1,True)
        self.software_select_checkboxframe.setStretchable(0,True)
        self.software_select_checkboxframe_vbox = self.factory.createVBox(self.software_select_checkboxframe)
        self.software_select_checkboxframe_vbox2 = self.factory.createVBox(self.software_select_checkboxframe_vbox)
        self.software_select_checkbox_ = {}
        self.software_select_checkbox_alignment_ = {}
        self.checkboxframe_update(self.softwareSelectBox.selectedItem())
        
    def checkboxframe_update(self, selected_item):
        label = selected_item.label()
        self.software_select_checkboxframe_vbox2.deleteChildren()
        self.software_select_checkboxframe_vbox2_replacepoint = self.factory.createReplacePoint(self.software_select_checkboxframe_vbox2)
        self.software_select_checkbox_ = {}
        self.software_select_checkbox_alignment_ = {}

        for i in self.softwareCategories[label]:
            self.software_select_checkbox_alignment_[i] = self.factory.createLeft(self.software_select_checkboxframe_vbox2)
            self.software_select_checkbox_[i] = self.factory.createCheckBox(self.software_select_checkbox_alignment_[i], i)
            self.software_select_checkbox_[i].setEnabled(True) 
        self.software_select_checkboxframe_vbox2.setEnabled(True)
        self.softwareDialog.recalcLayout()
        appl.redrawScreen()
              