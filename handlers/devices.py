#import Globals, sys, curses, traceback, string, os, re, time, ConfigParser
import sys, curses, traceback, string, os, re, time, ConfigParser
from handlers import events
from zenconf import configdicts
from Products.ZenUtils.ZenScriptBase import ZenScriptBase

class devices():
    def __init__(self,BLAH=''):
	self.current_dir = os.path.dirname(os.path.abspath(__file__))+'/../'
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(open(os.path.join(self.current_dir, configdicts.DEVGRPCACHE)))
        self.device_dict={}
        self.group_dict={}
        self.command_dict = {}
        self.dmd = None
        self.evt = events.events()
        try:
            self.dmd = ZenScriptBase(connect=True).dmd
        except Exception, e:
            print "Connection to zenoss dmd failed: %s\n" % e
            #sys.exit(1)


    def refreshDeviceList(self):
        print "Refreshing Devicelist"
        for z in self.dmd.Devices.getSubDevices():
            print "checking device ip %s" % z.manageIp
            if z.manageIp != '':
                print "caching this device"
                self.cacheDevice(z)
    def refreshDevice(self,dev):
        return self.cacheDevice(self.dmd.Devices.findDeviceByIdOrIp(dev['id']))
        #return self.getDevice(dev['sectionid'])

    def performAction(self,action,dev):
	'''
	takes the zenoss device name/ used to take config file device object
	'''
	d=self.getDevice('device-'+dev)
	print "performAction: finding zenoss object by IP"
	zenid=self.findByEc2IP(d['externalip'])
	if zenid:
		print "performAction: got the zenid: %s" % zenid
		return self._performAction(action,zenid)
	else:
		print "performAction: could not get the zenid for device : %s" % d
		return false

    def _performAction(self,action,d,output=None):
        print "_performAction: command %s" % action
        #screen.addstr(0,0,"WORKING",curses.A_BLINK)
        #screen.refresh()
        filename='/tmp/'+d.snmpSysName+"."+d.manageIp+"."+action
        if os.path.exists(filename):
            os.remove(filename)
        FILE = open(filename, "w", 0)
        FILE.write("")
        FILE.close()
        output = open(filename, 'r+', 0)
        command=d.getUserCommands(asDict=True).get(action,None)
        d.doCommandForTarget(command, d, output)
        print "_performAction:  done command"
	football = self.parseCommandOutput(output)
	self.evt.createDeviceEvent(d.name(),'Info','Performing command '+action+' on device '+d.name()+" \n\n<pre>"+football+"</pre>")
        return football

    def parseCommandOutput(self,file):
        file.seek(0)
        removeme=re.compile("ssh -o StrictHostKeyChecking=no")
        results=""
        for line in file:
            text=self.remove_html_tags(line)
            if not text.strip() == ""  and not removeme.search(text):
                results+=text
        file.close()
        return results.strip()

    def remove_html_tags(self,data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)
    
    def getDevice(self,dev):
        '''
        returns the appropiate section from the config file
	    make sure dev has 'device-' or 'group-' followed by zenoss id/name
        '''
        
        #if self.config.has_section(dev):
        #    return self.config.items(dev)
        football = {}
        srv = {}
        cmd = {}
        print "getDevice: checking if config section exists"
        if self.config.has_section(dev):
            print "getting opts from config for dev %s" % dev
            for opt in self.config.options(dev):
                football[opt] = self.config.get(dev,opt)
            '''
            add commands to list
            '''
            try:
                exec("cmd = configdicts.%s_commands" % football['server-type'])
                exec("srv = configdicts.%s_services" % football['server-type'])
                srv.update(configdicts.basic_services)
                cmd.update(configdicts.basic_commands)
            except:
		        pass
            football['commands'] = cmd
            football['services'] = srv
            print "getting events from config for dev %s" % dev
            football['events'] = self.evt.getDeviceEvents(football['id'])
            football
        return football
        
    def listDevices(self,DEVICES=None):
        '''
        pulls all devices from the config file
        '''
        #global config, device_dict
        classes=re.compile('/Server/SSH/Linux/([A-Za-z0-9\/]{0,20})')
        devsearch=re.compile('device-')
        text=''
        i=1
        if DEVICES == None:
            for list in self.config.sections():
                rawtext=''.join(list)
                if devsearch.search(rawtext):
                    text+=rawtext+"\n"
                    self.device_dict[i] = rawtext
                    i=i+1
                    print "Getting device %s" %  rawtext
        else:
            self.device_dict = DEVICES
        return self.device_dict
    
 

    def cacheDevice(self,d):
        '''
        caches the devices attributes in the ini file
        accepts the zenoss object
        '''
        DOMAIN=''
        PROVIDER=''
        ENV='prod'
        STYPE= ''
	try:
		internalip=d.os.interfaces.eth0.getIp()
        except Exception, e:
		internalip=''
		pass
        #global ec2hostname, ENV, config, DOMAIN
        print "Caching snmpsysname %s..." % d.snmpSysName
        SECTION='device-'+d.id
        #ec2hostname= self.performAction('getEc2Hostname',d).strip()
        APP=re.compile('([A-Za-z0-9\-]{0,10})\.([A-Za-z0-9\-]{0,50})\.([A-Za-z]{0,10})')
        STRINGS=APP.findall(d.snmpSysName)
        print "STRINGS %s" % (STRINGS)
	if STRINGS:
         for PART in STRINGS:
		print "DUMPING PARTS %s %s %s" % (PART[0],PART[1],PART[2])
		DOMAIN=PART[1]+PART[2]
		STYPE=PART[0]
	#elif len(STRINGS) != len(DCSTRINGS):
	# print "found a datacenter device, string length = %s" % len(STRINGS)
	# for PART in DCSTRINGS:
	#  DOMAIN='tfound'
	#  PROVIDER='dc'
	#  ENV='prod'
	#  print PART
	#  STYPE=PART
	#  internalip = ''
        #if ENV == '' and DOMAIN == '':
        #    print "not cacheing ..."
        #    return
        #ENV=prod_dict[d.getProdState()]
        #domain=re.compile(ENV + '.' + PROVIDER + '.([A-Za-z0-9]{0,10})')
        #domainr=domain.findall(d.snmpSysName)
        #DOMAIN=''.join(domainr)
        #stypes=re.compile('([A-Za-z0-9]{0,10}).'+ENV + '.' + PROVIDER + '.' + DOMAIN)
        #styper=stypes.findall(d.snmpSysName)
        #stype=''.join(styper)
        if not self.config.has_section(SECTION):
            self.config.add_section(SECTION)
        self.config.set(SECTION, 'id', d.id)
        self.config.set(SECTION, 'sectionid', SECTION)
        self.config.set(SECTION, 'domain', DOMAIN)
        self.config.set(SECTION, 'internalip', internalip)
        self.config.set(SECTION, 'externalip', d.manageIp)
        self.config.set(SECTION, 'internalhostname', d.snmpSysName)
        self.config.set(SECTION, 'externalhostname', d.name())
        self.config.set(SECTION, 'ec2hostname', d.name())
        self.config.set(SECTION, 'key', d.zKeyPath)
        self.config.set(SECTION, 'class', d.getDeviceClassPath())
        self.config.set(SECTION, 'state', ENV )
        self.config.set(SECTION, 'comment', d.comments)
        self.config.set(SECTION, 'lastpuppetsync', '')
        self.config.set(SECTION, 'timestamp', '')
        self.config.set(SECTION, 'server-type', STYPE)
        GROUPSECTION='group-'+DOMAIN+'-'+ENV
        TYPESECTION='group-'+DOMAIN+'-'+ENV+'-'+STYPE
        if not self.config.has_section(GROUPSECTION):
            self.config.add_section(GROUPSECTION)
            self.config.set(GROUPSECTION, 'members', '')
            self.config.set(GROUPSECTION, 'name',DOMAIN+'-'+ENV )
            self.config.set(GROUPSECTION, 'sectionid',GROUPSECTION )
        if not self.config.has_section(TYPESECTION):
            self.config.add_section(TYPESECTION)
            self.config.set(TYPESECTION, 'members', '')
            self.config.set(TYPESECTION, 'name', DOMAIN+'-'+ENV+'-'+STYPE)
            self.config.set(TYPESECTION, 'sectionid',TYPESECTION )
        mygroup = [v.strip() for v in self.config.get(GROUPSECTION, 'members').split(',')]
        mytype = [v.strip() for v in self.config.get(TYPESECTION, 'members').split(',')]
        newgroup = ""
        newtype = ""
        if not SECTION in mygroup:
            try:
                for member in mygroup:
                    if not member == '':
                        newgroup += member+','
                    else:
                        newgroup+=member
            except (AttributeError):
                pass
            mygroup =newgroup+SECTION
            self.config.set(GROUPSECTION, 'members', mygroup)
        if not SECTION in mytype:
            try:
                for member in mytype:
                    if not member == '':
                        newtype += member+','
                    else:
                        newtype+=member
            except (AttributeError):
                pass
            mytype =newtype+SECTION
            self.config.set(TYPESECTION, 'members', mytype)
        for key,serv in configdicts.basic_services.iteritems():
	    try:
             p=d.getRRDDataPoint(serv)
             self.config.set(SECTION, serv, d.getRRDValue(p.getId()))
	    except (AttributeError):
	     pass
	omg={}
	try:
        	exec("omg=configdicts.%s_services.iteritems()" % STYPE)
	except:
		pass
        for key,serv in omg:
            try:
                p=d.getRRDDataPoint(serv)
                self.config.set(SECTION, serv, d.getRRDValue(p.getId()))
            except (RuntimeError, TypeError, NameError,AttributeError):
                pass
