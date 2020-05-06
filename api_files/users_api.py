import flask
from flask import jsonify, request

from data import db_session
from data.jobs import Jobs
from data.users import User

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/redact_user/<int:user_id>', methods=['POST'])
def redact_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['id', 'email', 'name', 'surname', 'about', 'age',
                  'position', 'speciality', 'address', 'hashed_password']):
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    may_b = session.query(User).filter(User.id == request.json['id']).first()
    if may_b:
        return jsonify({'error': 'Id already exists'})
    may_b = session.query(User).filter(User.id == user_id).first()
    if may_b:
        may_b.id = request.json['id']
        may_b.email = request.json['email']
        may_b.name = request.json['name']
        may_b.surname = request.json['surname']
        may_b.about = request.json['about']
        may_b.age = request.json['age']
        may_b.position = request.json['position']
        may_b.speciality = request.json['speciality']
        may_b.address = request.json['address']
        may_b.hashed_password = request.json['hashed_password']
        session.add(may_b)
        session.commit()
        return jsonify({'success': 'OK'})
    else:
        return jsonify({'error': 'Not found'})


@blueprint.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/all_users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [user.to_dict(only=('id', 'email', 'name', 'surname', 'about', 'age',
                                    'position', 'speciality', 'address', 'hashed_password', 'created_date'))
                 for user in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user':
                user.to_dict(only=('id', 'email', 'name', 'surname', 'about', 'age',
                                   'position', 'speciality', 'address', 'hashed_password', 'created_date'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['id', 'email', 'name', 'surname', 'about', 'age',
                  'position', 'speciality', 'address', 'hashed_password']):

        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    may_b = session.query(User).filter(User.id == request.json['id']).first()
    if may_b:
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        email=request.json['email'],
        name=request.json['name'],
        surname=request.json['surname'],
        about=request.json['about'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        hashed_password=request.json['hashed_password'],
    )
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})
