# coding=utf-8
"""Transfer from/to obs"""
import os                   # os.path
import GUI_warning_popup    # warning
from osc import conf,core   # osc -> to talk with oBS    
import urlparse             # some string magic
from urllib import quote_plus #
import shutil               # filesystem manipulation
import StringIO             # stdout redirection
import sys                  # 
import time                 # to insert time

class KIWI_transfer(object):
    def __init__(self, myFactory, myParent, myConfigDict):
        """Transfer from/to obs
        @param myFactory: widgetFactory to use
        @type myFactory: Instance of widgetFactory
        @param myParent: parent widget
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
        self.error = False
        self.apiobject = None
        self.apiuser = None
        self.apipass = None
        self.oscconf = conf.get_config()
        self.project = ""
        self.prjname = "imaging:foo"
        self.pkgname = "imaging"
        self.reponame = "image"
        self.architecture = "i586"
        self.outputDir = os.path.join(self.configDict['output_dir'])
        self.bsDir = os.path.join(str(self.outputDir)+str("/upload"))
        #
        # start
        
    def test(self, logView):
        """Check for availablilty of API
        @param logView: logView to print messages
        @type logView: Instance of logView
        
        This function checks for the project and the package.
        If not present, they'll be created.
        """
        # tweak stdout into logView
        zen=StringIO.StringIO()
        sys.stdout=zen
        #sys.stdout=sys.__stdout__
        if self.configDict.has_key("api_url"):
            #
            #
            logView.appendLines(self.configDict["api_url"]+"\n")
            api = urlparse.urlparse(self.configDict["api_url"])[1]
            logView.appendLines(api+"\n")
            
            # host known ?
            # (check ~/.oscrc)
            if not conf.config.has_key('api_host_options'):
                # key missing !
                msg = str("Konfigurieren sie Benutzername und Passwort für den\nAPI-SERVER in der Datei ~/.oscrc !\n\n".encode("utf-8"))
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myParent, msg) 
                WARNING_URL_GUI.handleEvent()
                return False
            if conf.config['api_host_options'].has_key(api):
                self.apiobject = conf.config['api_host_options'][api]
                self.apiuser = conf.config['api_host_options'][api]['user']
                self.project = "imaging:"+str(self.apiuser)
                self.prjname = self.project
                #
                # check if project exists
                prjlist = core.meta_get_project_list(self.configDict["api_url"])
                #
                # if not there, create it !
                if not self.project in prjlist:
                    #
                    #
                    #create the project  xml-data as in "osc meta prj -e"
                    mydata = ['<project name="'+str(self.project)+'">\n', 
                              '  <title>Imaging Project for'+str(self.apiuser)+'</title>\n', 
                              '  <description>This project provides the imaging.\n', 
                              '\n', 
                              '\n', 
                              '  </description>\n', 
                              '  <person role="maintainer" userid="'+str(self.apiuser)+'"/>\n', 
                              '  <person role="bugowner" userid="'+str(self.apiuser)+'"/>\n', 
                              '  <build>\n', 
                              '    <enable/>\n', 
                              '  </build>\n', 
                              '  <publish>\n', 
                              '    <disable/>\n', 
                              '  </publish>\n', 
                              '  <debuginfo>\n', 
                              '    <disable/>\n', 
                              '  </debuginfo>\n', 
                              '  <repository name="image">\n',]
                    for i in self.configDict["repo_active"]:
                        key_url = str("repo_input_url_"+str(i))
                        tmp = str(str(urlparse.urlparse(self.configDict[key_url])[2]).strip("/"))
                        repository = tmp.split("/")[-1] # last part
                        project_slash = tmp.split(str("/"+repository))[0] # first x parts
                        project_slash_split = project_slash.split("/")  # remove "/"
                        project_name = ""
                        for i in project_slash_split:
                            project_name = str(project_name)+str(i)
                        # ^^^ need to find a more elegant way to do this
                        myappend = '    <path repository="'+str(repository)+'" project="'+str(project_name)+'"/>\n'
                        #mydata.append('    <path repository="%s" project="%s"/>\n')  %(repository, project_name)
                        mydata.append(myappend) 
                    mydata.append('    <arch>i586</arch>\n') 
                    mydata.append('  </repository>\n')
                    mydata.append('</project>\n')
                    apiurl2 = self.configDict["api_url"]
                    logView.appendLines(apiurl2+"\n")
                    #
                    # write the data now
                    core.edit_meta( 
                              data=mydata,
                              metatype="prj", 
                              edit=False, 
                              path_args=quote_plus(self.project), 
                              apiurl=apiurl2
                              )
                    #
                    #write the special prjconf
                    mydata = ['Ignore: distribution-release\n', 'Ignore: distribution-release\n', '\n', '\n', '%if "%_repository" == "image"\n', 'Type: kiwi\n', '%else\n', 'Type: spec\n', '%endif\n']
                    core.edit_meta( 
                              data=mydata,
                              metatype="prjconf", 
                              edit=False, 
                              path_args=quote_plus(self.project), 
                              apiurl=apiurl2
                              )
                #
                # check if it was created
                prjlist = core.meta_get_project_list(self.configDict["api_url"])
                if not self.project in prjlist:
                    #
                    #bail out
                    return False
                #
                #check for the package
                pkglist = core.meta_get_packagelist(self.configDict["api_url"], self.project)
                if not self.pkgname in pkglist:
                    #
                    #create the package
                    files = []
                    mydata = ['<package name="imaging" project="'+str(self.project)+'">\n', '  <title>Limbo imaging Target</title>\n', '  <description>\n', 'LONG DESCRIPTION \n', 'GOES \n', 'HERE\n', '  </description>\n', '  <person role="maintainer" userid="'+str(self.apiuser)+'"/>\n', '  <person role="bugowner" userid="'+str(self.apiuser)+'"/>\n', '  <url>PUT_UPSTREAM_URL_HERE</url>\n', '</package>\n']
                    #
                    # edit_meta
                    core.edit_meta(
                              data=mydata,
                              metatype="pkg", 
                              path_args=(quote_plus(self.project), quote_plus(self.pkgname)), 
                              template_args=({'name': self.pkgname,
                                              'user': self.apiuser
                                              }),
                              apiurl=self.configDict["api_url"]
                              )
#===============================================================================
#                    if False:
#                        #
#                        # display the correct dir when sending the changes
#                        olddir = os.getcwd()
#                        p = core.Package(self.bsDir)
#                        p.todo = files
#                        jahr, monat, tag, stunde, minuten, sekunden = time.localtime()[0:6]
#                        msg = "Auto-checkin by LiRE at %s:%s:%s %s/%s/%s" % (stunde, minuten, sekunden, tag, monat, jahr) 
#                        p.commit(str(msg))
#                        core.set_state(self.pkgname, ' ')
#                        os.chdir(olddir)
# 
#                    pass
#===============================================================================
                #
                # check if it was created
                pkglist = core.meta_get_packagelist(self.configDict["api_url"], self.project)
                if not self.pkgname in pkglist:
                    #
                    #bail out
                    return False
                sys.stdout=sys.__stdout__
                line = zen.getvalue()
                logView.appendLines(line.encode("utf-8"))
                return True
            else:
                msg = str("Konfigurieren sie Benutzername und Passwort für den\nAPI-SERVER in der Datei ~/.oscrc !\n\n".encode("utf-8"))
                WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myParent, msg) 
                WARNING_URL_GUI.handleEvent()
                return False
        else:
            msg = str("Kkeine API-URL gesetzt!\n\n".encode("utf-8"))
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myParent, msg) 
            WARNING_URL_GUI.handleEvent()
            return False
            
    def checkOut(self, logView):
        """Checkout imaging folder
        @param logView: logView to print messages
        @type logView: Instance of logView
        
        This function checks the package out.
        """
        #
        # aquire stdout
        zen=StringIO.StringIO()
        sys.stdout=zen
        #
        # remove the target dir - doppelt hält besser ... 
        self.rm_rf(self.bsDir)
        shutil.rmtree(self.bsDir, ignore_errors=True)
        # 
        #checkout
        try:
            core.checkout_package(self.configDict["api_url"], self.project, self.pkgname, prj_dir=self.bsDir)
        except:
            #
            # fehler während osc checkout
            e = str(sys.exc_info())
            msg = str("Fehler während 'osc checkout'!\n%s\n".encode("utf-8")%(e,))
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myParent, msg) 
            WARNING_URL_GUI.handleEvent()
            sys.stdout=sys.__stdout__
            line = zen.getvalue()
            logView.appendLines(line.encode("utf-8"))
            return False
        #
        # stdout back
        sys.stdout=sys.__stdout__
        line = zen.getvalue()
        logView.appendLines(line.encode("utf-8"))
        return True

    def checkIn(self, logView):
        """Checkin to Server
        @param logView: logView to print messages
        @type logView: Instance of logView
        
        This function copies the files and checks the package in.
        
        """
        #
        # aquire stdout
        zen=StringIO.StringIO()
        sys.stdout=zen
        #
        #move files in
        olddir = os.getcwd()
        if not os.path.exists(self.bsDir):
            print "pah - this is a serious error ... i just checked that stuff out !"
            return False
        src =  os.path.join(self.outputDir+'/config.kiwi')
        dst = os.path.join(self.bsDir+'/imaging/config.kiwi')
        shutil.copy(src, dst)
        src = os.path.join(self.outputDir+'/root.tar.bz2')
        dst = os.path.join(self.bsDir+'/imaging/root.tar.bz2')
        shutil.copy(src, dst)
        #
        # "osc addremove"
        p = core.Package(os.path.join(self.bsDir+'/imaging/'))
        #
        # some pieces are stolen from OSC code ...
        p.todo = p.filenamelist + p.filenamelist_unvers
        for filename in p.todo:
            if os.path.isdir(filename):
                continue
            # ignore foo.rXX, foo.mine for files which are in 'C' state
            if os.path.splitext(filename)[0] in p.in_conflict:
                continue
            state = p.status(filename)
            if state == '?':
                p.addfile(filename)
                #print core.statfrmt('A', core.getTransActPath(os.path.join(p.dir, filename)))
            elif state == '!':
                p.put_on_deletelist(filename)
                p.write_deletelist()
                os.unlink(os.path.join(p.storedir, filename))
                #print core.statfrmt('D', core.getTransActPath(os.path.join(p.dir, filename)))
        #
        # "osc ci -m"image $date"
        jahr, monat, tag, stunde, minuten, sekunden = time.localtime()[0:6]
        msg = "Auto-checkin by LiRE at %s:%s:%s %s/%s/%s" % (stunde, minuten, sekunden, tag, monat, jahr) 
        try:
            p.commit(str(msg))
        except:
            # fehler während osc checkout
            msg = str("Fehler während 'osc checkin'!\n\n".encode("utf-8"))
            WARNING_URL_GUI = GUI_warning_popup.GUI_warning_popup(self.factory, self.myParent, msg) 
            WARNING_URL_GUI.handleEvent()
            sys.stdout=sys.__stdout__
            line = zen.getvalue()
            logView.appendLines(line.encode("utf-8"))
            return False
        #
        # revert stdout hack
        sys.stdout=sys.__stdout__
        line = zen.getvalue()
        logView.appendLines(line.encode("utf-8"))
        return True

    
    def rm_rf(self, d):
        """Taken from http://code.activestate.com/recipes/552732/  MIT-License """
        if os.path.exists(d):
            if os.path.isdir(d):
                for path in (os.path.join(d,f) for f in os.listdir(d)):
                    if os.path.isdir(path):
                        self.rm_rf(path)
                    else:
                        os.unlink(path)
                os.rmdir(d)
            else:
                os.remove(d)
    
    def fetchBinary(self, logView):
        """ fetch the result from OBS
        @param logView: logView to print messages
        @type logView: Instance of logView
        
        This function fetches the result.

        """
        #
        # aquire stdout
        zen=StringIO.StringIO()
        sys.stdout=zen
        binaries = core.get_binarylist(self.configDict["api_url"],
                                   self.project, self.reponame, self.architecture,
                                   package = self.pkgname, verbose=True)
        
        if not os.path.isdir(self.outputDir):
            print "Creating %s" % self.outputDir
            os.makedirs(self.outputDir, 0755)

        if binaries == [ ]:
            msg = ('no binaries found. Either the package does not '
                     'exist, or no binaries have been built.')
            return False

        for binary in binaries:
            # skip source rpms
            if binary.name.endswith('.src.rpm'):
                continue
            target_filename = '%s/%s' % (self.outputDir, binary.name)

            if os.path.exists(target_filename):
                st = os.stat(target_filename)
                if st.st_mtime == binary.mtime and st.st_size == binary.size:
                    continue
        # freezes gui ...
            core.get_binary_file(self.configDict["api_url"],
                            self.project,
                            self.reponame, self.architecture,
                            binary.name,
                            package = self.pkgname,
                            target_filename = target_filename,
                            target_mtime = binary.mtime,
                            progress_meter = False)

        # reset stdout
        sys.stdout=sys.__stdout__
        line = zen.getvalue()
        logView.appendLines(line.encode("utf-8"))
        # hmm test for file ?
        return True

    def fetchLog(self, logView):
        """ fetch the Log from OBS
        @param logView: logView to print messages
        @type logView: Instance of logView
        
        This function fetches the Log.

        """
        #
        # aquire stdout
        zen=StringIO.StringIO()
        sys.stdout=zen
        #
        # fetch
        core.print_buildlog(self.configDict["api_url"], self.project, self.pkgname, self.reponame, self.architecture)
        #
        # reset stdout
        sys.stdout=sys.__stdout__
        line = zen.getvalue()
        logView.appendLines(line.encode("utf-8"))
        return True
    
    def checkStatus(self):
        """Check Status"""
        res = core.get_results(self.configDict["api_url"], self.prjname, self.pkgname)
        return res
    
