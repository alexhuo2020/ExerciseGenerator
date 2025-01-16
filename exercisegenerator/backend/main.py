from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

import numpy as np 
import random

from llm_agent import ai_answer, ai_question, ai_evaluation, ai_answer_code, ai_evaluation_code, ai_tutorial


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/exercisegenerator'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Table for the Game, including user input information
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    character_name = db.Column(db.String(100), nullable=False)
    expert_name = db.Column(db.String(100), nullable=False)
    game_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    problem_type = db.Column(db.String(100), nullable=True)
    problem_level = db.Column(db.String(100), nullable=True)

    # Relationship, all problems associated
    problem = db.relationship('Problem', backref='game', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'userid': self.user_id,
            'user_name': self.user_name,
            'character_name': self.character_name,
            'expert_name': self.expert_name,
            'game_name': self.game_name,
            'created_at': self.created_at.isoformat()
        }

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=True)
    user_solution = db.Column(db.Text, nullable=True)
    score = db.Column(db.Text, nullable=True)
    problem_type = db.Column(db.String(100), nullable=False)
    problem_level = db.Column(db.String(100), nullable=False)


# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/api/start_game', methods=['POST'])
def start_game():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [ 'userName', 'userId', 'characterName', 'expertName', 'gameName']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create new game choice record
        new_game = Game(
            user_id = data['userId'],
            user_name=data['userName'],
            character_name=data['characterName'],
            expert_name=data['expertName'],
            game_name=data['gameName'],
            problem_type=data['problemType'],
            problem_level=data['problemLevel']
        )

        # Save to database
        db.session.add(new_game)
        db.session.commit()

        return jsonify({
            'message': 'New game information set successfully.',
            'data': new_game.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_game/<user_id>', methods=['GET'])
def get_choices(user_id):
    try:
        games = Game.query.filter_by(user_id=user_id).all()
        return jsonify({
            'game': [game.to_dict() for game in games]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/get_recent_game/<user_id>', methods=['GET'])
def get_recent_game(user_id):
    try:
        # Fetch the most recent game by ordering by timestamp in descending order and limiting to 1
        recent_game = Game.query.filter_by(user_id=user_id).order_by(Game.created_at.desc()).first()
        
        if recent_game:
            return jsonify({'recent_choice': recent_game.to_dict()}), 200
        else:
            return jsonify({'message': 'No game found for this user'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_all_games', methods=['GET'])
def get_all_games():
    try:
        choices = Game.query.all()
        return jsonify({
            'choices': [choice.to_dict() for choice in choices]
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/problem', methods = [ 'POST'])
def problem():
    try:
        data = request.json
        character_name = data['characterName']
        expert_name = data['expertName']
        game_name = data['gameName']
        level = data['problemLevel']
        types = data['problemType']
        if level == 'Random':
            levels =["Easy", "Intermediate", "Difficult", "Super Difficult", "Random"]
            level = random.choice(levels) 
        
        if types == 'Random':
            all_types = ["Multiple Choice", "Coding", "T/F", "Eassy",  "Written Response", "Random"]
            types = random.choice(all_types)

        # Generate question with AI
        result = ai_question(character_name, expert_name, game_name, level, types)
        if types != 'coding':
            ans = ai_answer(result['question'], history=[''])
        else:
            ans = ai_answer_code(result['question'], history=[''])
            

        # Add the problem to database, associate with the game id
        game = Game.query.filter_by(user_id=data['userId']).order_by(Game.created_at.desc()).first() # get the current game
        
        new_problem = Problem(
            game_id=game.id,
            description=result['question'],
            solution=ans['answer'],
            problem_type=types,
            problem_level=level
        )

        db.session.add(new_problem)
        db.session.commit()

        print("succesful")
        return jsonify({'problemId':new_problem.id,'question': result['question'], 'history': result['history'], 'answer': ans['answer']
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/answer', methods = [ 'POST'])
def answer():
    try:
        data =request.json
        question = data['question']

        result = ai_answer(question, history='')

        return jsonify({'answer': result['answer']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        problem_id = data['problemId']
        problem = Problem.query.filter_by(id=problem_id).first()


        
        human_answer = data['prompt']
        history_content = data['history']
        history = []
        history.append(f'AI: question:\n {problem}')

        for items in history_content:
            history.append(items['author'] + " : " + items['content'])

        if 'correct answer' in human_answer:
            # ans = ai_answer(problem, history)
            # ## ADD answer to the problem
            # problem.solution = ans['answer']
            # db.session.commit()

            return jsonify(prediction=problem.solution), 201 
        else:
            if problem.problem_type != 'coding':
                eval = ai_evaluation(problem,  history, human_answer)
                score = eval['score']
                history = eval['history']
                problem.user_solution = human_answer
                problem.score = score 
                db.session.commit()
            else:
                eval = ai_evaluation_code(problem,  history, human_answer)
                score = eval['score']
                history = eval['history']
                problem.user_solution = human_answer
                problem.score = score 
                db.session.commit()

            return jsonify(prediction=eval['evaluation'], score=score), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tutorial', methods=['POST'])
def tutorial():
    try:
        data = request.json
        character_name = data['characterName']
        expert_name = data['expertName']
        game_name = data['gameName']
        level = data['problemLevel']
        types = data['problemType']
        if level == 'Random':
            levels =["Easy", "Intermediate", "Difficult", "Super Difficult", "Random"]
            level = random.choice(levels) 
        
        if types == 'Random':
            all_types = ["Multiple Choice", "Coding", "T/F", "Eassy",  "Written Response", "Random"]
            types = random.choice(all_types)

        # Generate question with AI
        result = ai_tutorial(character_name, expert_name, game_name, types)
            
        print("succesful")
        return jsonify({'tutorial':result['tutorial']
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
   

if __name__ == '__main__':
    app.run(debug=True, port=5000)
