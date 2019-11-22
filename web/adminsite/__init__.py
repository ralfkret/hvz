from flask import Blueprint

admin = Blueprint('adminsite', __name__, template_folder='adminsite_templates')

from . import views