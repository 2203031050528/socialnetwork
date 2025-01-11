from flask import render_template, jsonify, request
from app.models import large_social_network

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/add_user', methods=['POST'])
    def add_user():
        user = request.form['user']
        return jsonify(large_social_network.add_user(user))

    # ... rest of your routes ... 