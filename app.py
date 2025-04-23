from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_trends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Load and preprocess data
def load_data():
    df = pd.read_csv('Viral_Social_Media_Trends.csv')
    return df

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # In production, use proper password hashing
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
            
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    df = load_data()
    
    # Basic statistics
    total_posts = len(df)
    avg_views = df['Views'].mean()
    avg_likes = df['Likes'].mean()
    
    # Platform distribution
    platform_dist = df['Platform'].value_counts()
    
    # Engagement level distribution
    engagement_dist = df['Engagement_Level'].value_counts()
    
    return render_template('dashboard.html',
                         total_posts=total_posts,
                         avg_views=avg_views,
                         avg_likes=avg_likes,
                         platform_dist=platform_dist,
                         engagement_dist=engagement_dist)

@app.route('/analytics')
@login_required
def analytics():
    df = load_data()
    
    # Create visualizations
    fig_platform = px.bar(df['Platform'].value_counts(), 
                         title='Posts by Platform')
    fig_engagement = px.pie(df['Engagement_Level'].value_counts(),
                           title='Engagement Level Distribution')
    
    return render_template('analytics.html',
                         fig_platform=fig_platform.to_html(),
                         fig_engagement=fig_engagement.to_html())

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        platform = request.form['platform']
        content_type = request.form['content_type']
        hashtag = request.form['hashtag']
        region = request.form['region']
        
        # Load and preprocess data
        df = load_data()
        
        # Create label encoders for categorical variables
        label_encoders = {}
        categorical_columns = ['Platform', 'Content_Type', 'Hashtag', 'Region']
        
        for column in categorical_columns:
            label_encoders[column] = LabelEncoder()
            df[column] = label_encoders[column].fit_transform(df[column])
        
        # Prepare features and target
        X = df[categorical_columns]
        y = df['Engagement_Level']
        
        # Train model
        model = RandomForestClassifier()
        model.fit(X, y)
        
        # Prepare input data for prediction
        input_data = {
            'Platform': platform,
            'Content_Type': content_type,
            'Hashtag': hashtag,
            'Region': region
        }
        
        # Transform input data using the same label encoders
        for column in categorical_columns:
            input_data[column] = label_encoders[column].transform([input_data[column]])[0]
        
        # Make prediction
        prediction = model.predict([[
            input_data['Platform'],
            input_data['Content_Type'],
            input_data['Hashtag'],
            input_data['Region']
        ]])
        
        return render_template('prediction_result.html',
                             prediction=prediction[0])
    
    return render_template('predict.html')

@app.route('/export', methods=['GET'])
@login_required
def export_data():
    df = load_data()
    
    # Create export options
    export_format = request.args.get('format', 'csv')
    
    if export_format == 'csv':
        return df.to_csv(index=False)
    elif export_format == 'excel':
        return df.to_excel(index=False)
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 