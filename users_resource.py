from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('email', required=True)
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('about', required=True)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('hashed_password', required=True)
parser.add_argument('city_from', required=True)
parser.add_argument('age', required=True, type=int)

def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")

class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'email', 'name', 'surname', 'about', 'age',
                'position', 'speciality', 'address', 'hashed_password', 'created_date', 'city_from'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self, user_id):
        abort_if_user_not_found(user_id)
        args = parser.parse_args()
        session = db_session.create_session()
        if args['id'] <= 0:
            abort(404, message=f"Id must be > 0")
        may_b = session.query(User).filter(User.id == args['id']).first()
        if may_b and args['id'] != user_id:
            abort(404, message=f"User with id {args['id']} already exist")
        user = session.query(User).get(user_id)
        user.id=args['id']
        user.email=args['email']
        user.name=args['name']
        user.surname=args['surname']
        user.about=args['about']
        user.age=args['age']
        user.position=args['position']
        user.speciality=args['speciality']
        user.address=args['address']
        user.hashed_password=args['hashed_password']
        user.city_from=args['city_from']
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'email', 'name', 'surname', 'about', 'age',
                'position', 'speciality', 'address', 'hashed_password', 'created_date', 'city_from'))
            for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if args['id'] <= 0:
            abort(404, message=f"Id must be > 0")
        may_b = session.query(User).filter(User.id == args['id']).first()
        if may_b:
            abort(404, message=f"User with id {args['id']} already exist")
        user = User(
            id=args['id'],
            email=args['email'],
            name=args['name'],
            surname=args['surname'],
            about=args['about'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            hashed_password=args['hashed_password'],
            city_from=args['city_from']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})