#!/usr/bin/env python
import Globals, sys, curses, traceback, string, os, re, time, ConfigParser
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from cStringIO import StringIO
from operator import itemgetter
from zenconf import configdicts

# vars
ZENCLASS='/Server/Linux/'
PROVIDER='ec2'
CONFIG='zenconf/zenhosts.cfg'
DOMAIN='tfound'
ENV='prod'
subcat='mongo'
ec2hostname=''
dryrun='no'

# dictionaries
device_dict={}
group_dict={}
prod_dict = { 'Production': 'prod', 'Staging': 'staging', 'QA': 'qa','Development': 'dev' }
queue_services = { '1min Loadavg': 'loadavg_1min',  'MongoS cmd/s': 'MongoStats_commands', 'MongoS q/s': 'MongoStats_querys', 'MongoS conns/s': 'MongoStats_conns' }
docbase1_services = { '1min Loadavg': 'loadavg_1min', 'MongoD cmd/s': 'MongoD_Stats_commands', 'MongoD q/s': 'MongoD_Stats_querys', 'MongoD conns/s': 'MongoD_Stats_conns' }
webdocbase_services = { '1min Loadavg': 'loadavg_1min', 'Mongo cmd/s': 'MongoStats_commands', 'Mongo q/s': 'MongoStats_querys', 'Mongo conns/s': 'MongoStats_conns' }
web_services = { '1min Loadavg': 'loadavg_1min', 'Apache CPU Load': 'apache_cpuLoad', 'Apache Busy Slots': 'apache_slotSendingReply', 'MongoS cmd/s': 'MongoStats_commands', 'MongoS q/s': 'MongoStats_querys', 'MongoS conns/s': 'MongoStats_conns', 'JMX Heap used': 'JMX Heap Memory_used', 'JMX Heap max': 'JMX Heap Memory_max','JMX Files': 'JMX Open File Descriptors_OpenFiles','JMX Threads': 'JMX Thread Count_ThreadCount'}
queue_services = { '1min Loadavg': 'loadavg_1min', 'Apache CPU Load': 'apache_cpuLoad', 'Apache Busy Slots': 'apache_slotSendingReply', 'MongoS cmd/s': 'MongoStats_commands', 'MongoS q/s': 'MongoStats_querys', 'MongoS conns/s': 'MongoStats_conns', 'JMX Heap used': 'JMX Heap Memory_used', 'JMX Heap max': 'JMX Heap Memory_max','JMX Files': 'JMX Open File Descriptors_OpenFiles','JMX Threads': 'JMX Thread Count_ThreadCount','Corejobs Low':'CheckQueue_corejobs_low','Corejobs Medium':'CheckQueue_corejobs_medium','Corejobs High':'CheckQueue_corejobs_high'}
queues_services = { '1min Loadavg': 'loadavg_1min', 'Apache CPU Load': 'apache_cpuLoad', 'Apache Busy Slots': 'apache_slotSendingReply', 'MongoS cmd/s': 'MongoStats_commands', 'MongoS q/s': 'MongoStats_querys', 'MongoS conns/s': 'MongoStats_conns', 'JMX Heap used': 'JMX Heap Memory_used', 'JMX Heap max': 'JMX Heap Memory_max','JMX Files': 'JMX Open File Descriptors_OpenFiles','JMX Threads': 'JMX Thread Count_ThreadCount'}
queuem_services = {'Corejobs Low':'CheckQueue_corejobs_low','Corejobs Medium':'CheckQueue_corejobs_medium','Corejobs High':'CheckQueue_corejobs_high'}
search_services = { '1min Loadavg': 'loadavg_1min', 'Apache CPU Load': 'apache_cpuLoad', 'Apache Busy Slots': 'apache_slotSendingReply', 'MongoS cmd/s': 'MongoStats_commands', 'MongoS q/s': 'MongoStats_querys', 'MongoS conns/s': 'MongoStats_conns', 'JMX Heap used': 'JMX Heap Memory_used', 'JMX Heap max': 'JMX Heap Memory_max','JMX Files': 'JMX Open File Descriptors_OpenFiles','JMX Threads': 'JMX Thread Count_ThreadCount'}
basic_services =  { '1min Loadavg': 'loadavg_1min', 'Cpu Usage': 'cpu_ssCpuIdle' }
server_dict = {'Webonly': 'webonly', 'Mongo Standalone': 'docbase', 'MongoC': 'docbasec', 'MongoD': 'docbased', 'Mongo ReplSet': 'docbase1', 'MongoS': 'docbases','Web and Search': 'web', 'Corejobs/Rabbit': 'queue', 'Corejobs': 'queuem', 'Search': 'search'}
basic_commands = {'What am I':'whatami','Puppetsync':'puppetsync'}
queue_commands = {'Start Corejobs':'corejobsstart','Stop Corejobs':'corejobsstop','Start MongoS':'mongosstart','Stop MongoS':'mongosstop','SC Rsync to Akamai':'tfound-akamai-sync','Start Memcached':'memcachedstart','Stop Memcached':'memcachedstop'}
web_commands = {'Start Apache':'apachestart','Stop Apache':'apachestop','Start Memcached':'memcachedstart','Stop Memcached':'memcachedstop','Start MongoS':'mongosstart','Stop MongoS':'mongosstop'}
search_commands = {'Start Memcached':'memcachedstart','Stop Memcached':'memcachedstop','Start MongoS':'mongosstart','Stop MongoS':'mongosstop','Start Dasserver':'dasserverstart','Stop Dasserver':'dasserverstop'}
command_dict = {}

