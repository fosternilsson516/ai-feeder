from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.user_handler import Users

admin_center_bp = Blueprint('admin_center', __name__)
user_handler = Users()

@admin_center_bp.route('/')
def admin_center():
    return render_template('admin_center.html') 

@admin_center_bp.route('/services')
def services():
    return render_template('services.html')    

@admin_center_bp.route('/manage_employees')
def manage_employees():
    return render_template('manage_employees.html')    

@admin_center_bp.route('/upload_files')
def upload_files():
    return render_template('upload_files.html')

@admin_center_bp.route('/customer_info')
def customer_info():
    return render_template('customer_info.html')

@admin_center_bp.route('/customer_portal')
def customer_portal():
    return render_template('customer_portal.html')
               