from flask import render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length


from web import db
from web.models import Product

from . import admin


@admin.route('product_list')
def product_list():
    products=Product.query.order_by(Product.id).paginate(per_page=5)
    return render_template('product_list.html', products=products)


class ProductForm(FlaskForm):
    id = IntegerField('Id')
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    wanted_amount = IntegerField('Gewünschte Anzahl', validators=[DataRequired()])

@admin.route('product_delete/<int:id>', methods=['GET', 'POST'])
def product_delete(id):
    product = Product.query.get_or_404(id) 
    form = ProductForm()
    if form.validate_on_submit():
        db.session.delete(product)
        db.session.commit()
        flash(f'Produkt \'{product.name}\' gelöscht.', 'info')
        return redirect(url_for('.product_list'))
    flash(f'Sie löschen das Produkt \'{product.name}\'!', 'danger')
    return render_template('product_delete.html', form=ProductForm(), product=product)

@admin.route('product_edit/<int:product_id>', methods=['GET', 'POST'])
def product_edit(product_id):
    product = Product.query.get(product_id)
    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.wanted_amount = form.wanted_amount.data
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('.product_edit', product_id=product.id))
    return render_template('product_edit.html', form=form, product=product)