# import cached settings
config = ConfigParser.RawConfigParser()
config.readfp(open(CONFIG))

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def getmax(lines): return max([len(str(l)) for l in lines])

def showdata(screen,data):
    wy,wx=screen.getmaxyx()
    wy-=4
    wx-=4
    if type(data)==str:
        data = data.split('\n')
    padx = max(getmax(data),wx)
    pady = max(len(data)+1,wy)
    max_x = padx-wx
    max_y = pady-wy
    pad = curses.newpad(pady,padx)
    pad.box()
    for i,line in enumerate(data):
        pad.addstr(i,4,str(line))
    x=0
    y=0
    screen.addstr(0,0,"VIEWING LOG",curses.A_BOLD)
    screen.addstr(0,15,"KEYS",curses.A_NORMAL)
    screen.addstr(0,20,"u",hotkey_attr)
    screen.addstr(0,21,"p",curses.A_NORMAL)
    screen.addstr(0,23,"d",hotkey_attr)
    screen.addstr(0,24,"own",curses.A_NORMAL)
    screen.addstr(0,28,"l",hotkey_attr)
    screen.addstr(0,29,"eft",curses.A_NORMAL)
    screen.addstr(0,33,"r",hotkey_attr)
    screen.addstr(0,34,"ight",curses.A_NORMAL)
    screen.addstr(0,39,"Page ",curses.A_NORMAL)
    screen.addstr(0,44,"U",hotkey_attr)
    screen.addstr(0,45,"p",curses.A_NORMAL)
    screen.addstr(0,47,"Page ",curses.A_NORMAL)
    screen.addstr(0,52,"D",hotkey_attr)
    screen.addstr(0,53,"own",curses.A_NORMAL)
    screen.addstr(0,57,"t",hotkey_attr)
    screen.addstr(0,58,"op",curses.A_NORMAL)
    screen.addstr(0,61,"b",hotkey_attr)
    screen.addstr(0,62,"ottom",curses.A_NORMAL)
    screen.addstr(0,68,"q",hotkey_attr)
    screen.addstr(0,69,"uit",curses.A_NORMAL)
   
    inkey=0
    screen.refresh()    
    while inkey != 'q':
        pad.refresh(y,x,1,1,wy,wx)
        inkey = screen.getkey()
        
                
        if inkey=='u':y=max(y-1,0)
        elif inkey=='d':y=min(y+1,max_y)
        elif inkey=='l':x=max(x-1,0)
        elif inkey=='r':x=min(x+1,max_x)
        elif inkey=='D':y=min(y+wy,max_y)
        elif inkey=='U':y=max(y-wy,0)
        elif inkey=='t':y=0
        elif inkey=='b':y=max_y
    screen.erase() 

def displayAction(action,d=None):
 domain_check = re.compile(DOMAIN)
 subcat_check = re.compile(subcat)
 if not d == None:
   text=_performAction(action,d)
   if dryrun == 'no':
    showdata(screen,text)
    manageDevice(d)
    return CONTINUE
 for d in dmd.Devices.getSubDevices():
  path=d.getDeviceClassPath()
  state=d.getProdState()
  if domain_check.search(path) and subcat_check.search(path) and state == ENV:
   if dryrun == 'no':
    text=_performAction(action,d)
    showdata(screen,text)
# we'll want to log the event in zenoss here

def _performAction(action,d):
    screen.addstr(0,0,"WORKING",curses.A_BLINK)
    screen.refresh()
    filename='/tmp/'+d.snmpSysName+"."+d.manageIp+"."+action
    if os.path.exists(filename):
     os.remove(filename)
    FILE = open(filename, "w", 0)
    FILE.write("")
    FILE.close()
    output = open(filename, 'r+', 0)
    command=d.getUserCommands(asDict=True).get(action,None)
    d.doCommandForTarget(command, d, output)
    return parseCommandOutput(output)
 