#    def localbuild(self):
#        """Call osc build"""
#        THIS IS NOT YET IMPLEMENTED IN OBS/OSC !! 
#        pass

if __name__ == "__main__":
    myconfigdict = {'api_url': 'http://192.168.10.246/','net_input_ip': '192.168.1.12', 'profile': 'tmp', 'repo_active': [1], 'required': ['net_input_ip', 'net_input_defaultroute', 'net_input_netmask', 'outputdir', 'net_input_hostname', 'toinstall'], 'repo_input_url_1': 'http://192.168.10.247/lire/base_toolchain/', 'lastprofile': 'expert', 'repo_input_checkbox_1': True, 'softwareDict': {'openssl-doc': 'Productivity', 'libopenssl0_9_8': 'Productivity', 'libdc1394-22': 'Hardware', 'libpng12-0': 'System', 'ed': 'Productivity', 'libraw1394-devel': 'Development', 'libdc1394': 'Hardware', 'libpng3': 'System', 'compat-libstdc++': 'System', 'libraw1394-8': 'System', 'libdc1394_control12': 'Hardware', 'grub': 'System', 'nano': 'Productivity', 'libraw1394': 'System', 'opencv': 'Science', 'openvpn-down-root-plugin': 'Productivity', 'openvpn': 'Productivity', 'openssl-certs': 'Productivity', 'openvpn-auth-pam-plugin': 'Productivity', 'bc': 'Productivity', 'libdc1394-devel': 'Development', 'jpeg': 'Productivity', 'lzo': 'Development', 'opencv-devel': 'System', 'libopenssl-devel': 'Development', 'libjpeg-devel': 'Development', 'libjpeg': 'System', 'openssl': 'Productivity', 'libpng-devel': 'Development', 'lzo-devel': 'Development', 'pkg-config': 'System'}, 'net_input_hostname': 'spb1122', 'net_input_defaultroute': '192.168.1.2', 'soft_to_install': set(['libdc1394-22', 'libdc1394']), 'profiles': {'lire': 'LiRE', 'lire_exp': 'LiRE_exp'}, 'net_input_netmask': '255.255.255.0', 'repo_input_alias_1': 'beispiel', 'output_dir': '/home/dl9pf/lire_out'}
    myKIWI_transfer = KIWI_transfer(None,None,{},myconfigdict)
    myKIWI_transfer.test()
    pass
