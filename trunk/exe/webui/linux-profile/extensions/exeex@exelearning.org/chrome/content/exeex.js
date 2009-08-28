// Need to set window.* methods after window is loaded apparently

window.addEventListener("load", eXeexInit, true);

function eXeWindowIsClosing() {
  // try to prevent closing the main window
  if (content.document.getElementById('mainWindow').id == 'mainWindow') {
    var target = content.document.getElementById('menu-quit');
    var evObj = document.createEvent('MouseEvents');
    evObj.initMouseEvent( 'click', true, true, window, 1, 12, 345, 7, 220, false, false, true, false, 0, null );
    target.dispatchEvent(evObj);
    return false;
  }
  return true;
}

function eXeTryToClose(arg) {
  alert("Please use eXe's\n   File... Quit\nmenu to close eXe.");
  // don't let him close!  :-)
  return false;
}

function eXeexInit() {
  window.WindowIsClosing = eXeWindowIsClosing;
  window.tryToClose = eXeTryToClose;
  gBrowser.tabContainer.addEventListener("TabClose", eXeWindowIsClosing, true)
}