def displayCommandOutput(football):
  #manageDevice will use this
  # becuz i need to get command output elsewhere
  print ""

def parseCommandOutput(file):
   file.seek(0)
   removeme=re.compile("ssh -o StrictHostKeyChecking=no")
   results=""
   for line in file:
    text=remove_html_tags(line)
    if not text.strip() == ""  and not removeme.search(text):
     results+=text
   file.close()
   return results

def listGroups():
 global config, group_dict
 classes=re.compile(ZENCLASS +'/([A-Za-z0-9\/]{0,20})')
 devsearch=re.compile('group-')
 text=''
 i=1
 for list in config.sections():
  rawtext=''.join(list)
  if devsearch.search(rawtext):
   text+=rawtext+"\n"
   group_dict[i] = rawtext
   i=i+1 
 s = curses.newwin(40, 90, 5, 3)
 s.box()
 s.addstr(0,1, "Group List", curses.A_BOLD)
 s.addstr(2,6, "Name", curses.A_BOLD)
 i=1
 stype, host, state, lass, lasses, lasse, alert='','','','','','',''
 #for k,x in group_dict.iteritems():
 for k,x in sorted(group_dict.iteritems(), key=itemgetter(1)):
  #print x 
  try:
   SECTION='group-'+x
   stype=config.get(SECTION, 'server-type') 
   host=config.get(SECTION, 'externalip') 
   state=config.get(SECTION, 'state') 
   lass=config.get(SECTION, 'class') 
   alert=config.get(SECTION, 'alerts')
   lasses=classes.findall(lass)
   lasse=''.join(lasses)
  except:
   pass
  
  numb=2+i
  s.addstr(numb,2, str(i)+'.', hotkey_attr)
  s.addstr(numb,6, x, curses.A_NORMAL)
  s.addstr(numb,20, host, curses.A_NORMAL)
  s.addstr(numb,35, state, curses.A_NORMAL)
  s.addstr(numb,45, lasse, curses.A_NORMAL)
  s.addstr(numb,70, alert, curses.A_NORMAL)
  i=i+1
 s.refresh()
 c = s.getstr(5,33)
 action=''
# for k,d in device_dict.iteritems():
#  print "%d %s" % (k,d)
  #print device_dict[k]
# s.addstr(0,0, c+"jkl", curses.A_NORMAL)
# s.refresh()
# c = s.getstr(5,33)
 if c in (ord('Q'), ord('q'), curses.KEY_ENTER, 10):
  return
 exec("devs=group_dict[%s]" % c)
 if devs:
  listDevices(devs)
  listGroups()
#  print "FUCK YEAHAHAHAHAHAHAH"
#  x=config.get(devs,'members')
#  mydevs = [v.strip() for v in config.get(devs, 'members').split(',')]
#    try:
#      for member in mydevs:
#       if not member == '':
#        d=findByEc2Ip(member)
#
#       else:
#        newgroup+=member
#     except (AttributeError):
#       pass
#
#  x=findByEc2IP(config.get(dev,'externalip'))
#  cacheDevice(x)
#  manageDevice(x)
#  listDevices()
#  return CONTINUE
# if c in (ord('I'), ord('i'), curses.KEY_ENTER, 10):
#  cfg_dict['type'] = 'INFER'
# elif c in (ord('M'), ord('m')): displayAction('mongod_restart',dev)
 
def listDevices(DEVICES=None):
 global config, device_dict
 classes=re.compile(ZENCLASS+'/([A-Za-z0-9\/]{0,20})')
 devsearch=re.compile('device-')
 text=''
 i=1
 if DEVICES == None:
  for list in config.sections():
   rawtext=''.join(list)
   if devsearch.search(rawtext):
    text+=rawtext+"\n"
    device_dict[i] = rawtext
    i=i+1 
 else:
  device_dict = DEVICES
 s = curses.newwin(40, 90, 5, 3)
 s.box()
 s.addstr(0,1, "Device List", curses.A_BOLD)
 s.addstr(2,6, "Type", curses.A_BOLD)
 s.addstr(2,20, "IP", curses.A_BOLD)
 s.addstr(2,35, "Env", curses.A_BOLD)
 s.addstr(2,45, "Class", curses.A_BOLD)
 s.addstr(2,70, "Alerts", curses.A_BOLD)
 i=1
 stype, host, state, lass, lasses, lasse, alert='','','','','','',''
 device_dict
 for k,d in sorted(device_dict.iteritems(), key=itemgetter(1)):
  #print d
  try:
   stype=config.get(d, 'server-type') 
   host=config.get(d, 'externalip') 
   state=config.get(d, 'state') 
   lass=config.get(d, 'class') 
   alert=config.get(d, 'alerts')
   lasses=classes.findall(lass)
   lasse=''.join(lasses)
  except:
   pass
  
  numb=2+i
  s.addstr(numb,2, str(i)+'.', hotkey_attr)
  s.addstr(numb,6, stype, curses.A_NORMAL)
  s.addstr(numb,20, host, curses.A_NORMAL)
  s.addstr(numb,35, state, curses.A_NORMAL)
  s.addstr(numb,45, lasse, curses.A_NORMAL)
  s.addstr(numb,70, alert, curses.A_NORMAL)
  i=i+1
 s.refresh()
 c = s.getstr(5,33)
 action=''
