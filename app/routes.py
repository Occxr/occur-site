from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from .models import db, Product, CartItem, Order, OrderItem
from .forms import ProductForm
from datetime import datetime
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

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

@main_bp.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.username == 'admin':
        return redirect(url_for('main.home'))

    orders = Order.query.order_by(Order.timestamp.desc()).all()
    return render_template('admin_orders.html', orders=orders)


@main_bp.route('/start_crypto_checkout')
@login_required
def start_crypto_checkout():
    order = Order.query.filter_by(user_id=current_user.id).order_by(Order.timestamp.desc()).first()

    if not order or order.is_paid:
        return redirect(url_for('main.cart'))

    total = sum(item.product.price * item.quantity for item in order.items)

    api_url = 'https://api.oxapay.com/v1/payment/invoice'

    payload = {
        "amount": float(f"{total:.2f}"),
        "currency": "USD",
        "lifetime": 60,
        "fee_paid_by_payer": 1,
        "under_paid_coverage": 2.5,
        "auto_withdrawal": False,
        "mixed_payment": False,
        "callback_url": f"https://occur-site.onrender.com/oxapay_callback?token={os.getenv('OXAPAY_WEBHOOK_SECRET')}",
        "return_url": url_for('main.orders', _external=True),
        "email": f"{current_user.username}@occxr.store",
        "order_id": f"occxr_order_{order.id}",
        "thanks_message": "Thanks for your order!",
        "description": f"Order #{order.id}",
        "sandbox": False
    }

    headers = {
    'merchant_api_key': os.getenv("OXAPAY_API_KEY"),
    'Content-Type': 'application/json'
}

    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        result = response.json()

        payment_url = result.get("data", {}).get("payment_url")
        if not payment_url:
            raise Exception("payment_url missing in OxaPay response.")

        return redirect(payment_url)

    except Exception as e:
        print("OxaPay error:", e)
        return redirect(url_for('main.cart'))

@main_bp.route('/oxapay_callback', methods=['POST'])
def oxapay_callback():
    token = request.args.get("token")
    if token != os.getenv("OXAPAY_WEBHOOK_SECRET"):
        return "unauthorized", 401

    data = request.json
    order_id = data.get("order_id")
    status = data.get("status")

    if not order_id or not status:
        return "invalid", 400

    try:
        order_id_num = int(order_id.replace("occxr_order_", ""))
        order = Order.query.get(order_id_num)

        if order and status.lower() == "completed":
            order.is_paid = True
            db.session.commit()
            return "ok", 200

    except Exception as e:
        print("Webhook error:", str(e))
        return "error", 500

    return "ignored", 200