#coding:utf-8
"""Window with timout in waitForEvent()
   Check Status and transfer from obs.
"""
import yui
import locale
import re
import time

locale.setlocale(locale.LC_ALL, "")

class GUI_timeout_popup(object):
    """
    Window with timout in waitForEvent()
    Check Status and transfer from obs.
    """    
    def __init__(self, myfactory, myparent, mytransfer):
        self.factory = myfactory
        self.parent = myparent
        self.myTransfer = mytransfer
        self.count = 0
        self.timeout = True
        self.result = False
        self.status = "Failed"
        #: construct gui
        self.timeoutPopupDialog = self.factory.createPopupDialog()
        if self.parent:
            self.timeoutPopupDialog.setParent(self.parent)
        #self.networkdialog.setSize(50,40)
        self.timeoutVBox = self.factory.createVBox(self.timeoutPopupDialog)
        self.timeoutVBox.setStretchable( 0, True )
        self.timeoutVBox.setStretchable( 1, True )
        
        #self.timeoutLabel = self.factory.createLabel(self.timeoutVBox, self.timeoutMessage)
        #self.timeoutLabel = self.factory.createOutputField(self.timeoutVBox, self.timeoutMessage)
        self.minSize = self.factory.createMinSize(self.timeoutVBox, 70, 10)
        self.timeoutLabel = self.factory.createLogView(self.minSize, "Abbilderstellung:", 15, 200)
        self.timeoutLabel.setStretchable(1, True)
        self.busyindicator = self.factory.createBusyIndicator(self.timeoutVBox, "Aktiv", 5900)
        self.timeoutButtonHBox = self.factory.createHBox(self.timeoutVBox)
        self.timeoutButtonOK = self.factory.createPushButton(self.timeoutButtonHBox, "&OK")
        #self.timeoutButtonOK.setDefaultButton()
        self.timeoutButtonOK.setDisabled()
        self.timeoutButtonCancel = self.factory.createPushButton(self.timeoutButtonHBox, "&Abbruch")
        print self.parent
        self.event = None
    
    def checkStatus(self):
        """
        use osc calls to check the status
        """
        if not self.result:
            status = self.myTransfer.checkStatus()
            jahr, monat, tag, stunde, minuten, sekunden = time.localtime()[0:6]
            msg = "%02d:%02d:%02d" % (stunde, minuten, sekunden) 
            self.timeoutLabel.appendLines(str("Status des Auftrages um "+msg+":\n  "+str(status[0]+"\n")))
            #if status == "succeeded":
            if re.compile("succeeded").search(status[0]):
                self.status="succeeded"
                self.result=True        
                self.timeout = False
                msg=u"\nStarte Übertragung ...\n".encode("utf-8")
                self.timeoutLabel.appendLines(msg)
                self.event = self.timeoutPopupDialog.waitForEvent(1000)
                self.fresult = self.fetch()
                if self.fresult:
                    msg=u"\nÜbertragung erfolgreich abgeschlossen.\n".encode("utf-8")
                    self.timeoutLabel.appendLines(msg)
                else:
                    msg=u"\nÜbertragung fehlerhaft.\n".encode("utf-8")
                    self.timeoutLabel.appendLines(msg)
                    self.status = "failed"
                    self.result = False
                 
                
            #if status == "failed":
            if re.compile("failed").search(status[0]):
                self.status = "failed"
                self.result = True
                self.timeout = False
                self.event = self.timeoutPopupDialog.waitForEvent(1000)
                self.fresult = self.fetchLog()
            #if status == "expansion":
            if re.compile("expansion").search(status[0]):
                self.status = "expansion"
                self.result = True
                self.timeout = False
            #if status == "broken":
            if re.compile("broken").search(status[0]):
                self.status = "broken"
                self.result = True
                self.timeout = False

    def fetch(self):
        """fetch the generate binary
        """
        fresult = self.myTransfer.fetchBinary(self.timeoutLabel)
        #
        # print msg
        if fresult:
            self.timeoutButtonOK.setEnabled()
            self.timeoutButtonCancel.setDisabled()
        return fresult

    def fetchLog(self):
        """fetch/display the logfile
        """
        flresult = self.myTransfer.fetchLog(self.timeoutLabel)
        return flresult
    
    def handleEvent(self):
        """Event loop with timeout
        """
        self.result = False
        while True:
            if self.timeout:
                self.event = self.timeoutPopupDialog.waitForEvent(5000)
            else:
                self.event = self.timeoutPopupDialog.waitForEvent()
            self.checkStatus()
            self.busyindicator.setAlive(True)
            if not self.event:
                continue
            if self.event.eventType() == yui.YEvent.CancelEvent:
                if self.parent:
                    self.timeoutPopupDialog.deleteTopmostDialog()
                    return "failed"
                else:
                    self.timeoutPopupDialog.destroy()
                    break
            if self.event.widget() == self.timeoutButtonOK :
                if self.parent:
                    self.timeoutPopupDialog.deleteTopmostDialog()
                    return self.status
                else:
                    self.timeoutPopupDialog.destroy()
                    break
            if self.event.widget() == self.timeoutButtonCancel :
                if self.parent:
                    self.timeoutPopupDialog.deleteTopmostDialog()
                    return "failed"
                else:
                    self.timeoutPopupDialog.destroy()
                    break
            #
            # catch all
                    
if __name__ == "__main__":
    factory = yui.YUI.widgetFactory()
    timeoutmsg = "Diese Meldung wurde Ihnen präsentiert von\nClausthaler!"
    MY_WARNING_POPUP_GUI = GUI_timeout_popup(factory, None)
    MY_WARNING_POPUP_GUI.handleEvent() 
    