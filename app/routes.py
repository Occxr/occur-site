from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from .models import db, Product
from .forms import ProductForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/cart')
def cart():
    return render_template('cart.html')

@main_bp.route('/products')
def products():
    items = Product.query.all()
    return render_template('products.html', products=items)

@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@main_bp.route('/admin/dashboard')
@login_required
def dashboard():
    products = Product.query.all()
    return render_template('dashboard.html', products=products)

@main_bp.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('product_edit.html', form=form)

@main_bp.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('product_edit.html', form=form)

@main_bp.route('/admin/product/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('main.dashboard'))
