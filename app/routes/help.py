from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.user_handler import Users

help_bp = Blueprint('help', __name__)
user_handler = Users()

@help_bp.route('/')
def help():
    return render_template('help.html') 