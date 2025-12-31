from flask import Blueprint, request
from models import db, Referendums, ReferendumOptions, Votes, User
from datetime import datetime

from routes.auth import auth_bp

voter_bp = Blueprint('voter', __name__)


@voter_bp.route('/referendums', methods=['GET'])
def get_referendums():
    if request.method == 'GET':
        #only get open referendums
        referendum = Referendums.query.filter_by(status=True).all()

        #prepare response
        response = []

        #get options for each referendum
        for ref in referendum:
            referendum_options = ReferendumOptions.query.filter_by(referendum_id=ref.id).all()

            options_list = [
                {'id': opt.id, 'text': opt.option, 'votes': opt.vote_count}
                for opt in referendum_options
            ]

            response.append({
                'id': ref.id,
                'title': ref.title,
                'description': ref.description,
                'created_at': ref.created_at,
                'options': options_list
            })

    return {'referendums': response}, 200


@voter_bp.route('/referendums/<int:id>', methods=['GET'])
def get_referendum(id):
    if request.method == 'GET':
        referendum = Referendums.query.filter_by(id=id).first()

        if not referendum:
            return {'error': 'referendum not found'}, 404

        options = ReferendumOptions.query.filter_by(referendum_id=id).all()

        options_list = [
            {'id': opt.id, 'text': opt.option, 'votes': opt.vote_count}
            for opt in options
        ]

    return {
        'id': referendum.id,
        'title': referendum.title,
        'description': referendum.description,
        'status': referendum.status,
        'created_at': referendum.created_at,
        'options': options_list
    }, 200


@voter_bp.route('/vote', methods=['POST'])
def vote():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get['user_id']
        referendum_id = data.get['referendum_id']
        option_id = data.get['option_id']


        #validate inputs
        if not user_id or not referendum_id or not option_id:
            return {'message': 'missing fields'}, 400

        #referendum exists and is open
        referendum = Referendums.query.filter_by(id=referendum_id).first()
        if not referendum:
            return {'message': 'referendum not found'}, 404

        if referendum.status != True:
            return {'message': 'referendum is closed'}, 400


        #check user hasn't already voted
        existing_vote = Votes.query.filter_by({
            'user_id': user_id,
            'referendum_id': referendum_id,
        }).first()

        if existing_vote:
            return {'message': 'already voted, cannot vote again.'}, 400

        #check option exists
        option = ReferendumOptions.query.get(option_id)
        if not option:
            return {'message': 'option not found'}, 404
        if option.referendum_id != referendum.id:
            return {'message': 'referendum id mismatch'}, 400

        #create user vote
        new_vote = Votes({
            'user_id': user_id,
            'option_id': option_id,
            'created_at': datetime.now(),
            'referendum_id': referendum.id,
        })

        option.vote_count += 1

        db.session.add(new_vote)
        db.session.commit()

        return {'message': 'vote created'}, 201
