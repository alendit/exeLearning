// scripts from properties page. See comment in ../templates/properties.html
// for more info

regEx = /[a-z][a-z]_\w+/

// Translates all the nodes in the document
function translate(start, part) {
if (start.nodeName == '#text') {
nevow_clientToServerEvent('translate', this, '', start.parentNode.id, '!contents!'+part, start.data)
} else if (start.hasAttribute('label')) {
  nevow_clientToServerEvent('translate', this, '', start.id, 'label', start.label)
} else if (start.nodeName == 'label') {
  nevow_clientToServerEvent('translate', this, '', start.id, 'value', start.value);
  if (start.hasAttribute('tooltiptext')) {
    nevow_clientToServerEvent('translate', this, '', start.id, 'tooltiptext', start.getAttribute('tooltiptext'))
  }
} else if (start.nodeName == 'key') {
    if (start.hasAttribute('key')) {
        nevow_clientToServerEvent('translate', this, '', start.id, 'key', start.value)
    } else {
        nevow_clientToServerEvent('translate', this, '', start.id, 'keycode', start.value)
    }
} else if (start.nodeName == 'window') {
  nevow_clientToServerEvent('translate', this, '', start.id, 'title', start.value)
}
// Drill down
for (var i=0; i < start.childNodes.length; i++) {
    var node = start.childNodes[i];
    translate(node, i);
}
}

function setText(textID) {
  var help = document.getElementById(textID).hidden;
  if (help == false) {
      document.getElementById(textID).hidden=true; 
  } else {
      document.getElementById(textID).hidden=false;
  }
}


// Called by the user to provide an image file name to add to the package
function addImage(image, node) {
  netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
  var nsIFilePicker = Components.interfaces.nsIFilePicker;
  var fp = Components.classes["@mozilla.org/filepicker;1"].createInstance(nsIFilePicker);
  fp.init(window, "Select an image", nsIFilePicker.modeOpen);
  fp.appendFilter("Image Files", "*.jpg; *.jpeg; *.png; *.gif");
  fp.appendFilters(nsIFilePicker.filterAll);
  var res = fp.show();
  if (res == nsIFilePicker.returnOK) {
      image.attr('src', 'file://'+fp.file.path);
      image.removeAttr('width');
      image.removeAttr('height');
      submitForm(node)
  }
  
}

// Called by the user to clear an image from the package
function clearImage(elementId, node) {
  var image = document.getElementById(elementId);
  image.src    = '';
//  image.width  = '400';
//  image.height = '100';
  submitForm(node)
}

function collectIds(ids, start) {
if (start.id && start.id.match(regEx)) {
    ids.push(start.id);
}
for (var i in start.childNodes) {
    var node = start.childNodes[i];
    collectIds(ids, node); // Recurse
}
}

// On document load, we get all the form values from the server
function fillInForms() {
    $("input, img, select").each(function() {
        nevow_clientToServerEvent('fillInField', this, '', $(this).attr('id'));
    });
}

// Post data for a form to the server
// Submits the value for all the fields inside 'container'
// onDone is java script that will be evaluated after all the fields are done
function submitForm(container, onDone) {
    var fields = $("input, img, select");
    fields.each(function(index) {
            if (this.tagName == 'INPUT'){
                if($(this).attr("type") == 'text') {
                    var value = $(this).val();
                } else {
                    var value = $(this).attr('checked');
                }
            } else if (this.tagName == "SELECT") {
                var value = $(this).attr('value');
            } else var value = $(this).attr("src");
            if (onDone) {
                nevow_clientToServerEvent('recieveFieldData', this, '', $(this).attr('id'), escape(value), fields.length, onDone);
            } else {
                nevow_clientToServerEvent('recieveFieldData', this, '', $(this).attr('id'), escape(value), fields.length);
            }
    });
}

