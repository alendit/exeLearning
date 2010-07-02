var oldWidth, oldHeight;
var url = tinyMCE.getParam("media_external_list_url");
if (url != null) {
	// Fix relative
	if (url.charAt(0) != '/' && url.indexOf('://') == -1)
		url = tinyMCE.documentBasePath + "/" + url;

	document.write('<sc'+'ript language="javascript" type="text/javascript" src="' + url + '"></sc'+'ript>');
}

function enable_media_type(f, max_plugin, expected_pos, name ) {
   if (f.media_type.options[expected_pos].value != name) { 
      var pos = 0; 
      while (pos <= max_plugin) { 
         if (f.media_type.options[pos].value == name) { 
	    f.media_type.options[pos].disabled=""; 
	    pos = max_plugin; 
	 } 
	 pos += 1; 
      } 
   } 
   else { 
      f.media_type.options[expected_pos].disabled=""; 
   }
}

function init() {
	var pl = "", f, val;
	var type = "none", fe, i;

	tinyMCEPopup.resizeToInnerSize();
	f = document.forms[0]

	var max_plugin = f.media_type.options.length;
	//var assume_plugins =  tinyMCE.getParam("exe_assume_media_plugins");
        // begin backing this out, and let all media types show.  Here's the quick version:  ;-)
	var assume_plugins =  1;

	if (assume_plugins || tinyMCEPopup.windowOpener.detectFlash()) {
	   var flash_pos = 1;  // shortcut to expected hardcoded select position
           enable_media_type(f, max_plugin,  flash_pos, "flash");
	}
        if (assume_plugins || tinyMCEPopup.windowOpener.detectQuickTime()) {
	   var qt_pos = 2;  // shortcut to expected hardcoded select position
           enable_media_type(f, max_plugin,  qt_pos, "qt");
	}
	if (assume_plugins || tinyMCEPopup.windowOpener.detectWindowsMedia()) {
	   var wmp_pos = 3;  // shortcut to expected hardcoded select position
           enable_media_type(f, max_plugin,  wmp_pos, "wmp");
	}
        if (assume_plugins || tinyMCEPopup.windowOpener.detectReal()) {
	   var real_pos = 4;  // shortcut to expected hardcoded select position
           enable_media_type(f, max_plugin,  real_pos, "rmp");
	}
	// always allow the eXe MP3 because player is embedded (no detection mechanism, either):
	var mp3_pos = 5;  // shortcut to expected hardcoded select position
        enable_media_type(f, max_plugin,  mp3_pos, "mp3");

	// always allow the eXe MP3 because player is embedded (no detection mechanism, either):
	 var flv_pos = 6;  // shortcut to expected hardcoded select position
         enable_media_type(f, max_plugin,  flv_pos, "flp");
    //html5 video tags
    var html5_pos = 7;
        enable_media_type(f, max_plugin, html5_pos, "html5");


	fe = tinyMCE.selectedInstance.getFocusElement();
	if (/mceItem(Flash|ShockWave|WindowsMedia|QuickTime|RealMedia|MP3|FlowPlayer|HTML5)/.test(tinyMCE.getAttrib(fe, 'class'))) {
		pl = "x={" + fe.title + "};";

		switch (tinyMCE.getAttrib(fe, 'class')) {
			case 'mceItemFlash':
				type = 'flash';
				break;

			case 'mceItemShockWave':
				type = 'shockwave';
				break;

			case 'mceItemWindowsMedia':
				type = 'wmp';
				break;

			case 'mceItemQuickTime':
				type = 'qt';
				break;

			case 'mceItemRealMedia':
				type = 'rmp';
				break;
			
			case 'mceItemMP3':
				type = 'mp3';
				break;

			case 'mceItemFlowPlayer':
				type = 'flp';
				break;
            case 'mceItemHTML5':
                type = 'html5';
                break;
		}
		// In case this media type was disbled due to lack of its browser plugin,
		// but such a media type is now being loaded - don't want it uneditable.
		// So, go ahead and enable it now that we've already got media of this type:
	        var any_pos = 0;  // search through all the media types until we find this one:
                enable_media_type(f, max_plugin,  any_pos, type);
		// Note that this override really opens back up the problem that disabling
		// the media types was trying to solve anyhow, in that once a file with such media
		// is loaded, the eXe FireFox will once again complain of any missing plugin.
		// As such, all of this protection is really just a first pass filter for new .elps.

		document.forms[0].insert.value = tinyMCE.getLang('lang_update', 'Insert', true); 
	}

	document.getElementById('filebrowsercontainer').innerHTML = getBrowserHTML('filebrowser','src','media','media');
	document.getElementById('qtsrcfilebrowsercontainer').innerHTML = getBrowserHTML('qtsrcfilebrowser','qt_qtsrc','media','media');
	document.getElementById('bgcolor_pickcontainer').innerHTML = getColorPickerHTML('bgcolor_pick','bgcolor');

	var html = getMediaListHTML('filebrowser','src','media','media');
	if (html == "")
		document.getElementById("linklistrow").style.display = 'none';
	else
		document.getElementById("linklistcontainer").innerHTML = html;

	// Resize some elements
	if (isVisible('filebrowsercontainer'))
		document.getElementById('src').style.width = '230px';

	// Setup form
	if (pl != "") {
		pl = eval(pl);

		switch (type) {
			case "flash":
				setBool(pl, 'flash', 'loop');
				setBool(pl, 'flash', 'play');
				setBool(pl, 'flash', 'menu');
				setBool(pl, 'flash', 'swliveconnect');
				setStr(pl, 'flash', 'quality');
				setStr(pl, 'flash', 'scale');
				setStr(pl, 'flash', 'salign');
				setStr(pl, 'flash', 'wmode');
				setStr(pl, 'flash', 'base');
				setStr(pl, 'flash', 'flashvars');
			break;

			case "qt":
				setBool(pl, 'qt', 'loop');
				setBool(pl, 'qt', 'autoplay');
				setBool(pl, 'qt', 'cache');
				setBool(pl, 'qt', 'controller');
				setBool(pl, 'qt', 'correction');
				setBool(pl, 'qt', 'enablejavascript');
				setBool(pl, 'qt', 'kioskmode');
				setBool(pl, 'qt', 'autohref');
				setBool(pl, 'qt', 'playeveryframe');
				setBool(pl, 'qt', 'tarsetcache');
				setStr(pl, 'qt', 'scale');
				setStr(pl, 'qt', 'starttime');
				setStr(pl, 'qt', 'endtime');
				setStr(pl, 'qt', 'tarset');
				setStr(pl, 'qt', 'qtsrcchokespeed');
				setStr(pl, 'qt', 'volume');
				setStr(pl, 'qt', 'qtsrc');
			break;

			case "shockwave":
				setBool(pl, 'shockwave', 'sound');
				setBool(pl, 'shockwave', 'progress');
				setBool(pl, 'shockwave', 'autostart');
				setBool(pl, 'shockwave', 'swliveconnect');
				setStr(pl, 'shockwave', 'swvolume');
				setStr(pl, 'shockwave', 'swstretchstyle');
				setStr(pl, 'shockwave', 'swstretchhalign');
				setStr(pl, 'shockwave', 'swstretchvalign');
			break;

			case "wmp":
				setBool(pl, 'wmp', 'autostart');
				setBool(pl, 'wmp', 'enabled');
				setBool(pl, 'wmp', 'enablecontextmenu');
				setBool(pl, 'wmp', 'fullscreen');
				setBool(pl, 'wmp', 'invokeurls');
				setBool(pl, 'wmp', 'mute');
				setBool(pl, 'wmp', 'stretchtofit');
				setBool(pl, 'wmp', 'windowlessvideo');
				setStr(pl, 'wmp', 'balance');
				setStr(pl, 'wmp', 'baseurl');
				setStr(pl, 'wmp', 'captioningid');
				setStr(pl, 'wmp', 'currentmarker');
				setStr(pl, 'wmp', 'currentposition');
				setStr(pl, 'wmp', 'defaultframe');
				setStr(pl, 'wmp', 'playcount');
				setStr(pl, 'wmp', 'rate');
				setStr(pl, 'wmp', 'uimode');
				setStr(pl, 'wmp', 'volume');
			break;

			case "rmp":
				setBool(pl, 'rmp', 'autostart');
				setBool(pl, 'rmp', 'loop');
				setBool(pl, 'rmp', 'autogotourl');
				setBool(pl, 'rmp', 'center');
				setBool(pl, 'rmp', 'imagestatus');
				setBool(pl, 'rmp', 'maintainaspect');
				setBool(pl, 'rmp', 'nojava');
				setBool(pl, 'rmp', 'prefetch');
				setBool(pl, 'rmp', 'shuffle');
				setStr(pl, 'rmp', 'console');
				setStr(pl, 'rmp', 'controls');
				setStr(pl, 'rmp', 'numloop');
				setStr(pl, 'rmp', 'scriptcallbacks');
			break;

			case "flp":
				setStr(pl, 'flp', 'flv_src');
			break;
		}

		setStr(pl, null, 'src');
		setStr(pl, null, 'id');
		setStr(pl, null, 'name');
		setStr(pl, null, 'vspace');
		setStr(pl, null, 'hspace');
		setStr(pl, null, 'bgcolor');
		setStr(pl, null, 'align');
		setStr(pl, null, 'width');
		setStr(pl, null, 'height');

		if ((val = tinyMCE.getAttrib(fe, "width")) != "")
			pl.width = f.width.value = val;

		if ((val = tinyMCE.getAttrib(fe, "height")) != "")
			pl.height = f.height.value = val;

		oldWidth = pl.width ? parseInt(pl.width) : 0;
		oldHeight = pl.height ? parseInt(pl.height) : 0;
	} else
		oldWidth = oldHeight = 0;

	selectByValue(f, 'media_type', type);
	changedType(type);
	updateColor('bgcolor_pick', 'bgcolor');

	TinyMCE_EditableSelects.init();
	generatePreview();
}