# for k,d in device_dict.iteritems():
#  print "%d %s" % (k,d)
  #print device_dict[k]
# s.addstr(0,0, c+"jkl", curses.A_NORMAL)
# s.refresh()
# c = s.getstr(5,33)
 if c in (ord('Q'), ord('q'), curses.KEY_ENTER, 10):
  return
 exec("dev=device_dict[%s]" % c)
 if dev:
  x=findByEc2IP(config.get(dev,'externalip'))
  cacheDevice(x)
  manageDevice(x)
  listDevices()
  return CONTINUE
 if c in (ord('I'), ord('i'), curses.KEY_ENTER, 10):
  cfg_dict['type'] = 'INFER'
 elif c in (ord('M'), ord('m')): displayAction('mongod_restart',dev)
  


 
def cacheDevice(d):
    global ec2hostname, ENV, config, DOMAIN
    SECTION='device-'+d.id
    ec2hostname= _performAction('getEc2Hostname',d)
    ENV=prod_dict[d.getProdState()]
    domain=re.compile(ENV + '.' + PROVIDER + '.([A-Za-z0-9]{0,10})')
    domainr=domain.findall(d.snmpSysName)
    DOMAIN=''.join(domainr)
    stypes=re.compile('([A-Za-z0-9]{0,10}).'+ENV + '.' + PROVIDER + '.' + DOMAIN)
    styper=stypes.findall(d.snmpSysName)
    stype=''.join(styper)
    if not config.has_section(SECTION):
     config.add_section(SECTION)
    config.set(SECTION, 'id', d.id)
    config.set(SECTION, 'domain', DOMAIN)
    config.set(SECTION, 'internalip', d.os.interfaces.eth0.getIp())
    config.set(SECTION, 'externalip', d.manageIp)
    config.set(SECTION, 'internalhostname', d.snmpSysName)
    config.set(SECTION, 'externalhostname', d.name())
    config.set(SECTION, 'ec2hostname', ec2hostname.strip())
    config.set(SECTION, 'key', d.zKeyPath)
    config.set(SECTION, 'class', d.getDeviceClassPath())
    config.set(SECTION, 'state', ENV )
    config.set(SECTION, 'comment', d.comments)
    config.set(SECTION, 'lastpuppetsync', '')
    config.set(SECTION, 'timestamp', '')
    config.set(SECTION, 'server-type', stype)
    GROUPSECTION='group-'+DOMAIN+'-'+ENV
    TYPESECTION='group-'+stype+'-'+DOMAIN+'-'+ENV
    if not config.has_section(GROUPSECTION):
     config.add_section(GROUPSECTION)
     config.set(GROUPSECTION, 'members', '')
    if not config.has_section(TYPESECTION):
     config.add_section(TYPESECTION)
     config.set(TYPESECTION, 'members', '')
    mygroup = [v.strip() for v in config.get(GROUPSECTION, 'members').split(',')]
    mytype = [v.strip() for v in config.get(TYPESECTION, 'members').split(',')]
    newgroup = ""
    newtype = ""
    if not d.manageIp in mygroup:
     try:
      for member in mygroup:
       if not member == '':
        newgroup += member+','
       else:
        newgroup+=member
     except (AttributeError):
       pass
     mygroup =newgroup+d.manageIp
     config.set(GROUPSECTION, 'members', mygroup)
    if not d.manageIp in mytype:
     try:
      for member in mytype:
       if not member == '':
        newtype += member+','
       else:
        newtype+=member
     except (AttributeError):
       pass
     mytype =newtype+d.manageIp
     config.set(TYPESECTION, 'members', mytype)
    for key,serv in basic_services.iteritems():
     try:
      p=d.getRRDDataPoint(serv)
      config.set(SECTION, serv, d.getRRDValue(p.getId()))
     except (RuntimeError, TypeError, NameError,AttributeError):
      pass
    exec("omg=%s_services.iteritems()" % stype) 
    for key,serv in omg:
     try: 
      p=d.getRRDDataPoint(serv)
      config.set(SECTION, serv, d.getRRDValue(p.getId()))
     except (RuntimeError, TypeError, NameError,AttributeError):
      pass

    for dev in dmd.ZenEventManager.getDeviceIssues():
     if d.id in dev:
      config.set(SECTION, 'alerts', 'yes')
     else:
      config.set(SECTION, 'alerts', 'no')
      #print "adding to config file for device "+d.id
      config.items(SECTION)

    #with open(CONFIG, 'wb') as configfile:
    #   config.write(configfile)
    try:
     configfile = open(CONFIG, 'wb')
     config.write(configfile)
    except Exception, e:
     print "Could not write config: %s\n" % e
     sys.exit(1)

