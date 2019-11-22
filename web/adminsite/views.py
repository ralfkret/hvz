from flask import render_template
from . import admin

@admin.route('product_list')
def product_list():
    return 'product_list'