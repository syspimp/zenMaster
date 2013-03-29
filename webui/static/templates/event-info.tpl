<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta id="viewport" name="viewport" content="width=320; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;" />
	<title>$title</title>
	<link rel="stylesheet" href="/stylesheets/iphone.css" />
	<link rel="apple-touch-icon" href="/images/apple-touch-icon.png" />
	<script language="javascript"> 
	<!--
	var state = 'none';
 
	function showhide(layer_ref) {
 
	if (state == 'block') { 
	state = 'none'; 
	} 
	else { 
	state = 'block'; 
	} 
	if (document.getElementById &&!document.all) { 
	hza = document.getElementById(layer_ref); 
	hza.style.display = state; 
	} 
	} 
	//--> 
	</script> 
	<script type="text/javascript" charset="utf-8">
		window.onload = function() {
		  setTimeout(function(){window.scrollTo(0, 1);}, 100);
		}
	</script>
	<!-- for profile image -->
	<style type="text/css" media="screen">
		li.picture { background: #fff url(/images/server.png) no-repeat !important; }
	</style>
	<!-- end line customization -->
</head>

<body>
	
	<div id="header">
		<h1>$title</h1>
		<a href="javascript:history.go(-1)" id="backButton">Back</a>
	</div>

<h1>Event Information</h1>


<ul>
	<li py:for="key in events">
	<?python
	ack=''
	if events[key]['eventstate'] != 1:
		ack = 'Not acknowledged'
	?>
	<a href="/events/ack/${events[key]['evid']}"><small class="counter">${events[key]['count']}</small>${events[key]['summary']}</a>
	<a href="/events/ack/${events[key]['evid']}">${events[key]['component']} ${events[key]['eventclass']}</a>
	<a href="/events/ack/${events[key]['evid']}">First Time: ${events[key]['firsttime']}<br /> Last Time ${events[key]['lasttime']} ${ack}</a>
	</li>
</ul>
	<p><a href="#" class="green button" onclick="showhide('optionpanel');">Event Options</a></p>
	<div id="optionpanel" style="display: none">
	<p>
	 <a class="white button" href="/events/ack/${events[1]['evid']}">Acknowledge</a>
	 <a class="white button" href="/events/clear/${events[1]['evid']}">Clear</a>
	 <a class="white button" href="/devices/get/device-${events[1]['device']}">Go To Device</a>
     <a href="#" class="red button" onclick="showhide('optionpanel');">Hide</a> 
     <a class="black button" href="/events">Back to Events</a></p> 
    </div>
    
<p>&copy; 2011 Syspimp</p>
</body>
</html>