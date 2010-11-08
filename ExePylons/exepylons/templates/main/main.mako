<%inherit file="/base.mako" />
<%def name="title()">Main Page</%def>
<%def name="head_tags()">${h.javascript_link('/scripts/common.js')}</%def>
<div id='packages'>
    <h2> Package List </h2>
    % for package in c.packages:
    <p><a href='/package/index/${package.id}'>${package.title} - ${package.id}</a><p>
    % endfor
</div>
${h.text("And Zoidberg")}

<input id="createNew" type="submit" action="#" value="Create New"/>
