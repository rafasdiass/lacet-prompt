# -*- coding: utf-8 -*-
"""User routes."""
from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/profile')
def profile():
    """User profile page."""
    return render_template('user/profile.html')
