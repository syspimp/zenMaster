class actions():
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


