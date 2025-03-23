from flask import Blueprint, render_template
from .controller import AccessController

access_bp = Blueprint('access', __name__)
access_controller = AccessController()

@access_bp.route('/', methods=['GET'])
def index():
    result = {}
    return render_template('access/index.html', **result)