# coding=utf-8
#===============================================================================
#http://xml.coverpages.org/HostetlerMike-PythonAndXML2006.html
#===============================================================================
"""IMAGEROOT_write

Write the lire.conf and possibly other files to the target-root-directory
"""
import os                   # os.path
import sys                  # error handling
import GUI_warning_popup    # warning
import tarfile              # tar.bz2 !
#import XmlDictObject        # XML
from pprint import pprint # pprint
#from xml.etree import ElementTree
from xml.dom import minidom


class IMAGEROOT_write(object):
    """
        
        Write the lire.conf and possibly other files to the target-root-directory
        
        @param myFactory: widgetFactory to use
        @type myFactory: Instance of widgetFactory
        @param myParent: parent widget
        @type myParent: Instance of YDialog 
        @param myConfigDict: configDict
        @type myConfigDict: Dictionary

    """
    def __init__(self, myFactory, myParent, myConfigDict):
        """Write LIRE.config and populate image's "/"
        """
        self.factory = myFactory
        if myParent:
            self.myParent = myParent
            self.myDialog = myParent
        else:
            self.myParent = None
            self.myDialog = self.factory.createPopupDialog()
        #self.stateDict = myStateDict
        self.configDict = myConfigDict.copy()
        #self.configDictOrig = myConfigDict.copy()
        #
        # where to store the file
        self.configOut = os.path.join(str(self.configDict["output_dir"]))
        self.configFileDir = os.path.join(str(self.configDict["output_dir"])+"/root")
        self.configFileEtc = os.path.join(str(self.configFileDir)+"/etc")
        self.configFile = os.path.join(str(self.configFileEtc)+"/lire.conf")
        # empty -> if we have other files to store there, needs to be changed
        if os.path.exists(self.configFileDir):
            if os.path.exists(self.configFile):
                os.remove(self.configFile)
        if os.path.exists(self.configFileEtc):
            #
            if not os.path.isdir(self.configFileEtc):
                os.remove(self.configFileEtc)
                os.makedirs(self.configFileEtc)
        else:
            os.makedirs(self.configFileEtc)
        # the lire.conf itself
    
    def write(self):
        towrite = []
        # keys/values to write
        x = self.configDict["lire_target"].copy()
        # iterate
        try:  # parachute for conversion 
            for k in x.keys():
                # skip cat_ and prereq
                if str("cat_") in k:
                    continue
                if str("_prereq") in k:
                    continue
                #
                # special treatment for "dienste"
                if str("config_lire_target_").lower() in k:
                    name = str(str(k).split("config_lire_")[1]).upper()
                    value = str(x[k])
                    cfg = "%s=\"%s\"\n" % (name,value)
                    towrite.append(str(cfg))
                #
                # all others, split config_lire_ and target_
                else:
                    tmpname = str(str(k).split("config_lire_")[1])
                    name_1 = str(tmpname).split("target_")[0]
                    name_2 = str(tmpname).split("target_")[1]
                    name_lower = ""+str(name_1)+str(name_2)
                    name = str(name_lower).upper()
                    value = str(x[k])
                    cfg = "%s=\"%s\"\n" % (name,value)
                    towrite.append(str(cfg))
        except:
            msg = "Error during conversiont to lire.conf:\n "+str(e)+u"\n".encode("utf-8")
            #
            # error popup 
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myDialog, msg)
            WARNING_URL_GUI.handleEvent()
            return False
        #
        # sort and insert header
        towrite.sort()
        towrite.insert(0, "# lire.conf\n\n")
        #
        # write to disk
        try:
            #print towrite
            datei = open(self.configFile, 'w')
            datei.writelines(towrite)
            datei.close()
