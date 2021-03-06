# ===========================================================================
# eXe 
# Copyright 2004-2005, University of Auckland
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================

"""
OutlinePane is responsible for creating the XHTML for the package outline
"""

import logging
from nevow import stan
from nevow.livepage import handler
from exe.webui.renderable import Renderable
log = logging.getLogger(__name__)


# ===========================================================================
class OutlinePane(Renderable):
    """
    OutlinePane is responsible for creating the XHTML for the package outline
    """
    name = 'outlinePane'

    def process(self, request):
        """ 
        Get current package
        """
        log.debug("process")
        
        if "action" in request.args:
            nodeId = request.args["object"][0]
            package = self.package
            log.debug("got action=" + request.args["action"][0])

            if request.args["action"][0] == "changeNode":
                node = package.findNode(nodeId)
                if node is not None:
                    package.currentNode = node
                else:
                    log.error("changeNode cannot locate "+nodeId)

            elif request.args["action"][0] == "addChildNode":
                node = package.findNode(nodeId)
                if node is not None:
                    package.currentNode = node.createChild()
                else:
                    log.error("addChildNode cannot locate "+nodeId)

            elif (nodeId != package.root.id and 
                  request.args["action"][0] == "deleteNode"):
                node = package.findNode(nodeId)
                if node is not None and node is not self.package.root:
                    node.delete()
                    if node.isAncestorOf(package.currentNode):
                        package.currentNode = node.parent
                else:
                    log.error("deleteNode cannot locate "+nodeId)

    def handleAddChild(self, client, parentNodeId):
        """Called from client via xmlhttp. When the addChild button is called.
        Hooked up by authoringPage.py
        """
        node = self.package.findNode(parentNodeId)
        log.debug("handleAddChild parent=" + parentNodeId)
        if node is not None:
            self.package.currentNode = newNode = node.createChild()
            log.debug("XHAddChildTreeItem %s %s" % (newNode.id, newNode.title))
            client.call('XHAddChildTreeItem', newNode.id, parentNodeId, newNode.title)
        else:
            client.call('enableButtons')


    def handleDelNode(self, client, confirm, nodeId):
        """Called from xmlhttp. 
        'confirm' is a string. It is 'false' if the user or the gui has
        cancelled the deletion 'nodeId' is the nodeId
        """
        log.debug("handleDelNode nodeId=" + nodeId)
        if confirm == 'true':
            node = self.package.findNode(nodeId)
            if node is not None and node is not self.package.root:
                # Actually remove the elements in the dom
                client.call('XHDelNode', nodeId)
                # Update our server version of the package
                if (node.isAncestorOf(self.package.currentNode) or 
                    node is self.package.currentNode):
                    self.package.currentNode = node.parent
                node.delete()
            else:
                log.error("deleteNode cannot locate " + nodeId)
                client.call('enableButtons')
        else:
            client.call('enableButtons')


    def handleRenNode(self, client, nodeId, newName):
        """Called from xmlhttp"""
        log.debug("handleRenNode nodeId=%s newName=%s" % (nodeId, newName))
        if newName in ('', 'null'): 
            client.call('enableButtons')
            return
        node = self.package.findNode(nodeId)

        node.title = unicode(newName, 'utf8')
        # and send a signal to the node that it needs to change its anchors,
        # and those of ALL of its children nodes, as well:
        node.RenamedNodePath()

        params = [s.replace('"', '\\"') for s in 
                  [node.titleShort, node.titleLong, node.title]]
        command = u'XHRenNode("%s", "%s", "%s")' % tuple(params)
        log.debug(command)
        client.sendScript(command.encode('utf-8'))
        client.call('enableButtons')
    

    def handleSetTreeSelection(self, client):
        """
        Called when the client want's to update the tree with the correct
        selection
        """
        client.call('XHSelectTreeNode', self.package.currentNode.id)
        
            
    def _doJsRename(self, client, node):
        """
        Recursively renames all children to their default names on
        the client if the node's default name has not been overriden
        """
        log.debug("_doJsRename")
        if not node._title:
            params = [s.replace('"', '\\"') for s in 
                      [node.titleShort, node.titleLong, node.title]]
            params.append(node.id)
            command = 'XHRenNode("%s", "%s", "%s", "%s")' % tuple(params)
            log.debug(command)
            client.sendScript(command)
        for child in node.children: 
            self._doJsRename(client, child)


    def handleDrop(self, client, sourceNodeId, parentNodeId, nextSiblingNodeId):
        """Handles the end of a drag drop operation..."""
        source = self.package.findNode(sourceNodeId)
        parent = self.package.findNode(parentNodeId)
        nextSibling = self.package.findNode(nextSiblingNodeId)
        if source and parent:
            # If the node has a default title and is changing levels
            # Make the client rename the node after we've moved it
            doRename = (not source.title and 
                        parent is not source.parent)
            # Do the move
            if nextSibling:
                assert nextSibling.parent is parent, \
                       '"sibling" has different parent: [%s/%s] [%s/%s]' % \
                        (parent.id, parent.title, nextSibling.id, 
                         nextSibling.title)
                source.move(parent, nextSibling)
                log.info("Dragging %s under %s before %s" % 
                         (source.title, parent.title, nextSibling.title))
            else:
                source.move(parent)
                log.info("Dragging %s under %s at start" % 
                         (source.title, parent.title))
            # Rename on client if it will have changed
            if doRename:
                # Recursively rename all nodes on the client
                self._doJsRename(client, source)
        else:
            log.error("Can't drag and drop tree items")


    def _doJsMove(self, client, node):
        """Makes the javascipt move a node,
        the 'node' param should already have been moved 
        to the new position. This makes the client catch up
        to the server"""
        sibling = node.nextSibling() 
        if sibling:
            siblingId = sibling.id
        else:
            siblingId = 'null'

        if node.parent:
            client.call('XHMoveNode', node.id, node.parent.id, siblingId)


    def handlePromote(self, client, sourceNodeId):
        """Promotes a node"""
        node = self.package.findNode(sourceNodeId)
        if node.promote():
            self._doJsMove(client, node)
            self._doJsRename(client, node)
        else:
            client.call('enableButtons')

    def handleDemote(self, client, sourceNodeId):
        """Demotes a node"""
        node = self.package.findNode(sourceNodeId)
        if node.demote():
            self._doJsMove(client, node)
            self._doJsRename(client, node)
        else:
            client.call('enableButtons')


    def handleUp(self, client, sourceNodeId):
        """Moves a node up its list of siblings"""
        node = self.package.findNode(sourceNodeId)
        if node.up():
            self._doJsMove(client, node)
            self._doJsRename(client, node)
        else:
            client.call('enableButtons')


    def handleDown(self, client, sourceNodeId):
        """Moves a node down its list of siblings"""
        node = self.package.findNode(sourceNodeId)
        if node.down():
            self._doJsMove(client, node)
            self._doJsRename(client, node)
        else:
            client.call('enableButtons')


    def render(self, ctx, data):
        """
        Returns an xul string for viewing this pane.
        The xul is stored in a tuple inside the methods of this class
        then new lines are added when we actually return it
        """
        # Now do the rendering
        log.debug("render")
        xul = (u'<!-- start outline pane -->',
                '    <tree id="outlineTree"',
                '          hidecolumnpicker="true" ',
                '          onselect="outlineClick()" ',
                '          context="outlineMenu" flex="1"',
                '          ondraggesture="treeDragGesture(event)"',
                '          ondragenter="treeDragEnter(event)"',
                '          ondragover="treeDragOver(event)"',
                '          ondragexit="treeDragExit(event)"',
                '          ondragdrop="treeDragDrop(event)"',
                '          ondblclick="eval(document.getElementById('
                """'btnRename').getAttribute('oncommand'))">""",
                '        <treecols>',
                '            <treecol id="sectionCol" primary="true" '+
                'style="font-weight: bold" label="%s" flex="1"/>' \
                       % _(u"Outline"),
                '        </treecols>',
                '        <treechildren>',)
        xul += self.__renderNode(self.package.root, 12)
        xul += ('       </treechildren>',
                '    </tree>',
                '<!-- end outline pane -->')
        return stan.xml('\n'.join(xul))

    def encode2nicexml(self, string):
        """
        Turns & into &amp; etc
        """
        xmlEntities = [('&', '&amp;'),
                       ('"', '&quot;'),
                       ("'", '&apos;'),
                       ('<', '&lt;'),
                       ('>', '&gt;')]
        for src, dest in xmlEntities:
            string = string.replace(src, dest)
        return string

    def __renderNode(self, node, indent, extraIndent=2):
        """
        Renders all children recursively.
        'indent' is the number of spaces to put in front of each line of xul
        'extraIndent' is the extra number of spaces to put for the next level
        when recursing (this is really used as a local static constant)
        """
        if node.children:
            start = '<treeitem container="true" open="true">'
        else:
            start = '<treeitem>'

        # Render the inner bits
        titleShort = self.encode2nicexml(node.titleShort)
        titleFull = self.encode2nicexml(node.title)
        xul = ('%s' % start,
               """    <treerow _exe_nodeid="%s"> """ % node.id,
               '        <treecell label="%s" name="%s"/>' % (
                            titleShort, titleFull),
               '    </treerow>')

        # Recursively render children if necessary
        if node.children:
            xul += ('    <treechildren>',)
            for child in node.children:
                xul += self.__renderNode(child, indent + extraIndent)
            xul += ('    </treechildren>',)
        xul += ('</treeitem>',)
        # Return nicely indented xul
        return tuple([(' ' * indent) + line for line in xul])
    
# ===========================================================================