#        for dev in self.dmd.ZenEventManager.getDeviceIssues():
#            if d.id in dev:
#                self.config.set(SECTION, 'alerts', 'yes')
#                #print "Alert: %s31;1mYes%s0m" % (CSI,CSI)
#            else:
#                self.config.set(SECTION, 'alerts', 'no')
#                #print "adding to config file for device "+d.id
#                self.config.items(SECTION)
#                #   self.config.write(configfile)
        
        try:
            configfile = open(os.path.join(self.current_dir, configdicts.DEVGRPCACHE), 'wb')
            self.config.write(configfile)
        except Exception, e:
            print "Could not write config: %s\n" % e
        #sys.exit(1)


    def findByEc2Hostname(self,hostname):
        try:
            self.dmd = ZenScriptBase(connect=True).dmd
        except Exception, e:
            print "Connection to zenoss dmd failed: %s\n" % e
 
        for x in self.dmd.Devices.getSubDevices():
            if hostname == x.snmpSysName or hostname == x.name():
                return x

    def findByEc2IP(self,ip):
        try:
            self.dmd = ZenScriptBase(connect=True).dmd
        except Exception, e:
            print "Connection to zenoss dmd failed: %s\n" % e
 
        for x in self.dmd.Devices.getSubDevices():
            if ip == x.manageIp:
                return x
        for i in x.os.interfaces():
            if ip == i.getIp():
                return x

    def findByZenId(self,dev):
        try:
            self.dmd = ZenScriptBase(connect=True).dmd
        except Exception, e:
            print "Connection to zenoss dmd failed: %s\n" % e
 
        return self.dmd.Devices.findDeviceByIdOrIp(dev['id'])
    
    def getStats(self,d):
        # global system, services
        # SECTION='device-'+dev.id
        # system = [v.strip() for v in config.get(SECTION, 'system').split(',')]
        # services = [v.strip() for v in config.get(SECTION, 'services').split(',')]
        # return ([ system, services ])
        cigarbox={}
        stat=self.dmd.Devices.findDeviceByIdOrIp(d['id'])
        SECTION=d['sectionid']
        stype=d['server-type']
        #stype=config.get(SECTION, 'server-type')
        for key,serv in configdicts.basic_services.iteritems():
            try:
                p=stat.getRRDDataPoint(serv)
                config.set(SECTION, serv, stat.getRRDValue(p.getId()))
                cigarbox[key] = stat.getRRDValue(p.getId())
            except (RuntimeError, TypeError, NameError,AttributeError):
                pass
        exec("omg=configdicts.%s_services.iteritems()" % stype)
        for key,serv in omg:
            try:
                p=stat.getRRDDataPoint(serv)
                config.set(SECTION, serv, stat.getRRDValue(p.getId()))
                cigarbox[key] = stat.getRRDValue(p.getId())
            except (RuntimeError, TypeError, NameError,AttributeError):
                pass
        #    print cigarbox
        return cigarbox


