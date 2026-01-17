from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(50), default='Main')  # Dessert, Drink, Main, Snack
    chef_recommend = db.Column(db.Boolean, default=False)
    available = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'category': self.category,
            'chef_recommend': self.chef_recommend
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    message = db.Column(db.String(500))  # 爱的留言
    status = db.Column(db.String(20), default='pending')  # pending, cooking, ready, served
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    dish = db.relationship('Dish', backref='orders')

    def to_dict(self):
        return {
            'id': self.id,
            'dish_title': self.dish.title,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.strftime('%H:%M')
        }
