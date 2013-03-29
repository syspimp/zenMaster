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
		<h1>$title</h1>
		<a href="javascript:history.go(-1)" id="backButton">Back</a>
	</div>


<ul class="field">
	<li><h3>Output:</h3><br /><pre>${device}</pre></li>
</ul>

	<p><a href="#" class="green button" onclick="showhide('optionpanel');">Device Commands</a></p>
	<div id="optionpanel" style="display: none">
	<p>
	
    <a href="#" class="red button" onclick="showhide('optionpanel');">Hide</a> <a class="black button" href="/index">Back to index</a></p> 
    </div>
    
<p>&copy; 2011 Syspimp</p>
</body>
</html>
