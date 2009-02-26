# coding=utf-8
#===============================================================================
#http://xml.coverpages.org/HostetlerMike-PythonAndXML2006.html
#===============================================================================
"""Write kiwi's config.xml"""
import os                   # os.path
import GUI_warning_popup    # warning
#import XmlDictObject        # XML
from pprint import pprint # pprint
#from xml.etree import ElementTree
from xml.dom import minidom
import urlparse # s#http://#obs//#


class KIWI_write(object):
    def __init__(self, myFactory, myParent, myConfigDict):
        """Write kiwi's config.xml
        @param myFactory: widgetFactory to use (warning popup)
        @type myFactory: Instance of widgetFactory
        @param myParent: parent widget (warning popup)
        @type myParent: Instance of YDialog 
        @param myConfigDict: configDict
        @type myConfigDict: Dictionary
    """
        self.factory = myFactory
        if myParent:
            self.myParent = myParent
        else:
            self.myParent = None
        self.errormsg = None
        self.configDict = myConfigDict.copy()
        #self.checkset("lire_target", "CONFIG_LIRE_TARGET_IMAGE_SIZE", "255")
        self.imageSize = "100" 
        self.lire_target = self.configDict['lire_target'] 
        if self.lire_target.has_key('config_lire_target_image_size'):
            self.imageSize = self.lire_target['config_lire_target_image_size']
        self.error = False
        #
        # start
        self.roottag = "<image/>"
        self.newdoc  = minidom.parseString(self.roottag)
        self.newdoc.documentElement.setAttribute("name","limbo-auto-config")
        self.newdoc.documentElement.setAttribute("schemeversion","2.4")
        self.newdoc2  = minidom.parseString(self.roottag)
        self.newdoc2.documentElement.setAttribute("name","limbo-auto-config-kiwi")
        self.newdoc2.documentElement.setAttribute("schemeversion","2.4")
        if not self.configDict.has_key("repo_active"):
            self.errormsg = "Fehler: repo_active nicht gesetzt"
        

    def writeXml(self, outputType):
        if self.errormsg:
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myParent, self.errormsg) 
            WARNING_URL_GUI.handleEvent()
        if self.error:
            # bail out (from "no software/repo" screen)
            return False
        #
        # description
        self.description = self.newdoc.createElement("description")
        self.description.setAttribute("type", "system")
        self.newdoc.documentElement.appendChild(self.description)
        # description.author
        self.author = self.newdoc.createElement("author")
        self.author.appendChild(self.newdoc.createTextNode("rts"))
        self.description.appendChild(self.author)
        # description.contact
        self.contact = self.newdoc.createElement("contact")
        self.contact.appendChild(self.newdoc.createTextNode("lire@rts.uni-hannover.de"))
        self.description.appendChild(self.contact)
        # description.specification
        self.specification = self.newdoc.createElement("specification")
        self.specification.appendChild(self.newdoc.createTextNode("limbo kiwi auto-config"))
        self.description.appendChild(self.specification)
        #
        # preferences
        self.preferences = self.newdoc.createElement("preferences")
        self.newdoc.documentElement.appendChild(self.preferences)
        # preferences.type
        if outputType == "ext2":
            self.preftype = self.newdoc.createElement("type")
            self.preftype.setAttribute("primary", "true")
            self.preftype.setAttribute("filesystem", "ext2")
            self.preftype.appendChild(self.newdoc.createTextNode("ext2"))
            self.preferences.appendChild(self.preftype)
        if outputType == "ext3":
            self.preftype = self.newdoc.createElement("type")
            self.preftype.setAttribute("primary", "true")
            self.preftype.setAttribute("filesystem", "ext3")
            self.preftype.appendChild(self.newdoc.createTextNode("ext3"))
            self.preferences.appendChild(self.preftype)
        if outputType == "iso9660":
            self.preftype = self.newdoc.createElement("type")
            self.preftype.setAttribute("boot", "isoboot/lire")
            self.preftype.setAttribute("flags", "unified")
            self.preftype.appendChild(self.newdoc.createTextNode("iso"))
            self.preferences.appendChild(self.preftype)
        if outputType == "vmdk":
            self.preftype = self.newdoc.createElement("type")
            self.preftype.setAttribute("boot", "vmxboot/lire")
            self.preftype.setAttribute("filesystem", "ext2")
            self.preftype.appendChild(self.newdoc.createTextNode("vmx"))
            self.preferences.appendChild(self.preftype)
        if outputType == "pxe":
            self.preftype = self.newdoc.createElement("type")
            self.preftype.setAttribute("boot", "netboot/lire")
            self.preftype.setAttribute("filesystem", "ext2")
            self.preftype.appendChild(self.newdoc.createTextNode("pxe"))
            self.preferences.appendChild(self.preftype)
        # preferences.version
        self.prefver = self.newdoc.createElement("version")
        self.prefver.appendChild(self.newdoc.createTextNode("0.0.1"))
        self.preferences.appendChild(self.prefver)
        # preferences.size
        self.prefsize = self.newdoc.createElement("size")
        self.prefsize.setAttribute("unit", "M")
        self.prefsize.appendChild(self.newdoc.createTextNode(self.imageSize))
        self.preferences.appendChild(self.prefsize)
        # preferences.pkgmngr
        self.pkgmngr = self.newdoc.createElement("packagemanager")
        self.pkgmngr.appendChild(self.newdoc.createTextNode("zypper"))
        self.preferences.appendChild(self.pkgmngr)
        # preferences.rpmchecksig
        self.rpmchecksig = self.newdoc.createElement("rpm-check-signatures")
        self.rpmchecksig.appendChild(self.newdoc.createTextNode("False"))
        self.preferences.appendChild(self.rpmchecksig)
        # preferences.rpmforce
        self.rpmforce = self.newdoc.createElement("rpm-force")
        self.rpmforce.appendChild(self.newdoc.createTextNode("True"))
        self.preferences.appendChild(self.rpmforce)
        # preferences.locale
        self.locale = self.newdoc.createElement("locale")
        self.locale.appendChild(self.newdoc.createTextNode("en_US"))
        self.preferences.appendChild(self.locale)
        # preferences.keytable
        self.keytable = self.newdoc.createElement("keytable")
        self.locale.appendChild(self.newdoc.createTextNode("us.map.gz"))
        self.preferences.appendChild(self.keytable)
        #
        # users (group = root)
        self.users_root = self.newdoc.createElement("users")
        self.users_root.setAttribute("group", "root")
        self.newdoc.documentElement.appendChild(self.users_root)
        # users.user
        self.rootuser = self.newdoc.createElement("user")
        self.rootuser.setAttribute("name", "root")
        self.rootuser.setAttribute("home", "/")
        self.rootuser.setAttribute("pwd", "")
        self.users_root.appendChild(self.rootuser)
        #
        # repositories
        self.repo_ = {}
        self.reposource_ = {}
        for i in self.configDict["repo_active"]:
            key_url = str("repo_input_url_"+str(i))
            self.repo_[i]=self.newdoc.createElement("repository")
            self.repo_[i].setAttribute("type", "rpm-md")
            self.newdoc.documentElement.appendChild(self.repo_[i])
            self.reposource_[i]=self.newdoc.createElement("source")
            self.reposource_[i].setAttribute("path", self.configDict[key_url])
            self.repo_[i].appendChild(self.reposource_[i])
        # packages_bootstrap
        self.packages_bootstrap = self.newdoc.createElement("packages")
        self.packages_bootstrap.setAttribute("type", "bootstrap")
        self.newdoc.documentElement.appendChild(self.packages_bootstrap)
        # packages_bootstrap.package<n>
        self.pkg_ = {}
        for j in self.configDict["soft_to_install"]:
            self.pkg_[j]=self.newdoc.createElement("package")
            self.pkg_[j].setAttribute("name", j)
            self.packages_bootstrap.appendChild(self.pkg_[j])
        #newtag.appendChild(newdoc.createTextNode("text value"))
        #print self.newdoc.toprettyxml()
        #self.newdoc.write("/home/dl9pf/config.xml")
        #
        # todo: try/catch ?
        try:
            configFilePath = os.path.join(str(self.configDict["output_dir"])+"/config.xml")
            if os.path.exists(configFilePath):
                os.remove(configFilePath)
            fd = open(configFilePath , "w" )
            self.newdoc.writexml(fd)
            fd.close()
        except:
            msg = "Error:\n "+str(e)+u"\n".encode("utf-8")
            #
            # error popup 
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myDialog, msg)
            WARNING_URL_GUI.handleEvent()
            return False
        return True

    def writeKiwi(self, outputType):
        if self.errormsg:
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myParent, self.errormsg) 
            WARNING_URL_GUI.handleEvent()
        if self.error:
            # bail out (from "no software/repo" screen)
            return False
        #
        # description
        self.description = self.newdoc2.createElement("description")
        self.description.setAttribute("type", "system")
        self.newdoc2.documentElement.appendChild(self.description)
        # description.author
        self.author = self.newdoc2.createElement("author")
        self.author.appendChild(self.newdoc2.createTextNode("rts"))
        self.description.appendChild(self.author)
        # description.contact
        self.contact = self.newdoc2.createElement("contact")
        self.contact.appendChild(self.newdoc2.createTextNode("lire@rts.uni-hannover.de"))
        self.description.appendChild(self.contact)
        # description.specification
        self.specification = self.newdoc2.createElement("specification")
        self.specification.appendChild(self.newdoc2.createTextNode("limbo kiwi auto-config"))
        self.description.appendChild(self.specification)
        #
        # preferences
        self.preferences = self.newdoc2.createElement("preferences")
        self.newdoc2.documentElement.appendChild(self.preferences)
        # preferences.type
        if outputType == "ext2":
            self.preftype = self.newdoc2.createElement("type")
            self.preftype.setAttribute("primary", "true")
            self.preftype.setAttribute("filesystem", "ext2")
            self.preftype.appendChild(self.newdoc2.createTextNode("ext2"))
            self.preferences.appendChild(self.preftype)
        if outputType == "ext3":
            self.preftype = self.newdoc2.createElement("type")
            self.preftype.setAttribute("primary", "true")
            self.preftype.setAttribute("filesystem", "ext3")
            self.preftype.appendChild(self.newdoc2.createTextNode("ext3"))
            self.preferences.appendChild(self.preftype)
        if outputType == "iso9660":
            self.preftype = self.newdoc2.createElement("type")
            self.preftype.setAttribute("boot", "isoboot/lire")
            self.preftype.setAttribute("flags", "unified")
            self.preftype.appendChild(self.newdoc2.createTextNode("iso"))
            self.preferences.appendChild(self.preftype)
        if outputType == "vmdk":
            self.preftype = self.newdoc2.createElement("type")
            self.preftype.setAttribute("boot", "vmxboot/lire")
            self.preftype.setAttribute("filesystem", "ext2")
            self.preftype.appendChild(self.newdoc2.createTextNode("vmx"))
            self.preferences.appendChild(self.preftype)
        if outputType == "pxe":
            self.preftype = self.newdoc2.createElement("type")
            self.preftype.setAttribute("boot", "netboot/lire")
            self.preftype.setAttribute("filesystem", "ext2")
            self.preftype.appendChild(self.newdoc2.createTextNode("pxe"))
            self.preferences.appendChild(self.preftype)
        # preferences.version
        self.prefver = self.newdoc2.createElement("version")
        self.prefver.appendChild(self.newdoc2.createTextNode("0.0.1"))
        self.preferences.appendChild(self.prefver)
        # preferences.size
        self.prefsize = self.newdoc2.createElement("size")
        self.prefsize.setAttribute("unit", "M")
        self.prefsize.appendChild(self.newdoc2.createTextNode(self.imageSize))
        self.preferences.appendChild(self.prefsize)
        # preferences.pkgmngr
        self.pkgmngr = self.newdoc2.createElement("packagemanager")
        self.pkgmngr.appendChild(self.newdoc2.createTextNode("zypper"))
        self.preferences.appendChild(self.pkgmngr)
        # preferences.rpmchecksig
        self.rpmchecksig = self.newdoc2.createElement("rpm-check-signatures")
        self.rpmchecksig.appendChild(self.newdoc2.createTextNode("False"))
        self.preferences.appendChild(self.rpmchecksig)
        # preferences.rpmforce
        self.rpmforce = self.newdoc2.createElement("rpm-force")
        self.rpmforce.appendChild(self.newdoc2.createTextNode("True"))
        self.preferences.appendChild(self.rpmforce)
        # preferences.locale
        self.locale = self.newdoc2.createElement("locale")
        self.locale.appendChild(self.newdoc2.createTextNode("en_US"))
        self.preferences.appendChild(self.locale)
        # preferences.keytable
        self.keytable = self.newdoc2.createElement("keytable")
        self.locale.appendChild(self.newdoc2.createTextNode("us.map.gz"))
        self.preferences.appendChild(self.keytable)
        #
        # users (group = root)
        self.users_root = self.newdoc2.createElement("users")
        self.users_root.setAttribute("group", "root")
        self.newdoc2.documentElement.appendChild(self.users_root)
        # users.user
        self.rootuser = self.newdoc2.createElement("user")
        self.rootuser.setAttribute("name", "root")
        self.rootuser.setAttribute("home", "/")
        self.rootuser.setAttribute("pwd", "")
        self.users_root.appendChild(self.rootuser)
        #
        # repositories
        self.repo_ = {}
        self.reposource_ = {}
        for i in self.configDict["repo_active"]:
            key_url = str("repo_input_url_"+str(i))
            self.repo_[i]=self.newdoc2.createElement("repository")
            self.repo_[i].setAttribute("type", "rpm-md")
            self.newdoc2.documentElement.appendChild(self.repo_[i])
            self.reposource_[i]=self.newdoc2.createElement("source")
            obsurl = "obs://"+str(str(urlparse.urlparse(self.configDict[key_url])[2]).strip("/")) # need to fish out url without
            print obsurl
            self.reposource_[i].setAttribute("path", obsurl)
            self.repo_[i].appendChild(self.reposource_[i])
        # packages_bootstrap
        self.packages_bootstrap = self.newdoc2.createElement("packages")
        self.packages_bootstrap.setAttribute("type", "bootstrap")
        self.newdoc2.documentElement.appendChild(self.packages_bootstrap)
        # packages_bootstrap.package<n>
        self.pkg_ = {}
        for j in self.configDict["soft_to_install"]:
            self.pkg_[j]=self.newdoc2.createElement("package")
            self.pkg_[j].setAttribute("name", j)
            self.packages_bootstrap.appendChild(self.pkg_[j])
        #newtag.appendChild(newdoc.createTextNode("text value"))
        #print self.newdoc2.toprettyxml()
        #self.newdoc2.write("/home/dl9pf/config.xml")
        #
        # todo: try/catch ?
        try:
            configFilePath = os.path.join(str(self.configDict["output_dir"])+"/config.kiwi")
            if os.path.exists(configFilePath):
                os.remove(configFilePath)
            fd = open(configFilePath , "w" )
            self.newdoc2.writexml(fd)
            fd.close()
        except:
            msg = "Error:\n "+str(e)+u"\n".encode("utf-8")
            #
            # error popup 
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myDialog, msg)
            WARNING_URL_GUI.handleEvent()
            return False
        return True


