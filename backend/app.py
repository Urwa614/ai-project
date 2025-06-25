from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
import time
import json
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Career recommendations based on skills and interests
def generate_career_recommendation(skills, interests):
    skills_lower = skills.lower()
    interests_lower = interests.lower()
    
    tech_keywords = ['programming', 'coding', 'developer', 'software', 'web', 'app', 'python', 'javascript', 'java', 'c++', 'react', 'node']
    design_keywords = ['design', 'ui', 'ux', 'graphic', 'creative', 'art', 'drawing', 'photoshop', 'illustrator', 'sketch']
    data_keywords = ['data', 'analysis', 'analytics', 'statistics', 'math', 'excel', 'sql', 'database', 'visualization', 'tableau', 'bi']
    marketing_keywords = ['marketing', 'social media', 'content', 'writing', 'seo', 'advertising', 'brand', 'communication']
    finance_keywords = ['finance', 'accounting', 'economics', 'investment', 'banking', 'stock', 'market', 'business']
    
    # Count keyword matches
    tech_score = sum(1 for keyword in tech_keywords if keyword in skills_lower or keyword in interests_lower)
    design_score = sum(1 for keyword in design_keywords if keyword in skills_lower or keyword in interests_lower)
    data_score = sum(1 for keyword in data_keywords if keyword in skills_lower or keyword in interests_lower)
    marketing_score = sum(1 for keyword in marketing_keywords if keyword in skills_lower or keyword in interests_lower)
    finance_score = sum(1 for keyword in finance_keywords if keyword in skills_lower or keyword in interests_lower)
    
    # Find the highest score
    scores = {
        'tech': tech_score,
        'design': design_score,
        'data': data_score,
        'marketing': marketing_score,
        'finance': finance_score
    }
    
    max_category = max(scores, key=scores.get)
    
    # Generate recommendation based on the highest scoring category
    recommendations = {
        'tech': 'Based on your skills and interests, you would excel in Software Development. Consider focusing on full-stack development to leverage your technical abilities.',
        'design': 'Your creative skills suggest you would thrive in UX/UI Design. Consider building a portfolio showcasing your design thinking and visual communication skills.',
        'data': 'Your analytical mindset makes Data Science an excellent career path. Consider developing expertise in machine learning and data visualization tools.',
        'marketing': 'Your communication skills align well with Digital Marketing. Consider specializing in content strategy or social media management.',
        'finance': 'Your aptitude for numbers suggests a promising career in Financial Analysis. Consider pursuing certifications in financial planning or investment analysis.'
    }
    
    # If no clear match, provide a general recommendation
    if scores[max_category] == 0:
        return 'Based on your profile, consider exploring various fields to discover your passion. Start with short courses in different areas to find what resonates with you.'
    
    return recommendations[max_category]

app = Flask(__name__)
CORS(app)

# Use MongoDB Atlas connection string
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb+srv://girlprisious:UpkMnIvMqFbAst3X@cluster0.mmp5xjh.mongodb.net/urwah?retryWrites=true&w=majority')
mongo = PyMongo(app)

@app.route('/api/profile', methods=['POST'])
def create_profile():
    try:
        # Validate incoming data
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Insert profile
        result = mongo.db.profiles.insert_one(data)
        
        return jsonify({
            'message': 'Profile created successfully', 
            'profile_id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        # Log the full error for debugging
        app.logger.error(f'Error creating profile: {str(e)}')
        return jsonify({
            'error': 'Failed to create profile', 
            'details': str(e)
        }), 500

@app.route('/career-advice', methods=['POST'])
def career_advice():
    if request.method != 'POST':
        return jsonify({"error": "Method Not Allowed"}), 405
    
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    skills = data.get('skills', '')
    interests = data.get('interests', '')
    
    try:
        recommendation = generate_career_recommendation(skills, interests)
        return jsonify({
            "message": "Career advice generated successfully",
            "advice": recommendation
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
