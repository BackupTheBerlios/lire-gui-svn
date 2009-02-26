#coding:utf-8
import yui
import locale
locale.setlocale(locale.LC_ALL, "")

class GUI_popup(object):
    def __init__(self, factory, parent, message):
        self.factory = factory
        self.warningMessage = str(message)
        self.parent = parent
        #construct gui
        self.warningPopupDialog = self.factory.createMainDialog()
        if self.parent:
            self.warningPopupDialog.setParent(self.parent)
        #self.networkdialog.setSize(50,40)
        self.warningVBox = self.warningPopupDialog
        #self.warningVBox = self.factory.createVBox(self.warningPopupDialog)
        #self.warningVBox.setStretchable( 0, True )
        #self.warningVBox.setStretchable( 1, True )
        
        #self.warningLabel = self.factory.createLabel(self.warningVBox, self.warningMessage)

        self.yTableHeader = yui.YTableHeader()
        self.yTableHeader.addColumn("Selected")
        self.yTableHeader.addColumn("Name")
        self.yTableHeader.addColumn("Version")
        self.yTableHeader.addColumn("Description")
        
        self.myTableMinSize = self.factory.createMinSize(self.warningVBox, 50, 12)
        self.myTable = self.factory.createTable(self.myTableMinSize, self.yTableHeader)
        
        myItem = yui.YTableItem("X", "busybox-abc", "1.2.1", "1dasdklöööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööä")
        self.myTable.addItem(myItem)

        myItem2 = yui.YTableItem("", "busybox-def", "1.3.1", "2dasdklöööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööä")
        self.myTable.addItem(myItem2)
        self.myTable.setImmediateMode(True)

        
        #self.warningButtonOK = self.factory.createPushButton(self.warningVBox, "&OK")
        #self.warningButtonOK.setDefaultButton()
        #self.warningPopupDialog.recalcLayout()
#        self.event = None
        
    def handleEvent(self):
        while True:
            self.event = self.warningPopupDialog.waitForEvent()
            if not self.event:
                continue
            if self.event.eventType() == yui.YEvent.CancelEvent:
                if self.parent:
                    self.warningPopupDialog.deleteTopmostDialog()
                    return
                else:
                    self.warningPopupDialog.destroy()
                    break
            continue


if __name__ == "__main__":
    factory = yui.YUI.widgetFactory()
    warningmsg = "Diese Meldung wurde Ihnen präsentiert von\nClausthaler!"
    MY_WARNING_POPUP_GUI = GUI_popup(factory, None, warningmsg)
    MY_WARNING_POPUP_GUI.handleEvent() 