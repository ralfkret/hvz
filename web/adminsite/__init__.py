from flask import Blueprint

admin = Blueprint('adminsite', __name__)

from . import views