function insertMedia() {
	var fe, f = document.forms[0], h;

	var type =  f.media_type.options[f.media_type.selectedIndex].value;
        if (type == "none") {
           alert(tinyMCE.getLang('lang_media_select_media_type'));
           return false;
        } 

	if (!AutoValidator.validate(f)) {
		alert(tinyMCE.getLang('lang_invalid_data'));
		return false;
	}

	var src = f.src.value;
	// Apply the same file-browser button magic to any filenames which were
        // typed into the URL field by hand, rather than selected via the browser button,
        // as will apply to any !http: and !file: which isn't in the resource or previews dirs:
        if (src.search('resources/')!=0 && src.search('/previews/')!=0 && src.search('../previews/')!=0 && src.search('http:')!=0 && src.search('file:')!=0) {
            // looks like a hand-typed filename, 
            // so use type media2insert to indicate that no browser or preview is necessary:
            doBrowserHTML('filebrowser','src','media2insert','media');
            src = f.src.value;
        }

	f.width.value = f.width.value == "" ? 200 : f.width.value;
	f.height.value = f.height.value == "" ? 200 : f.height.value;

	fe = tinyMCE.selectedInstance.getFocusElement();
	if (fe != null && /mceItem(Flash|ShockWave|WindowsMedia|QuickTime|RealMedia|MP3|FlowPlayer|HTML5)/.test(tinyMCE.getAttrib(fe, 'class'))) {
		switch (f.media_type.options[f.media_type.selectedIndex].value) {
			case "flash":
				fe.className = "mceItemFlash";
				break;

			case "shockwave":
				fe.className = "mceItemShockWave";
				break;

			case "qt":
				fe.className = "mceItemQuickTime";
				break;

			case "wmp":
				fe.className = "mceItemWindowsMedia";
				break;

			case "rmp":
				fe.className = "mceItemRealMedia";
				break;

			case "mp3":
				fe.className = "mceItemMP3";
				break;

			case "flp":
				fe.className = "mceItemFlowPlayer";
				break;
            case "html5":
                fe.className = "mceItemHTML5";
                break;
		}

		if (fe.width != f.width.value || fe.height != f.height.value)
			tinyMCE.selectedInstance.repaint();

		fe.title = serializeParameters();
		fe.width = f.width.value;
		fe.height = f.height.value;
		fe.style.width = f.width.value + (f.width.value.indexOf('%') == -1 ? 'px' : '');
		fe.style.height = f.height.value + (f.height.value.indexOf('%') == -1 ? 'px' : '');
		fe.align = f.align.options[f.align.selectedIndex].value;
	} else {
		h = '<img src="' + tinyMCE.getParam("theme_href") + '/images/spacer.gif"' ;

		switch (f.media_type.options[f.media_type.selectedIndex].value) {
			case "flash":
				h += ' class="mceItemFlash"';
				break;

			case "shockwave":
				h += ' class="mceItemShockWave"';
				break;

			case "qt":
				h += ' class="mceItemQuickTime"';
				break;

			case "wmp":
				h += ' class="mceItemWindowsMedia"';
				break;

			case "rmp":
				h += ' class="mceItemRealMedia"';
				break;

			case "mp3":
				h += ' class="mceItemMP3"';
				break;

			case "flp":
				h += ' class="mceItemFlowPlayer"';
				break;
            case "html5":
                h += ' class="mceItemHTML5"';
                break;
		}

		h += ' title="' + serializeParameters() + '"';
		h += ' width="' + f.width.value + '"';
		h += ' height="' + f.height.value + '"';
		h += ' align="' + f.align.options[f.align.selectedIndex].value + '"';

		h += ' />';

		tinyMCE.selectedInstance.execCommand('mceInsertContent', false, h);
	}

	tinyMCEPopup.close();
}

