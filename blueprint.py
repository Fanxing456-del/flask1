from customer import customer_bp
from clerk import clerk_bp
from order import order_bp
from product import product_bp
from flask import Flask
from Model import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123456@localhost/架构_name'
db.init_app(app)
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(clerk_bp, url_prefix='/clerk')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(product_bp,url_prefix='/product')
if __name__ == '__main__':
    app.run()