if __name__ == "__main__":
    myconfigdict = {'net_input_ip': '192.168.1.12', 'profile': 'tmp', 'repo_active': [1], 'required': ['net_input_ip', 'net_input_defaultroute', 'net_input_netmask', 'outputdir', 'net_input_hostname', 'toinstall'], 'repo_input_url_1': 'http://192.168.10.247/lire/base_toolchain/', 'lastprofile': 'expert', 'repo_input_checkbox_1': True, 'softwareDict': {'openssl-doc': 'Productivity', 'libopenssl0_9_8': 'Productivity', 'libdc1394-22': 'Hardware', 'libpng12-0': 'System', 'ed': 'Productivity', 'libraw1394-devel': 'Development', 'libdc1394': 'Hardware', 'libpng3': 'System', 'compat-libstdc++': 'System', 'libraw1394-8': 'System', 'libdc1394_control12': 'Hardware', 'grub': 'System', 'nano': 'Productivity', 'libraw1394': 'System', 'opencv': 'Science', 'openvpn-down-root-plugin': 'Productivity', 'openvpn': 'Productivity', 'openssl-certs': 'Productivity', 'openvpn-auth-pam-plugin': 'Productivity', 'bc': 'Productivity', 'libdc1394-devel': 'Development', 'jpeg': 'Productivity', 'lzo': 'Development', 'opencv-devel': 'System', 'libopenssl-devel': 'Development', 'libjpeg-devel': 'Development', 'libjpeg': 'System', 'openssl': 'Productivity', 'libpng-devel': 'Development', 'lzo-devel': 'Development', 'pkg-config': 'System'}, 'net_input_hostname': 'spb1122', 'net_input_defaultroute': '192.168.1.2', 'soft_to_install': set(['libdc1394-22', 'libdc1394']), 'profiles': {'lire': 'LiRE', 'lire_exp': 'LiRE_exp'}, 'net_input_netmask': '255.255.255.0', 'repo_input_alias_1': 'beispiel', 'output_dir': '/home/dl9pf/lire_out'}
    myKIWI_write = KIWI_write(None,None,{},myconfigdict)
    myKIWI_write.write_xml()
    myKIWI_write.write_kiwi()

    pass
