from flask import Blueprint, redirect, url_for


main = Blueprint('main', __name__)

from . import errors

@main.route('/')
@main.route('/defaultsite')
def index():
    return redirect(url_for('adminsite.product_list'))