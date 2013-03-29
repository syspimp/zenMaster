<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta id="viewport" name="viewport" content="width=320; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;" />
	<title>$title</title>
	<link rel="stylesheet" href="/stylesheets/iphone.css" />
	<link rel="apple-touch-icon" href="/images/apple-touch-icon.png" />
	<script type="text/javascript" charset="utf-8">
		window.onload = function() {
		  setTimeout(function(){window.scrollTo(0, 1);}, 100);
		}
	</script>
	<!-- for profile image -->
	<style type="text/css" media="screen">
		li.picture { background: #fff url(/images/minid-profile.png) no-repeat !important; }
	</style>
	<!-- end line customization -->
</head>

<body>
	
	<div id="header">
		<h1>Device Information</h1>
		<a href="/devices" id="backButton">Back</a>
	</div>

<h1>${device['externalhostname']}</h1>

<ul class="profile">
	<li class="picture"><a href="http://www.minid.net"><!--use this space to define tooltip title when user taps-->Julio Alonso Picture</a></li>
	<li class="clearfix"><h2>${device['domain']}</h2><p>${device['state']} ${device['server-type']}</p></li>
</ul>

<ul class="field">
	<li><h3>External Ip</h3> <a href="ssh://10.0.0.1">${device['externalip']}</a></li>
	<li class="arrow"><h3>Events</h3> <small>Blog</small> <a href="http://www.minid.net">Merodeando</a></li>
	<li class="arrow"><h3>Commands</h3> <a href="http://www.google.com/">Carrer de Calàbria 168,<br />08015 Barcelona, Spain<br />World</a></li>
	<li><h3>Provider</h3> <a href="http://www.google.com/maps">Map</a></li>
	<li><h3>blah</h3> <a href="tel:+34999888777">oh hai</a></li>
	<li><h3>blah</h3> <a href="tel:+34999888777">lulz</a></li>
	<li><h3>Comments</h3> <big>Hello there this is a very small note I want to write.</big></li>
</ul>

<ul class="data">
	<li><p>This is very lulzy. You can put any thing here.</p></li>
</ul>

<p><strong>Best enjoyed on a real iPhone</strong><br />This iPhone UI Framework kit is licenced under GNU Affero General Public License (<a href="http://www.gnu.org/licenses/agpl.html">GNU AGPL 3</a>)</p>

</body>
</html>