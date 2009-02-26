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
#===============================================================================
# Copyright (C) [2008]  Jan-Simon Möller 
#           (C) [2008]  Leibniz Universität Hannover 
# This program is free software; you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation; either version 2 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
# for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, see <http://www.gnu.org/licenses/>. 
#===============================================================================
#
# GUI_repository.py
# Ask for the repositories
"""GUI_repositories - popup window for repository data"""

###########
# imports #
###########
import yui                  # UI
import re                   # input checks 
import GUI_warning_popup    # popup
import zypp                 # package manager
import os                   # os.path and so on
import sys                  # exceptions

########################
# class GUI_repository #
########################
class GUI_repository(object):
    """GUI_repository(myFactory, myParent, myStateDict, myConfigDict), returns stateDict,configDict
    
    GUI_repositories - popup window for repository data
    
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
        #
        # variables
        self.factory = myFactory
        self.parent = myParent
        self.stateDict = myStateDict
        self.configDictOrig = myConfigDict.copy()
        self.configDict = myConfigDict.copy()
        self.msgWarningURL = u"Bitte geben Sie eine gültige\nURL ein!\n(z.B. http://192.168.10.200/lire/standard/)".encode("utf-8")
        self.msgWarningAlias = u"Bitte geben Sie einen gültigen\nNamen ein!\n(z.B. lire_base)".encode("utf-8")
        self.maxrepo = 4 #: max number of repos to ask for
        self.maxrepos = self.maxrepo+1 # for iteration ;)
        self.softwareDict = {}
        #
        # tmp profile need to check handling for known profiles
        if not self.configDict.has_key("profile"):
            self.configDict["profile"] = "Standard"
        self.repotmppath = os.path.expanduser(str("~/.limbo/profiles/"+str(self.configDict["profile"])))
        if os.path.exists(self.repotmppath):
            for root, dirs, files in os.walk(self.repotmppath, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.removedirs(self.repotmppath)
            os.makedirs(self.repotmppath)
        else:
            os.makedirs(self.repotmppath)
        #
        #: zypp init
        self.zypp = zypp.ZYppFactory_instance().getZYpp()
        #: zypp target (repository cache/path)
        self.target = self.zypp.initializeTarget(zypp.Pathname(self.repotmppath))
        self.repomanageroptions = zypp.RepoManagerOptions(zypp.Pathname(self.repotmppath))
        #: zypp repomanager
        self.repomanager = zypp.RepoManager(self.repomanageroptions)
        self.myrepoinfo_ = {}
        #: zypp metadata pool
        self.pool = self.zypp.pool()
        #
        #: construct gui
        self.repositoryDialog = self.factory.createPopupDialog()
        if self.parent:
            self.repositoryDialog.setParent(self.parent)
        #
        #: VBox
        self.repoVBox = self.factory.createVBox(self.repositoryDialog)
        self.repoVBox.setStretchable( 0, True )
        self.repoVBox.setStretchable( 1, True )
        self.repoVBox.setWeight(0,100)
        self.repoVBox.setWeight(1,100)
        #
        # :label 
        self.repoLabel = self.factory.createLabel(self.repoVBox, "        Angabe der Repositories (max.4)        ")
        # and dicts for gui construction
        self.softwareSelectMinSize_ = {}
        self.repoFrame_ = {}
        self.repoHBox_ = {}
        self.repoCheckBox_ = {}
        self.repoSpacing1_ = {}
        self.repoURL_ = {}
        self.repoSpacing2_ = {}
        self.repoAlias_ = {}
        i = 1
        while i < self.maxrepos:
            #
            # minsize
            self.softwareSelectMinSize_[i] = self.factory.createMinSize(self.repoVBox, 70, 4)
            #
            # frame per input
            self.repoFrame_[i] = self.factory.createFrame(self.softwareSelectMinSize_[i], "Repository "+str(i))
            self.repoFrame_[i].setStretchable( 0, True )
            self.repoFrame_[i].setStretchable( 1, True )
            self.repoFrame_[i].setWeight(0,100)
            self.repoFrame_[i].setWeight(1,100)
            #
            # hbox per input
            self.repoHBox_[i] = self.factory.createHBox(self.repoFrame_[i])
            self.repoHBox_[i].setStretchable( 0, True )
            self.repoHBox_[i].setStretchable( 1, True )
            self.repoHBox_[i].setWeight(0,100)
            self.repoHBox_[i].setWeight(1,100)
            #
            # "enable" checkbox per input
            self.repoCheckBox_[i] = self.factory.createCheckBox(self.repoHBox_[i], "")
            self.repoCheckBox_[i].setStretchable( 0, True )
            self.repoCheckBox_[i].setStretchable( 1, True )
            self.repoCheckBox_[i].setWeight(0,5)
            self.repoCheckBox_[i].setNotify()
            #
            # spacing for "nice view"
            self.repoSpacing1_[i] = self.factory.createHSpacing(self.repoHBox_[i])
            #
            # repourl input
            self.repoURL_[i] = self.factory.createInputField(self.repoHBox_[i], "URL")
            self.repoURL_[i].setStretchable( 0, True )
            self.repoURL_[i].setStretchable( 1, True )
            self.repoURL_[i].setWeight(0,75)
            self.repoURL_[i].setValidChars("1234567890.abcdefghijklmnopqrstuvwxyz:/_-@")
            # 
            # spacing for "nice view"
            self.repoSpacing2_[i] = self.factory.createHSpacing(self.repoHBox_[i])
            #
            # repoalias input 
            self.repoAlias_[i] = self.factory.createInputField(self.repoHBox_[i], "Name")
            self.repoAlias_[i].setStretchable( 0, True )
            self.repoAlias_[i].setStretchable( 1, True )
            self.repoAlias_[i].setWeight(0,15)
            self.repoAlias_[i].setValidChars("1234567890abcdefghijklmnopqrstuvwxyz")
            #
            # always enable first box
            if i == 1:
                self.repoCheckBox_[i].setChecked()
                self.repoAlias_[i].setEnabled()
                self.repoURL_[i].setEnabled()
            else: # disable others by default
                self.repoURL_[i].setDisabled()
                self.repoAlias_[i].setDisabled()
            i = i + 1            
          # end while
        #
        # Buttons down        
        self.repoBottomHBox = self.factory.createHBox(self.repoVBox)
        self.repoButtonCancel = self.factory.createPushButton(self.repoBottomHBox, "Abbruch")
        self.repoButtonNext = self.factory.createPushButton(self.repoBottomHBox, "Weiter")
        self.repoButtonNext.setDefaultButton()
        #
        # empty event
        self.event = None
        #
        # update from configDict
        self.update()

    def update(self):
        """ update from configDict
        """
        k = 1
        #
        # for all repos
        while k < self.maxrepos:
            #
            # get value for "repo_input_checkbox_<num>" if available
            key_enabled = "repo_input_checkbox_"+str(k)
            if self.configDict.has_key(key_enabled):
                self.repoCheckBox_[k].setChecked()
                self.repoCheckBox_[k].setEnabled(True)
            #
            # get value for "repo_input_url_<num>" if available
            key_url = "repo_input_url_"+str(k)
            if self.configDict.has_key(key_url):
                self.repoURL_[k].setValue(str(self.configDict[key_url]))
                if self.repoCheckBox_[k].isChecked():
                    self.repoURL_[k].setEnabled(True)
            #
            # get value for "repo_input_alias_<num>" if available
            key_alias = "repo_input_alias_"+str(k)
            if self.configDict.has_key(key_alias):
                self.repoAlias_[k].setValue(str(self.configDict[key_alias]))
                if self.repoCheckBox_[k].isChecked():
                    self.repoAlias_[k].setEnabled(True)

            if self.repoCheckBox_[k].isChecked():
                self.repoAlias_[k].setEnabled()
                self.repoURL_[k].setEnabled()
            #
            # now "disabled"
            else:
                self.repoAlias_[k].setDisabled()
                self.repoURL_[k].setDisabled()
            #
            # don't forget to go one up ;)
            k = k + 1
            #while end
        #
        # if url is (still) empty fill in default
        #print self.configDict
        if self.repoURL_[1].value() == "":
            if self.configDict.has_key("repo_input_url_1"):
                self.repoURL_[1].setValue(str(self.configDict["repo_input_url_1"]))
            else:    
                self.repoURL_[1].setValue(str("http://192.168.10.247/lire/base_toolchain/"))
        if self.repoURL_[2].value() == "":
            self.repoURL_[2].setValue(str("http://192.168.10.247/lire_own/standard/"))
        if self.repoURL_[3].value() == "":
            self.repoURL_[3].setValue(str("http://192.168.10.247/base_toolchain/standard/"))

        #
        # if alias is (still) empty fill in default
        if self.repoAlias_[1].value() == "":
            self.repoAlias_[1].setValue(str("beispiel"))
        if self.repoAlias_[2].value() == "":
            self.repoAlias_[2].setValue(str("beispiel2"))
        if self.repoAlias_[3].value() == "":
            self.repoAlias_[3].setValue(str("beispiel3"))    
            
            
    def transfer(self):
        """move values to configdict
        """
        h = 1
        #
        # for all repos 
        while h < self.maxrepos:
            #
            # if not enabled - no action
            if not self.repoCheckBox_[h].isChecked():
                h = h + 1 # but go up one
                continue
            #
            # set repo_input_url_<num>"
            key_url = "repo_input_url_"+str(h)
            self.configDict[key_url] = self.repoURL_[h].value()
            #
            # set repo_input_alias_<num>"
            key_alias = "repo_input_alias_"+str(h) 
            self.configDict[key_alias] = self.repoAlias_[h].value()
            #
            # set repo_input_enabled_<num>"
            key_enabled = "repo_input_checkbox_"+str(h)
            self.configDict[key_enabled] = self.repoCheckBox_[h].isChecked()
            h = h + 1 # always count up
            # end while
        
    def checkUrlString(self, inputstring):
        """ Check for valid URL string, returns True/False
        @param inputstring: URL
        @type inputstring: String
        """
        #
        # regexp taken from regexp-database: URL = http://
        # check for valid fqdn
        regexp = r"^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$" #fqdn
        #
        # check for localhost
        regexp2 = r"^http\://localhost+(/\S*)?$" # localhost
        #
        # check for valid url 
        regexp3 = r"^(http|https)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&amp;%\$\-]+)*@)?((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.[a-zA-Z]{2,4})(\:[0-9]+)?(/[^/][a-zA-Z0-9\.\,\?\'\\/\+&amp;%\$#\=~_\-@]*)*$"
        #
        # match regular expression
        if re.match(regexp, inputstring):
            return True   # good ip
        else:
            if re.match(regexp2, inputstring):   # test for localhost
                return True   # good ip
            if re.match(regexp3, inputstring):   # test for ip + x
                return True   # good ip
            return False #bad ip
     
    def checkInput(self):
        """ Check for valid input
        """
        inputOK = False
        #
        # check input
        l = 1
        while l < self.maxrepos:
            #
            # if not enabled, we don't need to check
            if not self.repoCheckBox_[l].isChecked():
                l = l + 1 # but +1
                continue
            #
            # check url
            url = self.repoURL_[l].value()
            if not self.checkUrlString(url):
                msg = str(self.msgWarningURL+u"\nFehlerhaft: Repository #".encode("utf-8")+str(l).encode("utf-8"))
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.repositoryDialog.this, msg)
                WARNING_URL_GUI.handleEvent()
                inputOK = False
                return inputOK
            #
            # check alias
            if self.repoAlias_[l].value() == "":
                msg = str(self.msgWarningAlias+u"\nFehlerhaft: Repository #".encode("utf-8")+str(l).encode("utf-8"))
                WARNING_ALIAS_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.repositoryDialog.this, msg)
                WARNING_ALIAS_GUI.handleEvent()
                inputOK = False
                return inputOK
            inputOK = True
            l = l + 1 # +1
            ##end while
        return inputOK   

    def testrepos(self):
        """ Test if the repos can be loaded
        """
        #
        # remove old repos , we want a _clean_ run
        for repo in self.repomanager.knownRepositories():
            try:
                self.repomanager.removeRepository(repo)
            except: # no clue what possibly could happen here - murphy
                e = sys.exc_info()[1]
                msg = u"Error:\n ".encode("utf-8")+str(e).encode("utf-8")+"\n".encode("utf-8")+"Couldn't remove old repositories.\n Better restart program".encode("utf-8")
                #
                # error popup 
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.repositoryDialog.this, msg)
                WARNING_URL_GUI.handleEvent()
                #
                # exit test
                return False
                
        l = 1
        test = False
        repo_active = []
        #
        # for all repos
        while l < self.maxrepos:
            #
            # if not enabled, skip
            if not self.repoCheckBox_[l].isChecked():
                l = l + 1 # +1
                continue
            #
            # url and alias to use
            key_url = "repo_input_url_"+str(l)
            key_alias = "repo_input_alias_"+str(l) 
            #
            # construct a new repoinfo
            self.myrepoinfo_[l] = zypp.RepoInfo()
            self.myrepoinfo_[l].addBaseUrl(zypp.Url(self.configDict[key_url]))
            self.myrepoinfo_[l].setAlias(self.configDict[key_alias])
            self.myrepoinfo_[l].setName(self.configDict[key_alias])
            self.myrepoinfo_[l].setEnabled(True)
            self.myrepoinfo_[l].setType(zypp.RepoType.RPMMD)
            self.myrepoinfo_[l].setGpgCheck(False)
            #
            #TODO: try_catch  RuntimeError: Repo exception
            try:  # RuntimeError s can happen here
                result = self.repomanager.addRepository(self.myrepoinfo_[l])
                result = self.repomanager.refreshMetadata(self.myrepoinfo_[l])
                result = self.repomanager.buildCache(self.myrepoinfo_[l])
                result = self.repomanager.loadFromCache(self.myrepoinfo_[l])
            except RuntimeError:
                e = sys.exc_info()[1]
                msg = u"Error:\n ".encode("utf-8")+str(e)+"\nRepository #".encode("utf-8")+str(l).encode("utf-8")
                #
                # error popup 
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.repositoryDialog.this, msg)
                WARNING_URL_GUI.handleEvent()
                #
                # exit test
                return False
            except: # catch all others which haven't been spotted yet
                e = sys.exc_info()[1]
                msg = u"Error:\n ".encode("utf-8")+str(e).encode("utf-8")+"\nRepository #".encode("utf-8")+str(l).encode("utf-8")
                #
                # error popup
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.repositoryDialog.this, msg)
                WARNING_URL_GUI.handleEvent()
                #
                # exit test
                return False
            #
            # result should be empty ... 
            if not result == None:
                test = False
            else:
                test = True
                repo_active.append(l)
            l = l + 1 # +1
        # end while
        self.configDict["repo_active"] = repo_active
        return test

        
    def getSoftware(self):
        """ Get the packagenames and so on
        """
        groupDict = {}
        versionDict = {}
        summaryDict = {}
        descrDict = {}
        #
        # try to iterate over the pool
        try: 
            #
            # iterate over the pool
            for item in self.pool:
                #
                # only packages, no sources/patches
                if zypp.isKindPackage(item):
                    #
                    # name of the package
                    name = item.name()
                    #
                    # group of the package
                    group = zypp.asKindPackage(item).group()
                    descr = zypp.asKindPackage(item).description()
                    summary = zypp.asKindPackage(item).summary()
                    version = zypp.asKindPackage(item).edition()
                    #
                    # fill in tempdict
                    groupDict[name] = group
                    summaryDict[name] = summary
                    descrDict[name] = descr
                    versionDict[name] = version
            #
            # only use first part of Group  e.g.: System/network/x -> System
            for i,j in groupDict.iteritems():
                x = {}
                x["Group"] = j.partition("/")[0]
                self.softwareDict[i] = x
            for i,j in summaryDict.iteritems():
                self.softwareDict[i]["Summary"]=str(j)
            for i,j in descrDict.iteritems():
                self.softwareDict[i]["Description"]=str(j)
            for i,j in versionDict.iteritems():
                self.softwareDict[i]["Version"]=str(j)
            #
            # push to configDict
            self.configDict["softwareDict"]=self.softwareDict
        #
        # manage exceptions
        except: # print the exception
                e = sys.exc_info()[1]
                msg = u"Error:\n ".encode("utf-8")+str(e).encode("utf-8")+"\n".encode("utf-8")
                #
                # error popup
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.repositoryDialog.this, msg)
                WARNING_URL_GUI.handleEvent()
                #
                # exit test
                return False
        return True

    #############
    # eventloop #
    #############
    def handleEvent(self):
        """ Event loop
        """
        while True:
            #
            # get event
            self.event = self.repositoryDialog.waitForEvent()
            if not self.event:
                continue
            #
            # window destroyed "x"
            if self.event.eventType() == yui.YEvent.CancelEvent:
                #
                # return to parent and return old values
                if self.parent:
                    self.repositoryDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                #
                # destroy for main()
                else:
                    self.repositoryDialog.destroy()
                    return self.stateDict, self.configDictOrig
            #
            # cancel clicked
            if self.event.widget() == self.repoButtonCancel:
                #
                # return to parent and return old values
                if self.parent:
                    self.repositoryDialog.deleteTopmostDialog()
                    return self.stateDict, self.configDictOrig
                #
                # destroy for test
                else:
                    self.repositoryDialog.destroy()
                    return self.stateDict, self.configDictOrig
            #
            # check every repository "enabled" checkbox
            j = 1
            while j < self.maxrepos:
                if self.event.widget() == self.repoCheckBox_[j]:
                    #
                    # now "enabled"
                    if self.repoCheckBox_[j].isChecked():
                        self.repoAlias_[j].setEnabled()
                        self.repoURL_[j].setEnabled()
                        break
                    #
                    # now "disabled"
                    else:
                        self.repoAlias_[j].setDisabled()
                        self.repoURL_[j].setDisabled()
                        break
                j = j + 1 # +1
                #end while        
            #
            # check "next"
            if self.event.widget() == self.repoButtonNext:
                #
                # check input
                if not self.checkInput():
                    #self.update()
                    continue
                else:
                    #
                    # transfer to configDict
                    self.transfer()
                    #
                    # test if repos can be read
                    if not self.testrepos():
                        #print "nag1"
                        # nag screen
                        continue
                    #
                    # get software names/groups
                    if not self.getSoftware():
                        #print "nag2"
                        # nag screen
                        continue
                    #
                    # we're done
                    self.stateDict["REPOSITORY_DONE"] = 1
                    self.stateDict["SOFTWARE"] = 1
                    #
                    # return to parent
                    if self.parent:
                        self.repositoryDialog.deleteTopmostDialog()
                        return self.stateDict, self.configDict
                    #
                    # destroy for test
                    else:
                        self.repositoryDialog.destroy()
                        return self.stateDict, self.configDict

if __name__ == "__main__":
    """ Standalone test
    """
    import locale
    locale.setlocale(locale.LC_ALL, "")

    factory = yui.YUI.widgetFactory()
    statedict = {}
    statedict["START"] = 1
    statedict["NETZWERK"] = 1
    statedict["NETZWERK_DONE"] = 1
    statedict["REPOSITORY"] = 1
    statedict ["REPOSITORY_DONE"] = 0
    configdict = {}
    configdict["repo_input_url_1"] = "http://lire-repo.rts.uni-hannover.de/lire/base_toolchain/"
    configdict["repo_input_alias_1"] = "lire"
    
    MY_GUI = GUI_repository(factory, None, statedict, configdict)
    statedict, configdict = MY_GUI.handleEvent() 
    
    import pprint
    print "statedict"
    print "#########"
    pprint.pprint(statedict)
    print ""
    print "configdict"
    print "##########"
    pprint.pprint(configdict)
    print ""
    print "softwaredict"
    print "############"
    pprint.pprint(configdict["softwareDict"]) 
