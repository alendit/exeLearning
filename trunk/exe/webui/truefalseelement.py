# ===========================================================================
# eXe 
# Copyright 2004-2006, University of Auckland
# Copyright 2004-2008 eXe Project, http://eXeLearning.org
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
TrueFalseElement is responsible for a block of question. Used by TrueFalseBlock.
"""

import logging
from exe.webui         import common
from exe.webui.element import TextAreaElement

log = logging.getLogger(__name__)
# ===========================================================================
class TrueFalseElement(object):
    """
    TrueFalseElement is responsible for a block of question. 
    Used by TrueFalseBlock.
    """
    def __init__(self, index, idevice, question):
        """
        Initialize
        """
        self.index      = index
        self.id         = unicode(index) + "b" + idevice.id        
        self.idevice    = idevice

        self.question   = question
        # also split out each part for a separate TextAreaElement:
        # but first...
        # to compensate for the strange unpickling timing when objects are 
        # loaded from an elp, ensure that proper idevices are set:
        if question.questionTextArea.idevice is None: 
            question.questionTextArea.idevice = idevice
        if question.feedbackTextArea.idevice is None: 
            question.feedbackTextArea.idevice = idevice
        if question.hintTextArea.idevice is None: 
            question.hintTextArea.idevice = idevice
        #
        self.question_question = TextAreaElement(question.questionTextArea)
        self.question_feedback = TextAreaElement(question.feedbackTextArea)
        self.question_hint = TextAreaElement(question.hintTextArea)

        # note, question.isCorrect is left as it was, and not split out.
        # because there are low-level mechanisms in place somewhere 
        # with the radio buttons or ??? expecting that as such.
        
        self.questionId = "question"+ unicode(index) + "b" + idevice.id
        self.question_question.id = self.questionId
        self.feedbackId = "feedback" + unicode(index) + "b" + idevice.id 
        self.question_feedback.id = self.feedbackId
        self.hintId     = "hint" + unicode(index) + "b" + idevice.id 
        self.question_hint.id = self.hintId
        self.keyId      = "Key" + unicode(index) + "b" + idevice.id       

    def process(self, request):
        """
        Process arguments from the web server.  Return any which apply to this 
        element.
        """
        log.debug("process " + repr(request.args))

        is_cancel = common.requestHasCancel(request)

        if self.questionId in request.args \
        and not is_cancel:
            self.question_question.process(request)
            
        if self.hintId in request.args \
        and not is_cancel:
            self.question_hint.process(request)
                        
        if self.keyId in request.args \
        and not is_cancel:
            if request.args[self.keyId][0] == "true":
                self.question.isCorrect = True 
                log.debug("question " + repr(self.question.isCorrect))
            else:
                self.question.isCorrect = False        
        
        if self.feedbackId in request.args \
        and not is_cancel:
            self.question_feedback.process(request)
            
        if "action" in request.args and request.args["action"][0] == self.id:
            # before deleting the question object, remove any internal anchors:
            for q_field in self.question.getRichTextFields():
                 q_field.ReplaceAllInternalAnchorsLinks()  
                 q_field.RemoveAllInternalLinks()  
            self.idevice.questions.remove(self.question)
            # disable Undo once a question has been deleted: 
            self.idevice.undo = False

    def renderEdit(self):
        """
        Returns an XHTML string for editing this option element
        """
        
        html = self.question_question.renderEdit()

        html += _("True") + " " 
        html += common.option(self.keyId, self.question.isCorrect, "true") 
        html += _("False") + " " 
        html += common.option(self.keyId, not self.question.isCorrect, "false") 

        html += "<br/><br/>\n"

        html += common.elementInstruc(self.idevice.keyInstruc)
        
        html += self.question_feedback.renderEdit()
        html += self.question_hint.renderEdit()
        
        html += common.submitImage(self.id, self.idevice.id, 
                                   "/images/stock-cancel.png",
                                   _("Delete question"))
        html += "<br/><br/>\n"
        return html
    
    def renderQuestionView(self):
        """
        Returns an XHTML string for viewing this question element
        """
        is_preview = 0
        html  = self.renderQuestion(is_preview)
        if self.question.hintTextArea.content.strip() != "":
            html += u'<span '
            html += u'style="background-image:url(\'panel-amusements.png\');">'
            html += u'\n<a onmousedown="Javascript:updateCoords(event);'
            html += u'showMe(\'%s\', 350, 100);" ' % self.hintId
            html += u'style="cursor:help;align:center;vertical-align:middle;" '
            html += u'title="%s" \n' % _(u"Hint")
            html += u'href="javascript:void(0);">&nbsp;&nbsp;&nbsp;&nbsp;</a>'
            html += u'</span>'
            html += u'<div id="'+self.hintId+'" '
            html += u'style="display:none; z-index:99;">'
            html += u'<div style="float:right;" >'
            html += u'<img alt="%s" ' % _('Close')
            html += u'src="stock-stop.png" title="%s"' % _('Close')
            html += u" onmousedown=\"Javascript:hideMe();\"/></div>"
            html += u'<div class="popupDivLabel">'
            html += _(u"Hint")
            html += u'</div>\n'
            html += self.question_hint.renderView()
            html += u"</div>\n"
        
        return html
    
    def renderQuestionPreview(self):
        #TODO merge renderQuestionView and renderQuestionPreview
        """
        Returns an XHTML string for previewing this question element
        """
        is_preview = 1
        html  = self.renderQuestion(is_preview)
        html += " &nbsp;&nbsp;\n"

        html += common.elementInstruc(self.question_hint.field.content, 
                                      "panel-amusements.png", "Hint")
        return html

    def renderQuestion(self, is_preview):
        """
        Returns an XHTML string for viewing and previewing this question element
        """
        log.debug("renderPreview called in the form of renderQuestion")
    
        html  = u"<br/><br/>"

        if is_preview:
            html += self.question_question.renderPreview() + "<br/>" 
        else: 
            html += self.question_question.renderView() + "<br/>"

        html += _("True") + " " 
        html += self.__option(0, 2, "true") + " \n"
        html += _("False") + " " 
        html += self.__option(1, 2, "false") + "\n"
       
        return html
    
    def __option(self, index, length, true):
        """Add a option input"""
        html  = u'<input type="radio" name="option%s" ' % self.id
        html += u'id="%s%s" ' % (true, self.id)
        html += u'onclick="getFeedback(%d,%d,\'%s\',\'truefalse\')"/>' % (
                index, length, self.id)
        return html
    
    def renderFeedbackPreview(self):
        """
        Merely a front-end to renderFeedbackView(), setting preview mode.
        Note: this won't really matter all that much, since these won't yet
        show up in exported printouts, BUT the image paths will be correct.
        """
        return self.renderFeedbackView(is_preview=True)

    def renderFeedbackView(self, is_preview=False):
        """
        return xhtml string for display this option's feedback
        """
        feedbackStr1 = _(u"Correct!") + " "
        feedbackStr2 = _(u"Incorrect!") + " "

        # embed a score_representation as well, even==true,
        # so that Correct/Incorrect doesn't need to be un-translated
        # upon bursting from a CC export.
        # start off with a sorta random looking number:
        to_even1 = int(self.idevice.id)+5
        if to_even1 % 2:
            # ensure that to_even1 is indeed even, correct:
            to_even1 += 1
        # and ensure that to_even2 is odd, incorrect:
        to_even2 = to_even1 + 1


        if not self.question.isCorrect:
            feedbackStr1, feedbackStr2 = feedbackStr2, feedbackStr1 
            to_even1, to_even2 = to_even2, to_even1

        feedbackId1 = "0" + "b" + self.id
        feedbackId2 = "1" + "b" + self.id
        html  = u'<div id="s%s" style="color: rgb(0, 51, 204);' % feedbackId1
        html += u'display: none;" even_steven="%s">' % (str(to_even1))
        html += feedbackStr1 + '</div>\n'
        html += u'<div id="s%s" style="color: rgb(0, 51, 204);' % feedbackId2
        html += u'display: none;" even_steven="%s">' % (str(to_even2))
        html += feedbackStr2 + '</div>\n'
        html += u'<div id="sfbk%s" style="color: rgb(0, 51, 204);' % self.id
        html += u'display: none;">' 
        if is_preview:
            html += self.question_feedback.renderPreview()
        else:
            html += self.question_feedback.renderView()
        html += u'</div>\n'
        
        return html
        
    
# ===========================================================================
