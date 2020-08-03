from helphours import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_pages/404.html')
