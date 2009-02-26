#coding:utf-8
"""
Popup window mainly for displaying error messages
"""
import yui
import locale
locale.setlocale(locale.LC_ALL, "")

class GUI_warning_popup(object):
    """Gui_warning_popup(myFactory, myParent, myMessage),
    
    @param myFactory: widgetFactory to use
    @type myFactory: Instance of widgetFactory
    @param myParent: Parent widget
    @type myStateDict: Instace of YDialog
    @param Message: (error-) message to display
    @type myConfigDict: String
    
    """
    def __init__(self, myfactory, myparent, message):
        self.factory = myfactory
        self.warningMessage = str(message)
        self.parent = myparent
        #: construct gui
        self.warningPopupDialog = self.factory.createPopupDialog()
        if self.parent:
            self.warningPopupDialog.setParent(self.parent)
        #self.networkdialog.setSize(50,40)
        self.warningVBox = self.factory.createVBox(self.warningPopupDialog)
        self.warningVBox.setStretchable( 0, True )
        self.warningVBox.setStretchable( 1, True )
        
        #self.warningLabel = self.factory.createLabel(self.warningVBox, self.warningMessage)
        #self.warningLabel = self.factory.createOutputField(self.warningVBox, self.warningMessage)
        self.minSize = self.factory.createMinSize(self.warningVBox, 70, 10)
        self.warningLabel = self.factory.createLogView(self.minSize, "Fehler", 15, 200)
        self.warningLabel.setStretchable(1, True)
        self.warningLabel.appendLines(self.warningMessage)
        self.warningButtonOK = self.factory.createPushButton(self.warningVBox, "&OK")
        self.warningButtonOK.setDefaultButton()
        print self.parent
        self.event = None
        
    def handleEvent(self):
        """event loop
        """
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
            if self.event.widget() == self.warningButtonOK :
                if self.parent:
                    self.warningPopupDialog.deleteTopmostDialog()
                    return
                else:
                    self.warningPopupDialog.destroy()
                    break
                    
if __name__ == "__main__":
    factory = yui.YUI.widgetFactory()
    warningmsg = "Diese Meldung wurde Ihnen präsentiert von\nClausthaler!"
    MY_WARNING_POPUP_GUI = GUI_warning_popup(factory, None, warningmsg)
    MY_WARNING_POPUP_GUI.handleEvent() 
    