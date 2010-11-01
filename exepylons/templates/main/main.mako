<%inherit file="/base.mako" />
<%def name="title()">Main Page</%def>
<div id='packages'>
    <h2> Package List </h2>
    % for package in c.packages:
    <p>${package.title} - ${package.id}</p>
    % endfor
</div>

<input id="createNew" type="submit" action="#" value="Create New"/>
