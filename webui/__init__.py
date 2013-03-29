import Globals
import cherrypy
import os.path
import sys
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append('/data/zenoss')
from handlers import devices, events, groups
from genshi.template import TemplateLoader

# user auth stuff
# this needs to be changed to something more robust
users = {"admin": ""}

def clear_text(mypass):
    return mypass

class Root:
    @cherrypy.expose
    def __init__(self):
        '''
        webui is a cherrypy wrapper to access the
        zenmaster framework
        '''
        self.version = "1.0"
        self.dev=devices.devices()
        # update ini device cache
        self.dev.refreshDeviceList()
        self.grp=groups.groups()
        self.evt=events.events()
        self.title = 'zenMaster '+self.version
        
    def command(self,dev=None,action=None):
        '''
        runs a command on a device
        '''
        d={}
        doaction=''
        if action != None and dev != None:   
            	try:
                	print "Command: Calling Perform action %s on %s" % (action,dev)
                	doaction=self.dev.performAction(action,dev)
			print "Command: %s output: %s" % (action,doaction)
			d=doaction
			self.title="Run Command on %s" % dev
                	tpl='command.tpl'
           	except (UnboundLocalError,Exception,AttributeError), e:
                	msg="Command: EXCEPTION CAUGHT in action "+action+" on device "+dev
			print "dumping exceptions..."
			for i in e:
				print i
			print "%s" % e
			d=msg+" \n"+e.__str__()
			self.title='Exception Caught'
			tpl='error.tpl'
                	pass
        else:
                z=self.dev.listDevices()
                for val in z:
                    '''
                    set the vars expected in template
                    val is an integer
                    '''
                    print "Looping thru, seeting list to give to template, val %s, dev %s" % (val,self.dev.getDevice(z[val]))
                    d[val] = self.dev.getDevice(z[val])
                print "whole listdev stack %s" % z
                tpl='device-icon-list.tpl'
                self.title='Device List'
        tmpl = loader.load(tpl)
        return tmpl.generate(title=self.title,device=d).render('html', doctype='html')

    def aws(self,service=None,action=None,id=None):
        '''
        lists actions on a aws service or performs actions
        '''
        if service == 'autoscaling':
            if action != None and id != None:
                print
            else:
                tpl='autoscaling-list.tpl'
            
            #try:
            e=self.evt.getEvent(evid)
            #d['commands'] = self.dev.getCommands(d['server-type'])
            print "event array: %s" % e
            self.title='Event'
            tpl='event-info.tpl'
            #except (UnboundLocalError,Exception,AttributeError,UndefinedError), e:
            #    pass
        elif service == 'elb' and evid != None:
            #try:
                e=self.evt.getEvent(evid)
                self.evt.ackDeviceEvent(evid)
                self.title='Acknowledged Event for %s' % e[1]['summary']
                tpl='event-info.tpl'
            #except (UnboundLocalError,Exception,AttributeError), ex:
                #print "got an exception, dont know what it was tho, so heres the event stack: %s" % e
                #print "oh, found the exception %s" % ex
        elif service == 'instances' and evid != None:
            #try:
                e=self.evt.getEvent(evid)
                self.evt.closeEvent(evid)
                self.title='Cleared Event for %s' % e[1]['summary']
                tpl='event-info.tpl'
            #except (UnboundLocalError,Exception,AttributeError), ex:
                #print "got an exception, dont know what it was tho, so heres the event stack: %s" % e
                #print "oh, found the exception %s" % ex
        else:
                e=self.evt.listEvents()
                #print "ok, here are the events %s" % z
                tpl='event-icon-list.tpl'
                self.title='Event List'

        
        tmpl = loader.load('aws-choose-list.tpl')
        return tmpl.generate(title='zenMaster: AWS',
                             version=self.version).render('html', doctype='html')
      
    def index(self):
        tmpl = loader.load('index.tpl')
        return tmpl.generate(title='zenMaster: at one',
                             version=self.version).render('html', doctype='html')
    def events(self,action=None,evid=None):
        '''
        lists all events, gets one event, or acks an event
        '''
        e={}
        if action == 'get' and evid != None:
            
 #           try:
                e=self.evt.getEvent(evid)
                #d['commands'] = self.dev.getCommands(d['server-type'])
                if len(e) > 0:
                    print "event array: %s" % e
                    self.title='Event'
                    tpl='event-info.tpl'
                else:
                    e=self.evt.listEvents()
                    #print "ok, here are the events %s" % z
                    tpl='event-icon-list.tpl'
                    self.title='Event Not Found'
