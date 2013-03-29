<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" >
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta id="viewport" name="viewport" content="width=320; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;" />
	<title>$title</title>
	<link rel="stylesheet" href="/stylesheets/iphone.css" />
	<link rel="apple-touch-icon" href="/images/apple-touch-icon.png" />
	<script type="text/javascript" src="/js/smartphonedetect.js"></script>
	<script type="text/javascript" charset="utf-8">
		window.onload = function() {
		  setTimeout(function(){window.scrollTo(0, 1);}, 100);
		}
	</script>
</head>
<body>
	
	<div id="header">
		<h1>$title</h1>
		<a href="/index" id="backButton" onclick="showhide('waitdiv');" >Index</a>
	</div>
	<div id="waitcenter">
  		<div id="waitdiv"> 
  			<div class="bar1"></div> 
  			<div class="bar2"></div> 
  			<div class="bar3"></div> 
  			<div class="bar4"></div> 
  			<div class="bar5"></div> 
  			<div class="bar6"></div> 
  			<div class="bar7"></div> 
  			<div class="bar8"></div> 
		</div> 		
	</div>	
	<h1>These are all the devices I know about. Choose one:</h1>
	
	<ul>
	  <li class="arrow" py:for="key in device">
        <?python
        if device[key]['state'] == 'prod':
        	IMG='list-icon-1.png'
        elif device[key]['state'] == 'qa':
        	IMG='list-icon-2.png'
        else:
        	IMG='list-icon-3.png'
        print "working on key %s" % key
        ?>
        <a href="/devices/get/${device[key]['sectionid']}" onclick="showhide('waitdiv');"><img src="/images/${IMG}" class="ico" />${device[key]['ec2hostname']}</a>
        ${device[key]['comment']}
      </li>
	</ul>
	
<p>&copy; 2011 Syspimp</p>
	
</body>
</html>