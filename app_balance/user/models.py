# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app_balance.extensions import bcrypt, db


class Role(db.Model):
    """A role for a user."""

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role(name={self.name})>"


class User(UserMixin, db.Model):
    """A user of the app."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.LargeBinary(128), nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=dt.datetime.utcnow
    )
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Establish a relationship with the Role model
    roles = relationship("Role", back_populates="user", cascade="all, delete-orphan")

    @hybrid_property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set password."""
        self._password = bcrypt.generate_password_hash(value.encode('utf-8'))

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self._password, value.encode('utf-8'))

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User(username={self.username!r}, email={self.email!r})>"
