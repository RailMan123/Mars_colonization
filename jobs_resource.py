from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.jobs import Jobs

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True, type=bool)

def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")

class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                    'start_date', 'end_date', 'is_finished', 'user.name'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self, job_id):
        abort_if_job_not_found(job_id)
        args = parser.parse_args()
        session = db_session.create_session()
        if args['id'] <= 0:
            abort(404, message=f"Id must be > 0")
        may_b = session.query(Jobs).filter(Jobs.id == args['id']).first()
        if may_b and args['id'] != job_id:
            abort(404, message=f"Job with id {args['id']} already exist")
        job = session.query(Jobs).get(job_id)
        job.id = args['id']
        job.team_leader = args['team_leader']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        job.is_finished = args['is_finished']
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})

class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                    'start_date', 'end_date', 'is_finished', 'user.name'))
            for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if args['id'] <= 0:
            abort(404, message=f"Id must be > 0")
        may_b = session.query(Jobs).filter(Jobs.id == args['id']).first()
        if may_b:
            abort(404, message=f"Job with id {args['id']} already exist")
        job = Jobs(
            id=args['id'],
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})