def initGroups():
 config.add_section('search-haproxy-members')
 config.add_section('memcached-members')
 config.add_section('mongo-replset')
 config.add_section('tfound-prod')
 config.add_section('tfound-qa')
 config.add_section('tfound-dev')
 config.add_section('curiosity-prod')
 config.add_section('curiosity-qa')
 config.add_section('curiosity-dev')
 config.add_section('droz-prod')
 config.add_section('droz-qa')
 config.add_section('droz-dev')
 config.add_section('webandsolr')
 config.add_section('webonly')
 config.add_section('corejobs')
 config.add_section('dailystrength-prod')
 config.add_section('hsw-brazil-prod')
 config.add_section('hsw-china-prod')
 config.add_section('dbs')
 config.add_section('solr')
 config.add_section('dasserver')
 config.add_section('rabbit')
 try:
  configfile = open(CONFIG, 'wb')
  config.write(configfile)
 except Exception, e:
  print "Could not write config: %s\n" % e
  sys.exit(1)

dmd = None
try:
    dmd = ZenScriptBase(connect=True).dmd
except Exception, e:
    print "Connection to zenoss dmd failed: %s\n" % e
    sys.exit(1)

def findByEc2Hostname(hostname):
 for x in dmd.Devices.getSubDevices():
  if hostname == x.snmpSysName or hostname == x.name():
   return x

def findByEc2IP(ip):
 for x in dmd.Devices.getSubDevices():
  if ip == x.manageIp:
   return x
  for i in x.os.interfaces():
   if ip == i.getIp():
    return x 

#-- Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

#-- Define additional constants
EXIT = 0
CONTINUE = 1

#-- Define default conversion dictionary
cfg_dict = {'hostname': 'localhost',
            'ip': '0.0.0.0',
            'type':   'INFER',
            'proxy':  'NONE' }
actions_dict = {'puppetsync': 'Puppetsync','memcached_stop': 'Stop Memcached','memcached_start': 'Start Memcached'}

counter = 0
mode = None

#-- Give screen module scope
screen = None

#-- Create the topbar menu
def topbar_menu(menus):
    left = 2
    for menu in menus:
        menu_name = menu[0]
        menu_hotkey = menu_name[0]
        menu_no_hot = menu_name[1:]
        screen.addstr(1, left, menu_hotkey, hotkey_attr)
        screen.addstr(1, left+1, menu_no_hot, menu_attr)
        left = left + len(menu_name) + 3
        # Add key handlers for this hotkey
        topbar_key_handler((string.upper(menu_hotkey), menu[1]))
        topbar_key_handler((string.lower(menu_hotkey), menu[1]))
    # Little aesthetic thing to display application title
    screen.addstr(1, left-1, 
                  ">"*(52-left)+ " HSWI zenControl",
                  curses.A_STANDOUT) 
    screen.refresh()

#-- Magic key handler both loads and processes keys strokes
def topbar_key_handler(key_assign=None, key_dict={}):
    if key_assign:
        key_dict[ord(key_assign[0])] = key_assign[1]
    else:
        c = screen.getch()
        if c in (curses.KEY_END, ord('!')):
            return 0
        elif c not in key_dict.keys():
            curses.beep()
            return 1
        else:
            return eval(key_dict[c])
#-- Handlers for the topbar menus
def help_func():
    help_lines = []
    offset = 0
    fh_help = open('txt2html.txt')
    for line in fh_help.readlines():
        help_lines.append(string.rstrip(line))
    s = curses.newwin(19, 77, 3, 1)
    s.box()
    num_lines = len(help_lines)
    end = 0
    while not end:
        for i in range(1,18):
            if i+offset < num_lines:
                line = string.ljust(help_lines[i+offset],74)[:74]
            else:
                line = " "*74
                end = 1
            if i<3 and offset>0: s.addstr(i, 2, line, curses.A_BOLD)
            else: s.addstr(i, 2, line, curses.A_NORMAL)
        s.refresh()
        c = s.getch()
        offset = offset+15
    s.erase()
    return CONTINUE

