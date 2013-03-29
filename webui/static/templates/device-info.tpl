<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/">
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
	<!-- for profile image -->
	<style type="text/css" media="screen">
		li.picture { background: #fff url(/images/server.png) no-repeat !important; }
	</style>
	<!-- end line customization -->
</head>

<body>
	
	<div id="header">
		<h1>Device Information</h1>
		<a href="javascript:history.go(-1)" id="backButton">Back</a>
	</div>

<h1>${device['ec2hostname']}</h1>

<ul class="profile">
	<li class="picture"><a href="ssh://${device['externalip']}">Device</a></li>
	<li class="clearfix"><h2>${device['domain']}</h2><p>${device['state']} ${device['server-type']}</p></li>
</ul>

<ul class="field">
	<li><h3>External Ip</h3> <a href="ssh://${device['externalip']}">${device['externalip']}</a></li>
	<?python
	comments = 'None'
	if device['comment'] != '':
		comments = device['comment']
	?>
	<li><h3>Comment</h3> <a href="#">${comments}</a></li>
	<li py:for="key in device['services']"><?python
	
	try:
		srvkey=device['services'][key]
		srvkey=srvkey.lower()
		stat=device[srvkey]
	except:
		stat='None'
	?><h3>${key}</h3> <a href="#">${stat}</a></li>
	<?python
	url =''
	name = ''
	if device['server-type'] == 'web' or device['server-type'] == 'webonly': 
	 url = 'http://'+device['ec2hostname']+'/server-status'
	 name = 'Go to Apache Server Status'
	elif device['server-type'] == 'docbase1':
	 url = 'http://'+device['ec2hostname']+':28018'
	 name = 'Go to Mongo Rest API'
	elif device['server-type'] == 'search':
	 url = 'http://'+device['ec2hostname']+':8080/das'
	 name = 'Go to Das API'
	?>
	<li><a href="${url}">${name}</a></li>
</ul>

<h1>Events</h1>
<ul>
	<li py:for="key in device['events']">
	<a href="/events/get/${device['events'][key]['evid']}"><small class="counter">${device['events'][key]['count']}</small>${device['events'][key]['summary']}</a>
	<a href="/events/get/${device['events'][key]['evid']}">${device['events'][key]['component']} ${device['events'][key]['eventclass']}</a>
	<a href="/events/get/${device['events'][key]['evid']}">First Time: ${device['events'][key]['firsttime']}<br /> Last Time ${device['events'][key]['lasttime']}</a>
	</li>
</ul>
	<p><a href="#" class="green button" onclick="showhide('optionpanel');">Device Commands</a></p>
	<div id="optionpanel" style="display: none">
	<p>
	<span py:for="key in device['commands']">
	 <a class="white button" href="/command/${device['id']}/${device['commands'][key]}/">${key}</a>
	</span>
	
    <a href="#" class="red button" onclick="showhide('optionpanel');">Hide</a> <a class="black button" href="/index">Back to index</a></p> 
    </div>
    
<p>&copy; 2011 Syspimp</p>
</body>
</html>