#            except (UnboundLocalError,Exception,AttributeError,UndefinedError), e:
#                e=self.evt.listEvents()
#                #print "ok, here are the events %s" % z
#                tpl='event-icon-list.tpl'
#                self.title='Event Not Found'
        elif action == 'ack' and evid != None:
            #try:
                e=self.evt.getEvent(evid)
                self.evt.ackDeviceEvent(evid)
                self.title='Acknowledged Event for %s' % e[1]['summary']
                tpl='event-info.tpl'
            #except (UnboundLocalError,Exception,AttributeError), ex:
                #print "got an exception, dont know what it was tho, so heres the event stack: %s" % e
                #print "oh, found the exception %s" % ex
        elif action == 'clear' and evid != None:
            #try:
                e=self.evt.getEvent(evid)
                self.evt.closeEvent(evid)
                self.title='Cleared Event for %s' % e[1]['summary']
                tpl='event-info.tpl'
            #except (UnboundLocalError,Exception,AttributeError), ex:
                #print "got an exception, dont know what it was tho, so heres the event stack: %s" % e
                #print "oh, found the exception %s" % ex
        else:
                e=self.evt.listEvents()
                #print "ok, here are the events %s" % z
                tpl='event-icon-list.tpl'
                self.title='Event List'

        tmpl = loader.load(tpl)
        return tmpl.generate(title=self.title,events=e,version=self.version).render('html', doctype='html')

    def devices(self,action=None,dev=None):
        '''
        lists all devices, or gets one device
        '''
        d={}
        if action == 'get' and dev != None:
            
#            try:
	     print "Getting device: %s" % dev
             d=self.dev.getDevice(dev)
             #self.dev.refreshDevice(d)
             #d['commands'] = self.dev.getCommands(d['server-type'])
             print "device array: %s" % d
             tpl='device-info.tpl'
#            except (UnboundLocalError,Exception,AttributeError,UndefinedError), e:
# 			msg="Command: EXCEPTION CAUGHT:"
#			print "dumping exceptions..."
#			for i in e:
#				print i
#			print "%s" % e
#			d=msg+" \n"+e.__str__()
#			self.title='Exception Caught'
#			tpl='error.tpl'
#                	pass
        elif action == 'set' and dev != None:
            try:
                print
            except:
                pass
        else:
                z=self.dev.listDevices()
                for val in z:
                    '''
                    set the vars expected in template
                    val is an integer
                    '''
                    print "Looping thru, seeting list to give to template, val %s, dev %s" % (val,self.dev.getDevice(z[val]))
                    d[val] = self.dev.getDevice(z[val])
                print "whole listdev stack %s" % z
                tpl='device-icon-list.tpl'
                self.title='Device List'
        tmpl = loader.load(tpl)
        return tmpl.generate(title=self.title,device=d).render('html', doctype='html')

    def groups(self,action=None,group=None):
        '''
        gets all groups, or returns one group
        ''' 
        d={}
        if action == 'get' and group != None:
            
            i=1
            #try:
            z=self.grp.getGroup(group)
            '''
            this  loop is different from the device loop
            becuz val is a deviceid
            '''
            for val in z['members']:
                d[i] = self.dev.getDevice(val)
                i=i+1
            tpl='device-icon-list.tpl'
            self.title='Group '+z['name']
            #except (UnboundLocalError,Exception,AttributeError), e:
            #    pass
        elif action == 'set' and group != None:
            try:
                print
            except:
                pass
        else:
            try:
                z=self.grp.listGroups()
                for val in z:
                    try:
                        d[val]= {'sectionid': self.grp.getGroup(z[val])['sectionid'],
                                 'name': self.grp.getGroup(z[val])['name'],
                                 'members': self.grp.getGroup(z[val])['members']}
                    except:
                        pass
                tpl='group-icon-list.tpl'
                self.title='Group List'
            except (UnboundLocalError,Exception,AttributeError), e:
                print "Exception: %s" % e
                pass
        tmpl = loader.load(tpl)
        return tmpl.generate(title=self.title,device=d).render('html', doctype='html')
    events.exposed = True
    groups.exposed = True
    devices.exposed = True
    index.exposed = True
    aws.exposed = True
    command.exposed = True
    command._cp_config = {'tools.basic_auth.on': True,
        'tools.basic_auth.realm': 'Execute Commands. Enter the root user and pass.',
        'tools.basic_auth.users': users,
        'tools.basic_auth.encrypt': clear_text}
    
if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    loader = TemplateLoader(os.path.join(os.path.dirname(__file__), 'static/templates'),
                            auto_reload=True)

        # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': 'site.log',
                            'log.screen': True,
                            'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8000})
    conf = {'/': {'tools.staticdir.root': os.path.join(current_dir, 'static'),
                  'tools.sessions.on': True,
                  'tools.sessions.storage_type':  "file",
                  'tools.sessions.storage_path':  os.path.join(current_dir, 'sessions'),
                  'tools.sessions.timeout': 60},
            '/images': {'tools.staticdir.on': True,
                        'tools.staticdir.dir': 'images'},
            '/stylesheets': {'tools.staticdir.on': True,
                             'tools.staticdir.dir': 'stylesheets'},
            '/html': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': 'html'},
            '/js': {'tools.staticdir.on': True,
                        'tools.staticdir.dir': 'js'},
            }
    
    #cherrypy.config.update(current_dir+'/../zenconf/webui.conf')
    cherrypy.quickstart(Root(), '/', config=conf)
