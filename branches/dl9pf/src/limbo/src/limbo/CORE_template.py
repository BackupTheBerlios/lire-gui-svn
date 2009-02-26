# coding=utf-8
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
"""CORE_template

This is the CORE_template class of LImBO.
     L   I m   B   O           
     ire  |    y   |           
         aging     BS          

    Handle template loading ...

"""

import cPickle as Pickle      # dump data
import re                     # regular expressions
import os                     # file operations
import GUI_warning_popup      # nag screen
import sys                    # system operations

class CORE_template(object):
    def __init__(self):
        """
        Handle the Templates
        extends with  sync()
        """
        #
        # regexp for template-files
        self.regexp = r"\w*\.template"
        #
        # load Default-templates from /opt/limbo/share/templates/
        self.stddir = "/opt/yuitest/share/profiles/"
        self.userdir = os.path.expanduser("~/.limbo/profiles/")
        if os.path.exists(self.stddir):
            self.stdlist = os.listdir(self.stddir)
        else:
            self.stdlist = []
        if os.path.exists(self.userdir):
            self.userlist = os.listdir(self.userdir) # ['x.template']
        else:
            self.userlist = []
            os.makedirs(self.userdir)

    def getTemplateList(self):
        """return a list of available templates"""
        list = []
        #
        # if available, iterate and append
        if self.stdlist:
            for i in self.stdlist:
                list.append(i)
        if self.userlist:
            for i in self.userlist:
                list.append(i)
        return list
    
    def getConfigDict(self, templateName, logView):
        """read the pickle"""
#===============================================================================
#
#  TODO: RM target_dir/root, then COPY /rootfolder from template to target_dir/root
#        in case we use a big set of template root-folder data
#
#===============================================================================
        resultDict = None
        path = None
        #
        # search the 2 dirs for the templates and load the pickle
        if templateName in self.stdlist:
            path = os.path.join(str(str(self.stddir)+str(templateName)+"/"+str(templateName)+".template"))
        if templateName in self.userlist:
            path = os.path.join(str(str(self.userdir)+str(templateName)+"/"+str(templateName)+".template"))
        if path:
            #logView.appendLines(str(path)+"\n")
            if os.path.exists(path):
                fo = open(path, 'r')
                resultDict = Pickle.load(fo)
                fo.close()
                del fo
        return resultDict
        
        
    def saveConfigDict(self, templateName, configDict):
        #
        # will write only in userdict
        # skip std
#===============================================================================
#        #  TODO: Save target_dir/root to tar
#===============================================================================
        if templateName == "Standard":
            return True
        if templateName == "standard":
            return True
        try:
            pathdir = str(self.userdir)+"/"+str(templateName)
            if not os.path.exists(pathdir):
                os.makedirs(pathdir)
            pathfile = str(self.userdir)+"/"+str(templateName)+"/"+str(templateName)+".template"
            fo = open(pathfile, 'wab')
            Pickle.dump(configDict, fo, protocol=1) # protocol might be changed lateron
            fo.close()
            del fo
            result = True
            self.userlist.append(templateName)
        except:
            e = sys.exc_info()[1]
            msg = "Kritischer Fehler:\n "+str(e)+"\nProgramm wird beendet".encode("utf-8")
            #
            # error popup 
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(factory, None, msg)
            WARNING_URL_GUI.handleEvent()
            result = False
        return result
    
    def pprint(self):
        print "stdlist    :"+str(self.stdlist)
        print "userlist   :"+str(self.userlist)
       
#------------------------------------------------------------------------------ 
if __name__ == "__main__":
    pass
    myTemplate = CORE_template()
    myTemplate.pprint()
    print myTemplate.getTemplateList()



