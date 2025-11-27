from flask import Blueprint,request,jsonify
from Model import Order,db,Clerk
import json
order_bp = Blueprint('order',__name__)

@order_bp.route('/create_orders',methods = ['POST'])
def create_orders():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Miss'})

    try:
        order = Order(
            order_id = data['order_id'],
            customer_id=data['customer_id'],
            clerk_id=data['clerk_id'],
            total_money=data['total_money'],
            payment = data['payment']
        )

        db.session.add(order)
        db.session.commit()
        return jsonify({
            'order_id': order.order_id,
            'customer_id': order.customer_id,
            'clerk_id': order.clerk_id,
            'total_money': order.total_money,
            'payment':order.payment
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@order_bp.route('/get_price/<int:order_id>')
def get_price(order_id):
    """优惠政策"""
    order = Order.query.get(order_id)
    total_money = order.total_money
    if 5000 > total_money  > 1000:
        final_money = total_money * 0.97
    elif total_money > 5000:
        final_money = total_money * 0.95
    else:
        final_money = total_money
    return jsonify(final_money)

@order_bp.route('/get_clerk_name/<int:order_id>')
def get_clerk_name(order_id):
    """订单号找职工"""
    try:

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error':'order not found'})
        id = order.clerk_id
        clerk = Clerk.query.get(id)
        if not clerk:
            return jsonify({'error': 'clerk not found'})
        return jsonify({'clerk_name':clerk.name})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500