function getMediaListHTML() {
	if (typeof(tinyMCEMediaList) != "undefined" && tinyMCEMediaList.length > 0) {
		var html = "";

		html += '<select id="linklist" name="linklist" style="width: 250px" onfocus="tinyMCE.addSelectAccessibility(event, this, window);" onchange="this.form.src.value=this.options[this.selectedIndex].value;">';
		html += '<option value="">---</option>';

		for (var i=0; i<tinyMCEMediaList.length; i++)
			html += '<option value="' + tinyMCEMediaList[i][1] + '">' + tinyMCEMediaList[i][0] + '</option>';

		html += '</select>';

		return html;
	}

	return "";
}

function getType(v) {
	var fo, i, c, el, x, f = document.forms[0];

	fo = tinyMCE.getParam("media_types", "flash=swf;shockwave=dcr;qt=mov,qt,mpg,mp3,mp4,mpeg;shockwave=dcr;wmp=avi,wmv,wm,asf,asx,wmx,wvx;rmp=rm,ra,ram").split(';');

	// YouTube
	if (v.indexOf('http://www.youtube.com/watch?v=') == 0) {
		f.width.value = '425';
		f.height.value = '350';
		f.src.value = 'http://www.youtube.com/v/' + v.substring('http://www.youtube.com/watch?v='.length);
		// now, in case the current Flash media type is disabled due to no plugin, enable for this:
	        var max_plugin = f.media_type.options.length;
	        var flash_pos = 2;  // shortcut to expected hardcoded select position
                enable_media_type(f, max_plugin,  flash_pos, "flash");
		return 'flash';
	}

	// Google video
	if (v.indexOf('http://video.google.com/videoplay?docid=') == 0) {
		f.width.value = '425';
		f.height.value = '326';
		f.src.value = 'http://video.google.com/googleplayer.swf?docId=' + v.substring('http://video.google.com/videoplay?docid='.length) + '&hl=en';
		// now, in case the current Flash media type is disabled due to no plugin, enable for this:
	        var max_plugin = f.media_type.options.length;
	        var flash_pos = 2;  // shortcut to expected hardcoded select position
                enable_media_type(f, max_plugin,  flash_pos, "flash");
		return 'flash';
	}

	for (i=0; i<fo.length; i++) {
		c = fo[i].split('=');

		el = c[1].split(',');
		for (x=0; x<el.length; x++)
		if (v.indexOf('.' + el[x]) != -1)
			return c[0];
	}

	return null;
}

