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
		<a href="javascript:history.go(-1)" id="backButton">Back</a>
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
	
	<ul>
	  <li class="arrow" py:for="key in events">
	  	<?python
		ack=''
		ackclass=''
		if events[key]['eventstate'] != 1:
			ack = 'Not acknowledged'
			ackclass = "noack"
		?>
		<div class="${ackclass}">
        <a href="/events/get/${events[key]['evid']}"><small class="counter">${events[key]['count']}</small>${events[key]['summary']}</a>
        <a href="/events/get/${events[key]['evid']}">${events[key]['component']} ${events[key]['eventclass']}</a>
		<a href="/events/get/${events[key]['evid']}">First Time: ${events[key]['firsttime']}<br /> Last Time ${events[key]['lasttime']} ${ack}</a>
		</div> 	
      </li>
	</ul>

	<p><a href="#" class="green button" onclick="showhide('optionpanel');">Group Commands</a></p>
	<div id="optionpanel" style="display: none">
    <p><a class="white button" href="http://www.google.com">Visit</a> <a href="mailto:dtaylor@tfoundnt.com" class="white button">E-mail author</a> <a href="#" class="red button" onclick="showhide('optionpanel');">Hide me</a> <a class="black button" href="index.html">Back to index</a></p> 
    </div>

<p>&copy; 2011 Syspimp</p>
	
</body>
</html>