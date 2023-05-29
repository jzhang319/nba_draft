from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func


class League(db.Model):
  __tablename__ = 'leagues'

  if environment == 'production':
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id'), ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='leagues', lazy='dynamic')

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'users': [user.to_dict() for user in self.users],
      'admin': self.admin,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