function switchType(v) {
	var t = getType(v), d = document, f = d.forms[0];

	if (!t)
		return;

	selectByValue(d.forms[0], 'media_type', t);
	changedType(t);

	// Update qtsrc also
	if (t == 'qt' && f.src.value.toLowerCase().indexOf('rtsp://') != -1) {
		alert(tinyMCE.getLang("lang_media_qt_stream_warn"));

		if (f.qt_qtsrc.value == '')
			f.qt_qtsrc.value = f.src.value;
	}
}

function changedType(t) {
	var d = document;

	d.getElementById('flash_options').style.display = 'none';
	d.getElementById('qt_options').style.display = 'none';
	d.getElementById('shockwave_options').style.display = 'none';
	d.getElementById('wmp_options').style.display = 'none';
	d.getElementById('rmp_options').style.display = 'none';
	d.getElementById('none_options').style.display = 'none';
	d.getElementById('mp3_options').style.display = 'none';
	d.getElementById('flp_options').style.display = 'none';
    d.getElementById('html5_options').style.display = 'none';

	d.getElementById(t + '_options').style.display = 'block';
}

function serializeParameters() {
	var d = document, f = d.forms[0], s = '';

	switch (f.media_type.options[f.media_type.selectedIndex].value) {
		case "flash":
			s += getBool('flash', 'loop', true);
			s += getBool('flash', 'play', 'force_to_ALWAYS_show');
			s += getBool('flash', 'menu', true);
			s += getBool('flash', 'swliveconnect', false);
			s += getStr('flash', 'quality');
			s += getStr('flash', 'scale');
			s += getStr('flash', 'salign');
			s += getStr('flash', 'wmode');
			s += getStr('flash', 'base');
			s += getStr('flash', 'flashvars');
		break;

		case "qt":
			s += getBool('qt', 'loop', false);
			s += getBool('qt', 'autoplay', 'force_to_ALWAYS_show');
			s += getBool('qt', 'cache', false);
			s += getBool('qt', 'controller', true);
			s += getBool('qt', 'correction', false, 'none', 'full');
			s += getBool('qt', 'enablejavascript', false);
			s += getBool('qt', 'kioskmode', false);
			s += getBool('qt', 'autohref', false);
			s += getBool('qt', 'playeveryframe', false);
			s += getBool('qt', 'targetcache', false);
			s += getStr('qt', 'scale');
			s += getStr('qt', 'starttime');
			s += getStr('qt', 'endtime');
			s += getStr('qt', 'target');
			s += getStr('qt', 'qtsrcchokespeed');
			s += getStr('qt', 'volume');
			s += getStr('qt', 'qtsrc');
		break;

		case "shockwave":
			s += getBool('shockwave', 'sound');
			s += getBool('shockwave', 'progress');
			s += getBool('shockwave', 'autostart');
			s += getBool('shockwave', 'swliveconnect');
			s += getStr('shockwave', 'swvolume');
			s += getStr('shockwave', 'swstretchstyle');
			s += getStr('shockwave', 'swstretchhalign');
			s += getStr('shockwave', 'swstretchvalign');
		break;

		case "wmp":
			s += getBool('wmp', 'autostart', 'force_to_ALWAYS_show', '1', '0');
			s += getBool('wmp', 'enabled', false);
			s += getBool('wmp', 'enablecontextmenu', true);
			s += getBool('wmp', 'fullscreen', false);
			s += getBool('wmp', 'invokeurls', true);
			s += getBool('wmp', 'mute', false);
			s += getBool('wmp', 'stretchtofit', false);
			s += getBool('wmp', 'windowlessvideo', false);
			s += getStr('wmp', 'balance');
			s += getStr('wmp', 'baseurl');
			s += getStr('wmp', 'captioningid');
			s += getStr('wmp', 'currentmarker');
			s += getStr('wmp', 'currentposition');
			s += getStr('wmp', 'defaultframe');
			s += getStr('wmp', 'playcount');
			s += getStr('wmp', 'rate');
			s += getStr('wmp', 'uimode');
			s += getStr('wmp', 'volume');
		break;

		case "rmp":
			s += getBool('rmp', 'autostart', 'force_to_ALWAYS_show');
			s += getBool('rmp', 'loop', false);
			s += getBool('rmp', 'autogotourl', true);
			s += getBool('rmp', 'center', false);
			s += getBool('rmp', 'imagestatus', true);
			s += getBool('rmp', 'maintainaspect', false);
			s += getBool('rmp', 'nojava', false);
			s += getBool('rmp', 'prefetch', false);
			s += getBool('rmp', 'shuffle', false);
			s += getStr('rmp', 'console');
			s += getStr('rmp', 'controls');
			s += getStr('rmp', 'numloop');
			s += getStr('rmp', 'scriptcallbacks');
		break;

		case "flp":
			s += getStr('flp', 'flv_src');
		break;
	}

	s += getStr(null, 'id');
	s += getStr(null, 'name');
	s += getStr(null, 'src');
	s += getStr(null, 'align');
	s += getStr(null, 'bgcolor');
	s += getInt(null, 'vspace');
	s += getInt(null, 'hspace');
	s += getStr(null, 'width');
	s += getStr(null, 'height');

	s = s.length > 0 ? s.substring(0, s.length - 1) : s;

	return s;
}

