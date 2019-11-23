from flask import render_template
from . import admin
from web.models import Product

@admin.route('product_list')
def product_list():
    products=Product.query.paginate()
    show_pages = [1] + [i for i in range(products.page - 5, products.page +5)] + [products.pages]
    return render_template('product_list.html', products=products, show_pages=show_pages)