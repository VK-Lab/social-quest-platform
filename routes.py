from flask import jsonify, request
from flask_restful import Resource
from app import app, api, db, limiter
from models import Quest, QuestProgress, User
from auth import token_required
from datetime import datetime
import logging

class QuestList(Resource):
    method_decorators = [token_required]

    @limiter.limit("30/minute")
    def get(self, current_user):
        logging.debug(f"GET /api/quests request from user {current_user.username}")
        quests = Quest.query.filter_by(is_active=True).all()
        return jsonify([{
            'id': q.id,
            'title': q.title,
            'description': q.description,
            'xp_reward': q.xp_reward,
            'required_level': q.required_level
        } for q in quests])

    @limiter.limit("10/minute")
    def post(self, current_user):
        logging.debug(f"POST /api/quests request from user {current_user.username}")
        data = request.get_json()

        if not all(k in data for k in ('title', 'description', 'xp_reward')):
            return {'message': 'Missing required fields'}, 400

        new_quest = Quest(
            title=data['title'],
            description=data['description'],
            xp_reward=data['xp_reward'],
            required_level=data.get('required_level', 0)
        )

        db.session.add(new_quest)
        db.session.commit()

        return {
            'message': 'Quest created successfully',
            'quest_id': new_quest.id
        }, 201

class QuestProgressResource(Resource):
    method_decorators = [token_required]

    @limiter.limit("30/minute")
    def post(self, current_user, quest_id):
        logging.debug(f"POST /api/quests/{quest_id}/complete request from user {current_user.username}")
        quest = Quest.query.get_or_404(quest_id)

        # Check if quest is already completed
        existing_progress = QuestProgress.query.filter_by(
            user_id=current_user.id,
            quest_id=quest_id
        ).first()

        if existing_progress and existing_progress.status == 'completed':
            return {'message': 'Quest already completed'}, 400

        if not existing_progress:
            progress = QuestProgress(
                user_id=current_user.id,
                quest_id=quest_id
            )
            db.session.add(progress)
        else:
            progress = existing_progress

        progress.status = 'completed'
        progress.completed_at = datetime.utcnow()

        # Update user XP
        current_user.xp_total += quest.xp_reward

        db.session.commit()

        return {
            'message': 'Quest completed successfully',
            'xp_gained': quest.xp_reward,
            'total_xp': current_user.xp_total
        }, 200

class UserProgress(Resource):
    method_decorators = [token_required]

    @limiter.limit("30/minute")
    def get(self, current_user):
        logging.debug(f"GET /api/user/progress request from user {current_user.username}")
        progress = QuestProgress.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'user': {
                'username': current_user.username,
                'xp_total': current_user.xp_total
            },
            'quests': [{
                'quest_id': p.quest_id,
                'title': p.quest.title,
                'status': p.status,
                'completed_at': p.completed_at.isoformat() if p.completed_at else None
            } for p in progress]
        })

# Register resources
api.add_resource(QuestList, '/api/quests')
api.add_resource(QuestProgressResource, '/api/quests/<int:quest_id>/complete')
api.add_resource(UserProgress, '/api/user/progress')