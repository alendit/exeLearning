// Need to set window.* methods after window is loaded apparently

window.addEventListener("load", eXeexInit, true);

function eXeWindowIsClosing() {
  // try to prevent closing the main window
  var mainWin = content.document.getElementById('mainWindow');
  if (mainWin != null){
    var target = content.document.getElementById('menu-quit');
    var evObj = document.createEvent('MouseEvents');
    evObj.initMouseEvent( 'click', true, true, window, 1, 12, 345, 7, 220, false, false, true, false, 0, null );
    target.dispatchEvent(evObj);
    return false;
  } else {
    gBrowser.removeCurrentTab();
    return false;
  }
}

function eXeTryToClose(arg) {
  alert("Please use eXe's\n   File... Quit\nmenu to close eXe.");
  // don't let him close!  :-)
  return false;
}

function eXeexInit() {
  window.WindowIsClosing = eXeWindowIsClosing;
  window.tryToClose = eXeWindowIsClosing;
  gBrowser.tabContainer.addEventListener("TabClose", eXeWindowIsClosing, true)
}


