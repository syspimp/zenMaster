#import Globals, sys, curses, traceback, string, os, re, time, ConfigParser
import sys, curses, traceback, string, os, re, time, ConfigParser
sys.path.append('/data/zenoss/Products')
from Products.ZenUtils.ZenScriptBase import ZenScriptBase

class events():
    def __init__(self):
        self.dmd = None
        try:
            self.dmd = ZenScriptBase(connect=True).dmd
        except Exception, e:
            print "Connection to zenoss dmd failed: %s\n" % e
            #sys.exit(1)
    def getEvent(self,evid=None):
        if evid != None:
            events = {}
            i=1
#            for dev in self.dmd.ZenEventManager.getEventList():
#               if evid == dev.evid:
#                    events[i]={}
#                    events[i]['device'] = dev.device
#                    events[i]['summary'] = dev.summary
#                    events[i]['evid'] = dev.evid
#                    events[i]['component'] = dev.component
#                    events[i]['eventclass'] = dev.eventClass
#                    events[i]['eventstate'] = dev.eventState
#                    events[i]['count'] = dev.count
#                    events[i]['firsttime'] = dev.firstTime
#                    events[i]['lasttime'] = dev.lastTime
#                    events[i]['severity'] = dev.severity
#                    i=i+1
            return events
    
    def getDeviceEvents(self,devid=None):
        if devid != None:
            events = {}
            i=1
            from handlers import zenossapi
            z=zenossapi.zenossapi()
            events=z.get_events(devid)
            print "getDeviceEvents: %s" % events
#            for dev in self.dmd.ZenEventManager.getEventList():
#                if devid == dev.device:
#                    events[i]={}
#                    events[i]['summary'] = dev.summary
#                    events[i]['evid'] = dev.evid
#                    events[i]['device'] = dev.device
#                    events[i]['component'] = dev.component
#                    events[i]['eventclass'] = dev.eventClass
#                    events[i]['eventstate'] = dev.eventState
#                    events[i]['count'] = dev.count
#                    events[i]['firsttime'] = dev.firstTime
#                    events[i]['lasttime'] = dev.lastTime
#                    events[i]['severity'] = dev.severity
#                    i=i+1
            return events
        
    def listEvents(self):
        '''
        returns integer index of events
        '''
        events = {}
	football = {}
        i=1
        from handlers import zenossapi
        z=zenossapi.zenossapi()
        events=z.get_events()
        print "events.ListEvents.events: %s" % events
        for event in events['events']:
            temp=z.get_event(event['evid'])
            football[i]=temp['events']
            i=i+1
        print "events.listEvents.football: %s" % football 
#        for dev in self.dmd.ZenEventManager.getEventList():
#            events[i]={}
#            events[i]['device'] = dev.device
#            events[i]['summary'] = dev.summary
#            events[i]['evid'] = dev.evid
#            events[i]['component'] = dev.component
#            events[i]['eventclass'] = dev.eventClass
#            events[i]['eventstate'] = dev.eventState
#            events[i]['count'] = dev.count
#            events[i]['firsttime'] = dev.firstTime
#            events[i]['lasttime'] = dev.lastTime
#            events[i]['severity'] = dev.severity
#            i=i+1
        return events
    def ackDeviceEvent(self,evid=None):
        if evid != None: 
            return self.dmd.Events.manage_ackEvents(evid)
    def closeEvent(self,evid=None):
        if evid != None:
            from handlers import zenossapi
            z=zenossapi.zenossapi()
            z.close_event(evid)
        return
    def createDeviceEvent(self,devid=None,severity=None,summary=None):
        if devid != None:
            from handlers import zenossapi
            z=zenossapi.zenossapi()
            z.create_event_on_device(devid,severity,summary)
        return
