import Globals, sys, curses, traceback, string, os, re, time, ConfigParser
from zenconf import configdicts

class groups():
    def __init__(self):
	self.current_dir = os.path.dirname(os.path.abspath(__file__))+'/../'
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(open(os.path.join(self.current_dir, configdicts.DEVGRPCACHE)))
        self.device_dict={}
        self.group_dict={}
        
    def listGroups(self):
        #global config, group_dict
        #classes=re.compile('/Server/SSH/Linux/([A-Za-z0-9\/]{0,20})')
        devsearch=re.compile('group-')
        text=''
        i=1
        for list in self.config.sections():
            rawtext=''.join(list)
            if devsearch.search(rawtext):
                text+=rawtext+"\n"
                self.group_dict[i] = rawtext
                i=i+1
	    #print "Sorting ..."
	    #self.group_dict
	    items = [(v, k) for k, v in self.group_dict.items()]
        items.sort()
        items.reverse() 
        i=1
        for val in items:
            self.group_dict[i] = val[0]
            i=i+1
        return self.group_dict

    def _splitMembers(self,GROUPSECTION):
        return [v.strip() for v in self.config.get(GROUPSECTION, 'members').split(',')]
    
    def getGroup(self,GROUP=None):
        '''
        returns the appropiate section from the config
        '''
        football = {}
        if self.config.has_section(GROUP):
            for opt in self.config.options(GROUP):
                football[opt] = self.config.get(GROUP,opt)
            football['members'] = self._splitMembers(GROUP)
        return football
            
    
    def doGroupAction(self,GROUP=None):
        return
    def doThreadedGroupAction(self,NUMBER_THREADS='2'):
        return
