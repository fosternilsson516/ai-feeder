from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.user_handler import Users


analytics_bp = Blueprint('analytics', __name__)
user_handler = Users()

@analytics_bp.route('/')
def analytics():
    return render_template('owner/analytics.html')  