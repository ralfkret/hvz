from flask import render_template
from . import admin
from web.models import Product

@admin.route('product_list')
def product_list():
    return render_template('product_list.html', products=Product.query.all())