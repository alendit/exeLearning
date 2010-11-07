<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
        <title>EXE Main: ${self.title()}</title>
        ${h.javascript_link('/scripts/jquery.js')}
        ${self.head_tags()}
    </head>
    <body>
        <h1>${self.title()}</h1>

<!-- ***BEGIN page content -->
${self.body()}
<!-- ***END page content -->

    </body>
</html>