function setBool(pl, p, n) {
	if (typeof(pl[n]) == "undefined")
		return;

	if (pl[n] != "false" && pl[n] != "0") {
	   document.forms[0].elements[p + "_" + n].checked = pl[n];
	}
}

function setStr(pl, p, n) {
	var f = document.forms[0], e = f.elements[(p != null ? p + "_" : '') + n];

	if (typeof(pl[n]) == "undefined")
		return;

	// accommodate hidden fields in the same manner as text:
	if (e.type == "text" || e.type == "hidden")
		e.value = pl[n];
	else
		selectByValue(f, (p != null ? p + "_" : '') + n, pl[n]);
}

function getBool(p, n, d, tv, fv) {
	var v = document.forms[0].elements[p + "_" + n].checked;

	tv = typeof(tv) == 'undefined' ? 'true' : "'" + jsEncode(tv) + "'";
	fv = typeof(fv) == 'undefined' ? 'false' : "'" + jsEncode(fv) + "'";

	return (v == d) ? '' : n + (v ? ':' + tv + ',' : ':' + fv + ',');
}

function getStr(p, n, d) {
	var e = document.forms[0].elements[(p != null ? p + "_" : "") + n];
	// var v = e.type == "text" ? e.value : e.options[e.selectedIndex].value;
        // accommodate hidden fields in the same manner as text:
	var v = ((e.type == "text" || e.type == "hidden")? e.value : e.options[e.selectedIndex].value);

	return ((n == d || v == '') ? '' : n + ":'" + jsEncode(v) + "',");
}

