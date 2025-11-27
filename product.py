from flask import Blueprint,request,jsonify
from Model import Product,db
import json
from redis_config import redis_client

product_bp = Blueprint('product',__name__)

@product_bp.route('/product/cache_all_products')
def cache_all_products():
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