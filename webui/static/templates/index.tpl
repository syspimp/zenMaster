<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta id="viewport" name="viewport" content="width=320; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;" />
	<title>$title</title>
	<link rel="stylesheet" href="stylesheets/iphone.css" />
	<link rel="apple-touch-icon" href="images/apple-touch-icon.png" />
	<script type="text/javascript" src="/js/smartphonedetect.js"></script>
	<script type="text/javascript" charset="utf-8">
		window.onload = function() {
		  setTimeout(function(){window.scrollTo(0, 1);}, 100);
		  if(detectAllPhones())
		  {
			//window.location = "http://zenoss.yourdomain.com/";
		  }
		}
	</script>
</head>

<body>
	
	<div id="header">
		<h1>$title</h1>
	</div>
	
	<h1>zenMaster WebUI $version</h1>
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
	<ul>
		<li class="arrow"><a href="/devices" onclick="showhide('waitdiv');">Devices</a></li>
		<li class="arrow"><a href="/groups" onclick="showhide('waitdiv');">Groups</a></li>
		<li class="arrow"><a href="/events" onclick="showhide('waitdiv');">Events</a></li>
		<li class="arrow"><a href="/aws" onclick="showhide('waitdiv');">AWS</a></li>
		<li class="arrow"><a href="/puppet" onclick="showhide('waitdiv');">Puppet</a></li>
		<li class="arrow"><a href="#" onclick="showhide('waitdiv');">Test</a></li>
	</ul>
	
	<ul class="data">
		<li><p>Choose a section to manage. You can see a listing of what's available, or create a new entry.</p></li>
	</ul>
	
<p>&copy; 2010 Syspimp</p>

	
	
</body>
</html>
