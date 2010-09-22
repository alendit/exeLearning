#!/usr/bin/env python

## converts a xul menu-bar from mainpage.py to a jquery- and superfish 
## based html menu-bar

import os
from xml.dom import minidom

html = u"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <title>Navibar</title>
        <link rel='stylesheet' type='text/css' media='screen' href='superfish.css' />

        <!--<script type="application/x-javascript" src="chrome://global/content/nsTransferable.js"/>
        <script language="JavaScript" src="/scripts/common.js"/>
        <script language="JavaScript" src="/xulscripts/draganddrop.js"/>
        <script language="JavaScript" src="/xulscripts/mainpage.js"/>-->
        <script language="JavaScript" src="jquery.js"/></script>
        <script type='text/javascript' src='superfish.js'></script>
        <script type='text/javascript'>
            $(document).ready(function() {
                $('ul.sf-menu').superfish();
                });
        </script>
    </head>
    <body>
        <div>
""" 

## here the magic happens

xuldoc = minidom.parse('mainpage.xul').getElementsByTagName('menubar')[0]

doc = minidom.Document()
bar = doc.createElement("ul")
bar.setAttribute("label", "root")
bar.setAttribute("class", 'sf-menu sf-vertical')
doc.appendChild(bar)
text = doc.createTextNode("")
bar.appendChild(text)

def menuConverter(parent, menu):
    if not hasattr(menu, "tagName") or not menu.tagName == "menu" :
        return
    li = doc.createElement("li")
    print parent.attributes['label'].value
    print "Parent's children: %s" % (len(parent.childNodes))
    parent.appendChild(li)
    a = doc.createElement("a")
    a.setAttribute("id", menu.attributes["id"].value)
    a.setAttribute("href", "#")
    li.appendChild(a)
    text = doc.createTextNode(menu.attributes["label"].value)
    a.appendChild(text)
    ul = doc.createElement("ul")
    ul.setAttribute("label", menu.attributes["label"].value + " ul")
    li.appendChild(ul)
    text = doc.createTextNode("")
    ul.appendChild(text)
    for sub in menu.getElementsByTagName("menupopup")[0].childNodes:
        if not hasattr(sub, "tagName") : continue
        if sub.tagName == "menuitem":
            liItem = doc.createElement("li")
            ul.appendChild(liItem)
            aItem = doc.createElement("a")
            onclick = getattr(sub.attributes.get("oncommand", None) or\
                    sub.attributes.get("onclick", None), "value", "")
            aItem.setAttribute("onclick", onclick)
            liItem.appendChild(aItem)
            label = getattr(sub.attributes.get("label", None), "value", "")
            text = doc.createTextNode(label)
            aItem.appendChild(text)
        elif sub.tagName == "menu":

            print "Sub label %s" % sub.attributes['label'].value
            menuConverter(ul, sub)


for menu in xuldoc.childNodes:
    if hasattr(menu, "tagName"):
        print "Main menue: %s" % menu.attributes['label'].value
    menuConverter(bar, menu)


xml = bar.toprettyxml()
print "Parent's children: %s" % (len(bar.childNodes))

open("test.xml", "w").write(xml)

html += """%s\n     </div>
    </body>
</html>""" % xml
                                   

file('result.html', 'w').write(html)
os.system("firefox result.html")
