# Zenoss-3.0.x JSON API Example (python)
#
# To quickly explore, execute 'python -i api_example.py'
#
# >>> z = ZenossAPIExample()
# >>> events = z.get_events()
# etc.

#import sys, os
#sys.path.append(os.path.abspath('../../'))
#from zenmaster.conf import conf

import json
import urllib
import urllib2

ZENOSS_INSTANCE = 'http://localhost:8080'
ZENOSS_USERNAME = 'admin'
ZENOSS_PASSWORD = 'n0t1ck3t'
ENV='dev'
PROJECT='tfound'

ROUTERS = { 'MessagingRouter': 'messaging',
            'EventsRouter': 'evconsole',
            'ProcessRouter': 'process',
            'ServiceRouter': 'service',
            'DeviceRouter': 'device',
            'NetworkRouter': 'network',
            'TemplateRouter': 'template',
            'DetailNavRouter': 'detailnav',
            'ReportRouter': 'report',
            'MibRouter': 'mib',
            'ZenPackRouter': 'zenpack' }

class zenossapi:
    def __init__(self, debug=True):
        """
        Initialize the API connection, log in, and store authentication cookie
        """
        # Use the HTTPCookieProcessor as urllib2 does not save cookies by default
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        if debug: self.urlOpener.add_handler(urllib2.HTTPHandler(debuglevel=1))
        self.reqCount = 1

        # Contruct POST params and submit login.
        loginParams = urllib.urlencode(dict(
                        __ac_name = ZENOSS_USERNAME,
                        __ac_password = ZENOSS_PASSWORD,
                        submitted = 'true',
                        came_from = ZENOSS_INSTANCE + '/zport/dmd'))
        self.urlOpener.open(ZENOSS_INSTANCE + '/zport/acl_users/cookieAuthHelper/login',
                            loginParams)

    def _router_request(self, router, method, data=[]):
        if router not in ROUTERS:
            raise Exception('Router "' + router + '" not available.')

        # Contruct a standard URL request for API calls
        req = urllib2.Request(ZENOSS_INSTANCE + '/zport/dmd/' +
                              ROUTERS[router] + '_router')

        # NOTE: Content-type MUST be set to 'application/json' for these requests
        req.add_header('Content-type', 'application/json; charset=utf-8')

        # Convert the request parameters into JSON
        reqData = json.dumps([dict(
                    action=router,
                    method=method,
                    data=data,
                    type='rpc',
                    tid=self.reqCount)])

        # Increment the request count ('tid'). More important if sending multiple
        # calls in a single request
        self.reqCount += 1

        # Submit the request and convert the returned JSON to objects
        dump=json.loads(self.urlOpener.open(req, reqData).read())
	print "zenossapi._router_request = %s" % reqData
	print "zenossapi._router_result = %s" % dump

        #return json.loads(self.urlOpener.open(req, reqData).read())
	return dump
    
    def do_action(self, command='whatami', deviceClass='/zport/dmd/Devices'):
        self.create_event_on_device(deviceClass, 'Info', 'Test action from WebUI')
	req = urllib2.Request(ZENOSS_INSTANCE + deviceClass + '/run_command')
        # Convert the request parameters into JSON
	data = {"uids":[deviceClass],"command":command}
        #reqData = json.dumps([dict(
	#		data=data,
	#		)])
	reqData = urllib.urlencode(data)
	dump=self.urlOpener.open(req, reqData).read()
	dump
	return dump

        #dump=self._router_request('DeviceRouter', 'getUserCommands',
	#			data=[{'uid': deviceClass}])
	#return dump
        #return self._router_request('DeviceRouter', 'getUserCommands',
        #                            data=[{'uid': deviceClass, 'get': command}])['result']
                                    
    def get_devices(self, deviceClass='/zport/dmd/Devices', prodstate=None):
	if prodstate==None:
		prodstate=['Production','Development','QA']
	data = dict(uid=deviceClass)
	data['params'] = dict(productionState=prodstate)
        return self._router_request('DeviceRouter', 'getDevices',
                                    data=[{'uid': deviceClass}, {'params': {'productionState': prodstate }}])['result']
    def get_event(self, evid=None, component=None, eventClass=None):
        data = dict(start=0, limit=100, dir='DESC', sort='severity')
        data['keys'] = ['eventState', 'severity', 'component', 'eventClass', 'summary', 'firstTime', 'lastTime', 'count', 'evid', 'eventClassKey', 'message']
        data['params'] = dict(severity=[5,4,3,2], eventState=[0,1])

        if component: data['params']['component'] = component
        if eventClass: data['params']['eventClass'] = eventClass
        if evid: data['params']['evid'] = evid

        return self._router_request('EventsRouter', 'query', [data])['result']


    def get_events(self, device=None, component=None, eventClass=None, evid=None):
        data = dict(start=0, limit=100, dir='DESC', sort='severity')
        data['keys'] = ['eventState', 'severity', 'component', 'eventClass', 'summary', 'firstTime', 'lastTime', 'count', 'evid', 'eventClassKey', 'message']
        data['params'] = dict(severity=[5,4,3,2], eventState=[0,1])

        if device: data['params']['device'] = device
        if component: data['params']['component'] = component
        if eventClass: data['params']['eventClass'] = eventClass
        if evid: data['params']['evid'] = evid

        return self._router_request('EventsRouter', 'query', [data])['result']

    def add_device(self, deviceName, deviceClass):
        data = dict(deviceName=deviceName, deviceClass=deviceClass)
        return self._router_request('DeviceRouter', 'addDevice', [data])

    def create_event_on_device(self, device, severity, summary):
        if severity not in ('Critical', 'Error', 'Warning', 'Info', 'Debug', 'Clear'):
            raise Exception('Severity "' + severity +'" is not valid.')

        data = dict(device=device, summary=summary, severity=severity,
                    component='', evclasskey='', evclass='')
        return self._router_request('EventsRouter', 'add_event', [data])

    def close_event(self, evid):
        data = dict(evids=[evid])
        return self._router_request('EventsRouter', 'close', [data])
    
    def IntToDottedIP(self, intip):
        if intip is None:
            return
        octet = ''
        for exp in [3,2,1,0]:
            octet = octet + str(intip / ( 256 ** exp )) + "."
            intip = intip % ( 256 ** exp )
        return(octet.rstrip('.'))
    def setEnv(self, env):
        self.ENV=env
        return