def getStats(d):
# global system, services
# SECTION='device-'+dev.id
# system = [v.strip() for v in config.get(SECTION, 'system').split(',')]
# services = [v.strip() for v in config.get(SECTION, 'services').split(',')]
# return ([ system, services ])
    cigarbox={}
    SECTION='device-'+d.id
    stype=config.get(SECTION, 'server-type')
    for key,serv in basic_services.iteritems():
     try:
      p=d.getRRDDataPoint(serv)
      config.set(SECTION, serv, d.getRRDValue(p.getId()))
      cigarbox[key] = d.getRRDValue(p.getId())
     except (RuntimeError, TypeError, NameError,AttributeError):
      pass
    exec("omg=%s_services.iteritems()" % stype)
    for key,serv in omg:
     try:
      p=d.getRRDDataPoint(serv)
      config.set(SECTION, serv, d.getRRDValue(p.getId()))
      cigarbox[key] = d.getRRDValue(p.getId())
     except (RuntimeError, TypeError, NameError,AttributeError):
      pass
#    print cigarbox
    return cigarbox

def manageDevice(dev):
 global ec2hostname
 screen.addstr(5,4, " "*72, curses.A_NORMAL)
 screen.addstr(8,4, " "*72, curses.A_NORMAL)
 screen.addstr(11,4, " "*72, curses.A_NORMAL)
 screen.addstr(14,4, " "*72, curses.A_NORMAL)
 screen.refresh()
 if config.get('device-'+dev.id, 'alerts') == 'no':
  ALERT='OK'
 else:
  ALERT='Degraded'
 s = curses.newwin(40, 77, 3, 1)
 s.box()
 s.addstr(0,1, "Device Management", curses.A_BOLD)
 s.addstr(2,2, "internal:", curses.A_NORMAL)
 s.addstr(3,3, "ec2hostname", curses.A_NORMAL)
 s.addstr(3,15, ec2hostname, curses.A_BOLD)
 s.addstr(4,3, "ip", curses.A_NORMAL)
 s.addstr(4,15, dev.os.interfaces.eth0.getIp(), curses.A_BOLD)
 s.addstr(5,3, "hostname", curses.A_NORMAL)
 s.addstr(5,15, dev.snmpSysName, curses.A_BOLD)
 s.addstr(6,2, "external:", curses.A_NORMAL)
 s.addstr(7,3, "ip", curses.A_NORMAL)
 s.addstr(7,15, dev.manageIp, curses.A_BOLD)
 s.addstr(8,3, "hostname", curses.A_NORMAL)
 s.addstr(8,15, dev.name(), curses.A_NORMAL)
 s.addstr(9,3, "class:", curses.A_NORMAL)
 s.addstr(9,15, dev.getDeviceClassPath(), curses.A_BOLD)
 s.addstr(10,3, "Status:", curses.A_NORMAL)
 s.addstr(10,15, ALERT, curses.A_BOLD)
 s.addstr(11,3, "Comments:", curses.A_NORMAL)
 s.addstr(11,15, dev.comments, curses.A_BOLD)
 s.addstr(13,2, "Actions", curses.A_BOLD)
 s.addstr(14,3, "R", hotkey_attr)
 s.addstr(14,4, "efresh stats", curses.A_NORMAL)
 s.addstr(15,3, "P", hotkey_attr)
 s.addstr(15,4, "uppetsync", curses.A_NORMAL)
 s.addstr(16,3, "Retest to clear alert", curses.A_NORMAL)
 s.addstr(17,3, "Restart ", curses.COLOR_RED)
 s.addstr(17,11, "A",  hotkey_attr)
 s.addstr(17,12, "pache", curses.COLOR_RED)
 s.addstr(18,3, "Restart ", curses.COLOR_RED)
 s.addstr(18,12, "D", hotkey_attr)
 s.addstr(18,13, "asserver", curses.COLOR_RED)
 s.addstr(19,3, "Restart ", curses.COLOR_RED)
 s.addstr(19,12, "M", hotkey_attr)
 s.addstr(19,13, "ongoD", curses.COLOR_RED)
 s.addstr(20,3, "W", hotkey_attr)
 s.addstr(20,4, "hatami", curses.A_NORMAL)
 stats = getStats(dev)
 i=0
 for key,var in stats.iteritems():
  numb=14+i
  #print var
  s.addstr(numb,30, key+": ", curses.A_BOLD)
  s.addstr(numb,50, str(var), curses.COLOR_RED)
  i=i+1
 numb=22
 s.addstr(numb,2, "Events", curses.A_BOLD)
 e=dmd.ZenEventManager.getEventList()
 i=0
 for k,v in enumerate(e):
  i=i+1
  numb=numb+1
  if v.device == dev.id:
   s.addstr(numb,3, "1. "+v.summary, curses.COLOR_RED)
 
 s.refresh()
 c = s.getch()
 action=''
 if c in (ord('I'), ord('i'), curses.KEY_ENTER, 10):
  cfg_dict['type'] = 'INFER'
 elif c in (ord('M'), ord('m')): displayAction('mongod_restart',dev)
 elif c in (ord('P'), ord('p')): displayAction('puppetsync',dev)
 elif c in (ord('A'), ord('a')): displayAction('apache_restart',dev)
 elif c in (ord('D'), ord('d')): displayAction('dasserver_restart',dev)
 elif c in (ord('R'), ord('r')):
  cacheDevice(dev)
  manageDevice(dev)
 elif c in (ord('W'), ord('w')): displayAction('whatami',dev)
 else: curses.beep()
 s.erase()

