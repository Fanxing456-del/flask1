from flask_sqlalchemy import SQLAlchemy
# 实例化
db = SQLAlchemy()

class Customer(db.Model):
    """客户模型"""
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(100))

class Clerk(db.Model):
    """职工"""
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))
    department = db.Column(db.String(20))
    position = db.Column(db.String(20))
    phone = db.Column(db.String(20))

class Order(db.Model):
    order_id = db.Column(db.Integer,primary_key = True)
    customer_id = db.Column(db.Integer)
    clerk_id = db.Column(db.Integer)
    total_money = db.Column(db.Integer)
    payment = db.Column(db.String(24))

class Product(db.Model):
    product_id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(24))
    unit_price = db.Column(db.Integer)
    description = db.Column(db.String(64))
    count = db.Column(db.Integer)
