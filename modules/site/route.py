from flask import Blueprint, render_template

from . import template_folder
from .controller import siteController


site_bp = Blueprint(
    'Site Manager', __name__, url_prefix='/site', template_folder=template_folder
)
site_controller = siteController()


@site_bp.route('/', methods=['GET'])
def index():
    result = site_controller.index()
    return render_template('index.html', **result)
