from flask import Blueprint

from myhome.controllers import controller

bp = Blueprint("views", __name__, template_folder="templates")

bp.add_url_rule("/", view_func=controller.index)
bp.add_url_rule("/homepage", view_func=controller.index)

def init_app(app):
    app.register_blueprint(bp)