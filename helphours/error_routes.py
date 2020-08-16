from helphours import app, log
from flask import render_template, request


@app.errorhandler(404)
def page_not_found(error):
    log.error(f'A 404 error was raised for path={request.path}')
    return render_template('error_pages/404.html'), 404
