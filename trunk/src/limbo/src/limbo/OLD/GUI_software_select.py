#coding:utf-8
import yui
import locale

class GUI_software_select(object):
    
    def __init__(self, myFactory, myParent, mySelection, myItems, myConfigDict):
        self.factory = myFactory
        self.parent = myParent
        self.selection = mySelection
        self.items = myItems
        self.configDictOrig = myConfigDict.copy()
        self.configDict = myConfigDict.copy()
        
        self.softwareSelectDialog = self.factory.createPopupDialog()
        if self.parent:
            self.softwareSelectDialog.setParent(self.parent)
        self.softwareSelectVbox = self.factory.createVBox(self.softwareSelectDialog)
        self.softwareSelectLabel = self.factory.createLabel(self.softwareSelectVbox, "Pakete der Kategorie "+str(self.selection)+":")
        self.softwareSelectCheckbox_ = {}
        self.softwareSelectCheckboxLeft_ = {}
        for i in self.items:
            self.softwareSelectCheckboxLeft_[i] = self.factory.createLeft(self.softwareSelectVbox)
            self.softwareSelectCheckbox_[i] = self.factory.createCheckBox(self.softwareSelectCheckboxLeft_[i], i)

        self.softwareBottomHBox = self.factory.createHBox(self.softwareSelectVbox)
        self.softwareBottomHBox_left = self.factory.createLeft(self.softwareBottomHBox)
        self.softwareButtonHelp = self.factory.createPushButton(self.softwareBottomHBox_left, "&Hilfe")
        self.softwareBottomHBoxRight = self.factory.createRight(self.softwareBottomHBox)
        self.softwareBottomHBoxRight_hbox = self.factory.createHBox(self.softwareBottomHBox)
        self.softwareButtonCancel = self.factory.createPushButton(self.softwareBottomHBoxRight_hbox, "Zurück")
        self.softwareButtonNext = self.factory.createPushButton(self.softwareBottomHBoxRight_hbox, "Übernehmen")

        self.update()
        self.event = None

    def update(self):
        for i in self.items:
            string = str("software_"+str(self.selection)+"_"+str(i))
            if self.configDict.has_key(string):
                if self.configDict[string] == 1:
                    self.softwareSelectCheckbox_[i].setChecked()
            else:
                self.softwareSelectCheckbox_[i].setChecked(False)
                    
    def check(self):
        pass       
        
    def handleevent(self):
        while True:
            self.event = self.softwareSelectDialog.waitForEvent()
            if not self.event:
                continue
            if self.event.eventType() == yui.YEvent.CancelEvent:
                if self.parent:
                    self.softwareSelectDialog.deleteTopmostDialog()
                    return self.configDictOrig
                else:
                    self.softwareSelectDialog.destroy()
                    break
                return self.configDictOrig
            if self.event.widget() == self.softwareButtonCancel:
                if self.parent:
                    self.softwareSelectDialog.deleteTopmostDialog()
                    return self.configDictOrig
                else:
                    self.softwareSelectDialog.destroy()
                    break
                return self.configDictOrig    
    
    
    
    
    
    
if __name__ == "__main__":
    factory = yui.YUI.widgetFactory()
    statedict = {}
    configdict = {}
    selection = "Libraries"
    items = ["libstdc++", "zlib"]
    
    MY_GUI = GUI_software_select(factory, None, selection, items, configdict)
    MY_GUI.handleevent()