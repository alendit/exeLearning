<%inherit file="/base.mako" />
<%def name="title()">Login</%def>
<%def name="head_tags()"></%def>
<div id='login_form'>
${h.form(url(controller='login', action='submit'))}
  <p>Login: ${h.text('login')}</p>
  <p>Password: ${h.password('password')}</p>
  <p>${h.submit('submit_login', 'Login')}</p>
${h.end_form()}
</div>