def find_func():
    global mode,cfg_dict
    s = curses.newwin(5,15,2,1)
    s.box()
    s.addstr(1,5, "I", hotkey_attr)
    s.addstr(1,2, "by ", menu_attr)
    s.addstr(1,6, "p", menu_attr)
    s.addstr(2,5, "H", hotkey_attr)
    s.addstr(2,2, "by ", menu_attr)
    s.addstr(2,6, "ostname", menu_attr)
    s.addstr(3,2, "L", hotkey_attr)
    s.addstr(3,3, "ist Devices", menu_attr)
    s.addstr(1,2, "", hotkey_attr)
    s.refresh()
    c = s.getch()
    if c in (ord('I'), ord('i'), curses.KEY_ENTER, 10):
        curses.echo()
        s.erase()
	# this blanks the line
        #screen.addstr(5,33, " "*43, curses.A_UNDERLINE)
        screen.addstr(5,33, cfg_dict['ip'], curses.A_UNDERLINE)
        tmpip = screen.getstr(5,33)
        if not tmpip == "":
         cfg_dict['ip'] = tmpip
        else:
         tmpip = cfg_dict['ip']
        curses.noecho()
	found = findByEc2IP(cfg_dict['ip'])
	if found:
         cacheDevice(found)
	 #mode = "device"
#	 SUCCESS = found.manageIp + " "+ found.getDeviceName()
#	 screen.addstr(14, 4," Device found: " + SUCCESS, curses.A_BOLD)
	 manageDevice(found)
    elif c in (ord('H'), ord('h')):
        curses.echo()
        s.erase()
        screen.addstr(8,33, " "*43, curses.A_UNDERLINE)
        cfg_dict['hostname'] = screen.getstr(8,33)
        curses.noecho()
	found = findByEc2Hostname(cfg_dict['hostname'])
	if found:
	 cacheDevice(found)
	 manageDevice(found)
	 #mode = "device"
	 #SUCCESS = found.manageIp
	 #screen.addstr(14, 4," Device found: " + SUCCESS, curses.A_BOLD)
    elif c in (ord('L'), ord('l')):
	listDevices()
    elif c in (ord('T'), ord('t')):
        s.addstr(3,7, "->", menu_attr)
        s.refresh()
        s2 = curses.newwin(8,15,4,10)
        s2.box()
        s2.addstr(1,2, "H", hotkey_attr)
        s2.addstr(1,3, "TML", menu_attr)
        s2.addstr(2,2, "P", hotkey_attr)
        s2.addstr(2,3, "ython", menu_attr)
        s2.addstr(3,2, "F", hotkey_attr)
        s2.addstr(3,3, "AQ", menu_attr)
        s2.addstr(4,2, "S", hotkey_attr)
        s2.addstr(4,3, "mart_ASCII", menu_attr)
        s2.addstr(5,2, "R", hotkey_attr)
        s2.addstr(5,3, "aw", menu_attr)
        s2.addstr(6,2, "I", hotkey_attr)
        s2.addstr(6,3, "nfer Type", menu_attr)
        s2.addstr(6,2, "", hotkey_attr)
        s2.refresh()
        c = s2.getch()
        if c in (ord('I'), ord('i'), curses.KEY_ENTER, 10):
            cfg_dict['type'] = 'INFER'
        elif c in (ord('H'), ord('h')): cfg_dict['type'] = 'HTML'
        elif c in (ord('P'), ord('p')): cfg_dict['type'] = 'PYTHON'
        elif c in (ord('F'), ord('f')): cfg_dict['type'] = 'FAQ'
        elif c in (ord('S'), ord('s')): cfg_dict['type'] = 'SMART_ASCII'
        elif c in (ord('R'), ord('r')): cfg_dict['type'] = 'RAW'
        else: curses.beep()
        s2.erase()
        s.erase()
    else:
        curses.beep()
        s.erase()
    return CONTINUE

