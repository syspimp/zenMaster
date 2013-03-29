'''
        this goes into curses handler
        s = curses.newwin(40, 90, 5, 3)
        s.box()
        s.addstr(0,1, "Device List", curses.A_BOLD)
        s.addstr(2,6, "Type", curses.A_BOLD)
        s.addstr(2,20, "IP", curses.A_BOLD)
        s.addstr(2,35, "Env", curses.A_BOLD)
        s.addstr(2,45, "Class", curses.A_BOLD)
        s.addstr(2,70, "Alerts", curses.A_BOLD)
        
        device_dict
        
        stype, host, state, lass, lasses, lasse, alert='','','','','','',''
        i=1
        for k,d in sorted(device_dict.iteritems(), key=itemgetter(1)):
            #print d
            try:
                stype=self.config.get(d, 'server-type')
                host=self.config.get(d, 'externalip')
                state=self.config.get(d, 'state')
                lass=self.config.get(d, 'class')
                alert=self.config.get(d, 'alerts')
                # make class easy to read
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
                #  print "FUCK YEAHAHAHAHAHAHAH"
                x=findByEc2IP(config.get(dev,'externalip'))
                cacheDevice(x)
                manageDevice(x)
                listDevices()
                return CONTINUE
            if c in (ord('I'), ord('i'), curses.KEY_ENTER, 10):
                cfg_dict['type'] = 'INFER'
            elif c in (ord('M'), ord('m')): displayAction('mongod_restart',dev)
            '''
            
            
'''
def manageDevice(self,dev):
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
 e=self.dmd.ZenEventManager.getEventList()
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
'''