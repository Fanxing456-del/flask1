from flask import Blueprint,request,jsonify
from Model import Customer,db
import json
from redis_config import redis_client
customer_bp = Blueprint('customer',__name__)

@customer_bp.route('/create_customers',methods = ['POST'])
def create_customers():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Miss'})

    try:
        customer = Customer(
            id=data['id'],
            name=data['name'],
            phone=data['phone'],
            address=data['address']
        )

        db.session.add(customer)
        db.session.commit()
        return jsonify({
            'id': customer.id,
            'name': customer.name,
            'phone': customer.phone,
            'address': customer.address
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/cache_all_customers')
def cache_all_customers():
    try:
        customers = db.session.query(Customer).all()
        print(f"查询到 {len(customers)} 条记录")

        cached_count = 0
        for customer in customers:
            cache_key = f"user:{customer.id}"
            customer_data = {
                'id': customer.id,
                'name': customer.name,
                'phone': customer.phone,
                'address': customer.address
            }
            redis_client.setex(cache_key, 300, json.dumps(customer_data))
            cached_count += 1
            print(f"已缓存消费者 {customer.id}")

        return jsonify({'message': f"成功缓存{cached_count}个人"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/get_all_customers')
def get_all_customers():
    try:
        keys = redis_client.keys("*")

        if not keys:
            return jsonify([])
        # 将 bytes 转换为字符串列表
        string_keys = [key.decode('utf-8') for key in keys]

        customers = []
        for key in string_keys:
            cached_data = redis_client.get(key)
            if cached_data:
                customer_data = json.loads(cached_data.decode('utf-8'))
                customers.append(customer_data)

        return jsonify(customers)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500