def doit_func():
    global counter
    counter = counter+1
    if cfg_dict['type'] == 'INFER':
        cfg_dict['type'] = dmTxt2Html.infer_type(cfg_dict['source'])
    dmTxt2Html.main(cfg_dict)
    return CONTINUE

def proxy_func():
    s = curses.newwin(6, 15, 2, 8)
    s.box()
    s.addstr(1, 2, "P", hotkey_attr)
    s.addstr(1, 3, "roxy Bar", menu_attr)
    s.addstr(2, 2, "T", hotkey_attr)
    s.addstr(2, 3, "rap Links", menu_attr)
    s.addstr(3, 2, "A", hotkey_attr)
    s.addstr(3, 3, "ll Proxyes", menu_attr)
    s.addstr(4, 2, "N", hotkey_attr)
    s.addstr(4, 3, "o Proxies", menu_attr)
    s.addstr(4, 2, "", hotkey_attr)
    s.refresh()
    c = s.getch()
    s.erase()
    if c in (ord('N'), ord('n'), curses.KEY_ENTER, 10):
        cfg_dict['proxy'] = 'NONE'
    elif c in (ord('P'), ord('p')): cfg_dict['proxy'] = 'NAVIGATOR'
    elif c in (ord('T'), ord('t')): cfg_dict['proxy'] = 'TRAP_LINKS'
    elif c in (ord('A'), ord('a')): cfg_dict['proxy'] = 'ALL'
    else: curses.beep()
    return CONTINUE


#-- Display the currently selected options
def draw_dict():
 global mode
 if mode == "device":
    s = curses.newwin(19, 77, 3, 1)
    s.box()
    s.addstr(14,33, "LOL"*43, curses.A_NORMAL)
    s.refresh()
 elif mode == "group":
    screen.refresh()
 else:
    screen.addstr(5,33, " "*43, curses.A_NORMAL)
    screen.addstr(8,33, " "*43, curses.A_NORMAL)
    screen.addstr(11,33, " "*43, curses.A_NORMAL)
    screen.addstr(14,33, " "*43, curses.A_NORMAL)
    screen.addstr(5, 33, cfg_dict['ip'], curses.A_STANDOUT)
    screen.addstr(8, 33, cfg_dict['hostname'], curses.A_STANDOUT)
    screen.addstr(11,33, cfg_dict['type'], curses.A_STANDOUT)
    screen.addstr(14,33, cfg_dict['proxy'], curses.A_STANDOUT)
    screen.addstr(17,33, str(counter), curses.A_STANDOUT)
    screen.refresh()
    


#-- Top level function call (everything except [curses] setup/cleanup)
def main(stdscr):
    # Frame the interface area at fixed VT100 size
    global screen
    #screen = stdscr.subwin(23, 79, 0, 0)
    screen = stdscr.subwin(0,0,0,0)
    screen.box()
    screen.hline(2, 1, curses.ACS_HLINE, 77)
    screen.refresh()

    # Define the topbar menus
    find_menu = ("Find Device", "find_func()")
    groups_menu = ("Manage Groups", "listGroups()")
    doit_menu = ("AWS Actions", "doit_func()")
    help_menu = ("Help", "help_func()")
    exit_menu = ("Exit", "EXIT")

    # Add the topbar menus to screen object
    topbar_menu((find_menu, groups_menu, doit_menu, help_menu, exit_menu))

    # Draw the onscreen field titles
    screen.addstr(5, 4, "                Ip Address:", curses.A_BOLD)
    screen.addstr(8, 4, "                  Hostname:", curses.A_BOLD)
    #screen.addstr(11, 4,"           Conversion Type:", curses.A_BOLD)
    #screen.addstr(14, 4,"                Proxy Mode:", curses.A_BOLD)
    #screen.addstr(17, 4,"Conversions during Session:", curses.A_BOLD)
    screen.addstr(1, 77, "", curses.A_STANDOUT)
    draw_dict()
  
    # Enter the topbar menu loop
    while topbar_key_handler():
        draw_dict()


if __name__=='__main__':
    try:
        # Initialize curses
        stdscr=curses.initscr()
        #curses.start_color()
        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho() ; curses.cbreak()

        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        stdscr.keypad(1)
        main(stdscr)                    # Enter the main loop
        # Set everything back to normal
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()                 # Terminate curses
    except:
        # In the event of an error, restore the terminal
        # to a sane state.
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
        traceback.print_exc()           # Print the exception