#===============missing useradd broke kiwi - fixed in pkg=======================
#            file = os.path.join(str(self.configFileDir)+"/usr/sbin/useradd")
#            if not os.path.exists(file):
#                towrite = ["#!/bin/sh \n", ""]
#                datei = open(file, 'w')
#                datei.writelines
#===============================================================================

        except:
            e = sys.exc_info()[1]
            msg = "Error during write of lire.conf:\n "+str(e)+u"\n".encode("utf-8")
            #
            # error popup 
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myDialog, msg)
            WARNING_URL_GUI.handleEvent()
            return False
        return True
    
    
    def compress(self):
        # http://code.activestate.com/recipes/299412/
        #===============================================================================
        # 
        # import os
        # import tarfile
        # 
        # dstfolder = '/somepath/to/output'
        # fileorfoldertobackup = '/home/username'
        # dst = '%s.tar.bz2' % os.path.join(dstfolder, os.path.basename(fileorfoldertobackup))
        # out = tarfile.TarFile.open(dst, 'w:bz2')
        # out.addfile(fileorfoldertobackup, arcname=os.path.basename(fileorfoldertobackup))
        # out.close()
        # 
        # You can add as many 'addfile' commands as you would like. I hope this saves someone the momentary confusion I experienced.
        #===============================================================================
        try:
            #dst = "%s.tar.bz2" % os.path.join(str(self.configOut)+"/root")
            #out = tarfile.open(dst, "w:bz2")
#            for i in os.walk(self.configFileDir):  # for more -> pathwalker !
            #tarinfo = out.gettarinfo(self.configFile, "root/etc/lire.conf")
            #tarinfo = out.gettarinfo(os.path.join(str(self.configOut)+"/root"), "root")
            #out.addfile(tarinfo)
#============================missing useradd broke kiwi - fixed in pkg===================================================
#            tarinfo = out.gettarinfo(os.path.join(str(self.configFileDir)+"/usr/sbin/useradd"), "root/usr/sbin/useradd")
#            out.addfile(tarinfo)
#===============================================================================
            #out.close()
            cmd = "cd "+str(self.configOut)+" && tar -cjf root.tar.bz2 root/"
            os.system(cmd)
        except:
            e = sys.exc_info()[1]
            msg = "Error:\n "+str(e)+u"\n".encode("utf-8")
            #
            # error popup 
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myDialog, msg)
            WARNING_URL_GUI.handleEvent()
            return False
        return True


#===============================================================================
if __name__ == "__main__":
    myconfigdict = {'net_input_ip': '192.168.1.12', 'profile': 'tmp', 'repo_active': [1], 'required': ['net_input_ip', 'net_input_defaultroute', 'net_input_netmask', 'outputdir', 'net_input_hostname', 'toinstall'], 'repo_input_url_1': 'http://192.168.10.247/lire/base_toolchain/', 'lastprofile': 'expert', 'repo_input_checkbox_1': True, 'softwareDict': {'openssl-doc': 'Productivity', 'libopenssl0_9_8': 'Productivity', 'libdc1394-22': 'Hardware', 'libpng12-0': 'System', 'ed': 'Productivity', 'libraw1394-devel': 'Development', 'libdc1394': 'Hardware', 'libpng3': 'System', 'compat-libstdc++': 'System', 'libraw1394-8': 'System', 'libdc1394_control12': 'Hardware', 'grub': 'System', 'nano': 'Productivity', 'libraw1394': 'System', 'opencv': 'Science', 'openvpn-down-root-plugin': 'Productivity', 'openvpn': 'Productivity', 'openssl-certs': 'Productivity', 'openvpn-auth-pam-plugin': 'Productivity', 'bc': 'Productivity', 'libdc1394-devel': 'Development', 'jpeg': 'Productivity', 'lzo': 'Development', 'opencv-devel': 'System', 'libopenssl-devel': 'Development', 'libjpeg-devel': 'Development', 'libjpeg': 'System', 'openssl': 'Productivity', 'libpng-devel': 'Development', 'lzo-devel': 'Development', 'pkg-config': 'System'}, 'net_input_hostname': 'spb1122', 'net_input_defaultroute': '192.168.1.2', 'soft_to_install': set(['libdc1394-22', 'libdc1394']), 'profiles': {'lire': 'LiRE', 'lire_exp': 'LiRE_exp'}, 'net_input_netmask': '255.255.255.0', 'repo_input_alias_1': 'beispiel', 'output_dir': '/home/dl9pf/lire_out'}
    myROOT_write = IMAGEROOT_write(None,None,{},myconfigdict)
    myROOT_write.write()
