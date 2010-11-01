window.onload=function()
{
	if(!document.getElementById || !document.createTextNode){return;}
	domslides();
}
/* 
 * DOMSlides 
 * written by Christian Heilmann
 * Version 1.0
 * Licensed Creative Commons Attribution 2.5
 * http://creativecommons.org/licenses/by/2.5/
 */
function domslides()
{
/* Variables to change */

// Texts
	var tocLinkText='TOC';
	var tocCloseText='Close TOC';
	var counterText='(_x_ of _y_)'; 
	var nextSlideText='>>';
	var prevSlideText='<<';
	var titleAdd=' - ';

// IDs
	var boundaryId='boundary';	
	var footerId='footer';
	var tocListId='toclist';
	var closeTocId='closeToc';
	var navigationForm='ds_navigation';
	
// Classes
	var jsIndicatorClass='js';	
	var hideClass='hide';		
	var slideClass='slide';		
	var counterClass='counter';	
	

/* If you change things here, make sure you know what you are doing! */

// Check if the needed markup is available
	var ds_error=false;
	if(!document.getElementById(boundaryId))
	{
		alert('Boundary Element is missing');
		ds_error=true;
	}
	if(!document.getElementById(footerId))
	{
		alert('Footer Element is missing');
		ds_error=true;
	}
	if(!document.getElementsByTagName('h1')[0])
	{
		alert('Heading not existant');
		ds_error=true;
	}
	if(document.getElementsByTagName('h1')[0] && !document.getElementsByTagName('h1')[0].firstChild)
	{
		alert('Heading has no content');
		ds_error=true;
	}
	if(ds_error){return false;}

// Generate the TOC list 
	var tocul=document.createElement('ul');
	tocul.id=tocListId;
	var tocli=document.createElement('li');	
	var tocnestul=document.createElement('ul');
	var toca=ds_link(tocLinkText);
	var toca=ds_link(tocLinkText);
	toca.onclick=function()
	{
		var nul=this.parentNode.getElementsByTagName('ul')[0];
		if(nul.className)
		{
			nul.className='';
		} else {
			nul.className=hideClass;
			news.focus();
		}
		return false;
	}
	tocli.appendChild(toca);
	tocli.appendChild(tocnestul);
	tocul.appendChild(tocli);
	tocnestul.className=hideClass;
// insert list as the first item in the footer
	document.getElementById(footerId).insertBefore(tocul,document.getElementById(footerId).firstChild);

// Loop through all DIVs, and identify slides
	var divs=document.getElementsByTagName('div');
	var c=1;
	var slides=new Array();
	for(var i=1;i<divs.length;i++)
	{
// if the DIV has the slideClass
		if(new RegExp('\\b'+slideClass+'\\b').test(divs[i].className))
		{
// skip DIVs without headings
			var hl=divs[i].getElementsByTagName('h2')[0];
			if(!hl){continue;}
			slides[c]=divs[i];
			c++;
// Add slide title as TOC entry
			var hl=divs[i].getElementsByTagName('h2')[0].firstChild.nodeValue;
			if(oldhl && oldhl==hl){continue;}
			var newli=document.createElement('li');
			var newa=ds_link(hl);
			newa.c=c-1;
			newa.onclick=function()
			{
				showslide(this.c);
				this.parentNode.parentNode.className=hideClass;
				return false;
			}
			newli.appendChild(newa);
			tocnestul.appendChild(newli);
			var oldhl=hl;
		}
	}

// Add closing link to the TOC
	var tocli=document.createElement('li');	
	var toca=ds_link(tocCloseText);
	toca.onclick=function()
	{
		tocnestul.className=hideClass;
		news.focus();
		return false;
	}
	tocli.appendChild(toca);
	tocli.id=closeTocId;
	tocnestul.appendChild(tocli);	
	
// Create the form with the select box
	var newf=document.createElement('form');
	newf.id=navigationForm;
	var news=document.createElement('select');
	news.size=10; 	

// Loop through all slides
	for(var i=1;i<slides.length;i++)
	{
// Add the option with the title to the select box
		var newo=document.createElement('option');
		newo.appendChild(document.createTextNode(slides[i].getElementsByTagName('h2')[0].firstChild.nodeValue));
		news.appendChild(newo);
		newf.appendChild(news);
		document.getElementById(boundaryId).appendChild(newf);
		news.onchange=function()
		{
			showslide(this.selectedIndex+1);
		}
// Create counter and previous/next list
		var newul=document.createElement('ul');
		newul.className=counterClass;
		if(i>1)
		{
			var newli=document.createElement('li');
			var newa=ds_link(prevSlideText);
			newa.i=i-1;
			newa.onclick=function()
			{
				showslide(this.i);
				return false;
			}
			newli.appendChild(newa);
			newul.appendChild(newli);
		}
		var newli=document.createElement('li');
		var tmpText=counterText.replace('_x_',i);
		var tmpText=tmpText.replace('_y_',(slides.length-1));
		newli.appendChild(document.createTextNode(tmpText));
		newul.appendChild(newli);
	if(i<slides.length-1)
		{
			var newli=document.createElement('li');
			var newa=ds_link(nextSlideText);
			newa.i=i+1;
			newa.onclick=function()
			{
				showslide(this.i);
				return false;
			}
			newli.appendChild(newa);
			newul.appendChild(newli);
		}
		slides[i].appendChild(newul);
	}

	// check if there is a slide chosen on the URL and set it accordingly
	var	cid=window.location.toString().match(/#slide(.+)/);
	if (cid && cid[1]){cid=cid[1];}
	var startslide=cid?cid:1;

	// add class to boundary indicating JavaScript is available
	document.getElementById(boundaryId).className=jsIndicatorClass;
	newf.className=hideClass;
	showslide(startslide);
	var mainheading=document.getElementsByTagName('h1')[0];
	var headcontent=mainheading.firstChild.nodeValue;
	mainheading.className=hideClass;
	var newspan=document.createElement('span');
	newspan.appendChild(document.createTextNode(titleAdd+headcontent));
	document.getElementById('footer').appendChild(newspan);
	
	/* tool methods */
	// creates a new link
	function ds_link(t)
	{
		var tmp=document.createElement('a');
		tmp.appendChild(document.createTextNode(t))
		tmp.href='#';
		return tmp;
	}
	// show the current slide, set the select focus
	function showslide(o)
	{
		news.selectedIndex=o-1;
		for(var i=1;i<slides.length;i++)
		{
			slides[i].className=hideClass;
		}
		if(slides[o])
		{	
			slides[o].className=slideClass;
		}
		news.focus();
	}
}

