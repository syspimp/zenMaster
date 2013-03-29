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
		<a href="index" id="backButton">Index</a>
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
	<h1>Choose a group</h1>
	
	<ul>
	  <li class="arrow" py:for="key in device">
        <?python
        NUM=len(device[key]['members'])
        ?>
        <a href="groups/get/${device[key]['sectionid']}"><small class="counter">${NUM}</small>${device[key]['name']}</a> 	
      </li>
	</ul>

	<p><a href="#" class="green button" onclick="showhide('optionpanel');">Group Commands</a></p>
	<div id="optionpanel" style="display: none">
    <p><a class="white button" href="http://www.google.com">Visit</a> <a href="mailto:dtaylor@tfoundnt.com" class="white button">E-mail author</a> <a href="#" class="red button" onclick="showhide('optionpanel');">Hide me</a> <a class="black button" href="index.html">Back to index</a></p> 
    </div>

<p>&copy; 2011 Syspimp</p>
	
</body>
</html>