function getInt(p, n, d) {
	var e = document.forms[0].elements[(p != null ? p + "_" : "") + n];
	var v = e.type == "text" ? e.value : e.options[e.selectedIndex].value;

	return ((n == d || v == '') ? '' : n + ":" + v.replace(/[^0-9]+/g, '') + ",");
}

function jsEncode(s) {
	s = s.replace(new RegExp('\\\\', 'g'), '\\\\');
	s = s.replace(new RegExp('"', 'g'), '\\"');
	s = s.replace(new RegExp("'", 'g'), "\\'");

	return s;
}

function generatePreview(c) {
	var f = document.forms[0], p = document.getElementById('prev'), h = '', cls, pl, n, type, codebase, wp, hp, nw, nh;

	var type =  f.media_type.options[f.media_type.selectedIndex].value;
        if (type == "none") {
           return;
        } 
        // same for FlowPlayer FLVs, since they will just ask for a Flash plugin:
        // eventually might be nice to also clear out any previous preview..
        // PERHAPS this could later "preview" the same image the eXe previews for FLVs,
        // the one that says "you will see this on export", but for now, no preview at all:
        if (type == "flp") {
           return;
        }
	// and likewise for the embedded mp3 player: don't preview here,
        // lest users get confused when they see it ask for a missing plugin:
        if (type == "mp3") {
	   // but first, go ahead and set a reasonable first-pass
	   // height and width, if not already specified:
           if (f.width.value == "" && f.height.value == "") {
	      f.height.value = 15;
              f.width.value = 400;
           }
           return;
        }

	p.innerHTML = '<!-- x --->';

	nw = parseInt(f.width.value);
	nh = parseInt(f.height.value);

	if (f.width.value != "" && f.height.value != "") {
		if (f.constrain.checked) {
			if (c == 'width' && oldWidth != 0) {
				wp = nw / oldWidth;
				nh = Math.round(wp * nh);
				f.height.value = nh;
			} else if (c == 'height' && oldHeight != 0) {
				hp = nh / oldHeight;
				nw = Math.round(hp * nw);
				f.width.value = nw;
			}
		}
	}

	if (f.width.value != "")
		oldWidth = nw;

	if (f.height.value != "")
		oldHeight = nh;

	// After constrain
	pl = serializeParameters();

	switch (f.media_type.options[f.media_type.selectedIndex].value) {
		case "flash":
			cls = 'clsid:D27CDB6E-AE6D-11cf-96B8-444553540000';
			codebase = 'http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0';
			type = 'application/x-shockwave-flash';
			break;

		case "shockwave":
			cls = 'clsid:166B1BCA-3F9C-11CF-8075-444553540000';
			codebase = 'http://download.macromedia.com/pub/shockwave/cabs/director/sw.cab#version=8,5,1,0';
			type = 'application/x-director';
			break;

		case "qt":
			cls = 'clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B';
			codebase = 'http://www.apple.com/qtactivex/qtplugin.cab#version=6,0,2,0';
			type = 'video/quicktime';
			break;

		case "wmp":
			cls = tinyMCE.getParam('media_wmp6_compatible') ? 'clsid:05589FA1-C356-11CE-BF01-00AA0055595A' : 'clsid:6BF52A52-394A-11D3-B153-00C04F79FAA6';
			codebase = 'http://activex.microsoft.com/activex/controls/mplayer/en/nsmp2inf.cab#Version=5,1,52,701';
                        //  eXe Windows Media Player hack:
                        type = 'video/x-ms-wmv';
			break;

		case "rmp":
			cls = 'clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA';
			codebase = 'http://activex.microsoft.com/activex/controls/mplayer/en/nsmp2inf.cab#Version=5,1,52,701';
			type = 'audio/x-pn-realaudio-plugin';
			break;

		case "mp3":
			cls = 'clsid:d27cdb6e-ae6d-11cf-96b8-444553540000';
			codebase = 'http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0';
			type = 'application/x-shockwave-flash';
			break;

	}

	if (pl == '') {
		p.innerHTML = '';
		return;
	}

	pl = eval('x={' + pl + '};');

	if (!pl.src) {
		p.innerHTML = '';
		return;
	}

	pl.src = tinyMCE.convertRelativeToAbsoluteURL(tinyMCE.settings['base_href'], pl.src);
	pl.width = !pl.width ? 100 : pl.width;
	pl.height = !pl.height ? 100 : pl.height;
	pl.id = !pl.id ? 'obj' : pl.id;
	pl.name = !pl.name ? 'eobj' : pl.name;
	pl.align = !pl.align ? '' : pl.align;

	h += '<object';
	if (f.media_type.options[f.media_type.selectedIndex].value == "wmp") {
            // eXe Windows Media Player hack:
            h += ' type="' + type + '" data="' + pl.src + '"';
        }
        else {
            h += ' classid="clsid:' + cls + '"';
        }
	h += ' codebase="' + codebase + '" width="' + pl.width + '" height="' + pl.height + '" id="' + pl.id + '" name="' + pl.name + '" align="' + pl.align + '">';

	for (n in pl) {
		h += '<param name="' + n + '" value="' + pl[n] + '">';

		// Add extra url parameter if it's an absolute URL
		if (n == 'src' && pl[n].indexOf('://') != -1)
			h += '<param name="url" value="' + pl[n] + '" />';
	}

	h += '<embed type="' + type + '" ';

	for (n in pl)
		h += n + '="' + pl[n] + '" ';

	h += '></embed></object>';

	p.innerHTML = "<!-- x --->" + h;
}
