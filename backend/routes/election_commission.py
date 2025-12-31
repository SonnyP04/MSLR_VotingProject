from flask import Blueprint, request
from models import db, Referendums, ReferendumOptions
from datetime import datetime

ec_bp = Blueprint('election_commission', __name__)



@ec_bp.route('/referendum', methods=['POST'])
def create_referendum():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')


    if not title or not description:
        return {'message': 'Missing required fields'}, 400


    new_referendum = Referendums(
        title=title,
        description=description,
        status=False,
        created_at=datetime.now()
    )


    db.session.add(new_referendum)
    db.session.commit()

    return {'message': 'Referendum created', 'referendum_id': new_referendum.id}, 201



@ec_bp.route('/referendum/<int:id>/options', methods=['POST'])
def add_option(id):
    data = request.get_json()
    option_text = data.get('option')


    if not option_text:
        return {'message': 'Missing option text'}, 400


    referendum = Referendums.query.get(id)
    if not referendum:
        return {'message': 'Referendum not found'}, 404


    new_option = ReferendumOptions(
        option=option_text,
        referendum_id=id,
        vote_count=0
    )


    db.session.add(new_option)
    db.session.commit()

    return {'message': 'Option added', 'option_id': new_option.id}, 201



@ec_bp.route('/referendum/<int:id>/status', methods=['PUT'])
def update_referendum_status(id):
    data = request.get_json()
    status = data.get('status')


    if status is None:
        return {'message': 'Missing status field'}, 400


    referendum = Referendums.query.get(id)
    if not referendum:
        return {'message': 'Referendum not found'}, 404


    referendum.status = status
    db.session.commit()

    status_text = 'opened' if status else 'closed'
    return {'message': f'Referendum {status_text}'}, 200



@ec_bp.route('/dashboard/results', methods=['GET'])
def get_results():

    referendums = Referendums.query.all()

    results = []

    for ref in referendums:

        options = ReferendumOptions.query.filter_by(referendum_id=ref.id).all()


        total_votes = sum(opt.vote_count for opt in options)


        options_list = [
            {
                'id': opt.id,
                'text': opt.option,
                'votes': opt.vote_count,
                'percentage': (opt.vote_count / total_votes * 100) if total_votes > 0 else 0
            } for opt in options
        ]


        results.append({
            'referendum_id': ref.id,
            'title': ref.title,
            'description': ref.description,
            'status': 'open' if ref.status else 'closed',
            'total_votes': total_votes,
            'options': options_list
        })

    return {'results': results}, 200


