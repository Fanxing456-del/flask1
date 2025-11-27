from flask import Blueprint,request,jsonify
from Model import Clerk,db
import json

clerk_bp = Blueprint('clerk',__name__)

@clerk_bp.route('/create_clerks',methods = ['POST'])
def create_clerk():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Miss'})

    try:
        clerk = Clerk(
            id = data['id'],
            name=data['name'],
            phone=data['phone'],
            department=data['department'],
            position = data['position']
        )

        db.session.add(clerk)
        db.session.commit()
        return jsonify({
            'id': clerk.id,
            'name': clerk.name,
            'phone': clerk.phone,
            'department': clerk.department,
            'position':clerk.position
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clerk_bp.route("/cache_all_clerks")
def cache_all_clerks():
    try:
        clerks = db.session.query(Clerk).all()
        print(f"查询到 {len(clerks)} 条记录")

        cached_count = 0
        for clerk in clerks:
            cache_key = f"user:{clerk.id}"
            clerk_data = {
                'id': clerk.id,
                'name': clerk.name,
                'department':clerk.department,
                'phone': clerk.phone,
                'position': clerk.position
            }
            redis_client.setex(cache_key, 300, json.dumps(clerk_data))
            cached_count += 1
            print(f"已缓存职工 {clerk.id}")

        return jsonify({'message': f"成功缓存{cached_count}个人"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
