from flask import Blueprint, request
from models import db, Referendums, ReferendumOptions

api_bp = Blueprint('api', __name__, url_prefix='/mslr')


#endpoint 1 get by status
@api_bp.route('/referendums', methods=['GET'])
def get_referendums_open():
    if request.method == 'GET':
        referendum_status = request.args.get('status')
        if referendum_status == 'open':
            referendums = Referendums.query.filter_by(status=True).all()
        elif referendum_status == 'closed':
            referendums = Referendums.query.filter_by(status=False).all()
        else:
            return {'message': 'Referendum not found'}, 404

        response = []
        for ref in referendums:
            options = ReferendumOptions.query.filter_by(referendum_id=ref.id).all()

            options_list = [
                {'id': opt.id, 'text': opt.option, 'votes': opt.vote_count}
                for opt in options
            ]

            response.append({
                'referendum_id': ref.id,
                'title': ref.title,
                'description': ref.description,
                'status': 'open' if ref.status else 'closed',
                'options': options_list
            })

        return {'referendums': response}, 200

#endpoint 2 get by id
@api_bp.route('/referendums/<id>', methods=['GET'])
def get_referendum(id):
    if request.method == 'GET':
        referendum = Referendums.query.get(id)
        if not referendum:
            return {'message': 'Referendum not found'}, 404

        options = ReferendumOptions.query.filter_by(referendum_id=id).all()

        options_list = [
            {'id': opt.id, 'text': opt.option, 'votes': opt.vote_count}
            for opt in options
        ]

        return {
            'referendum_id': referendum.id,
            'title': referendum.title,
            'description': referendum.description,
            'status': 'open' if referendum.status else 'closed',
            'options': options_list
        }, 200

