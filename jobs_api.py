import flask
from flask import jsonify, request

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/redact_job/<int:job_id>', methods=['POST', 'GET'])
def redact_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    may_b = session.query(Jobs).filter(Jobs.id == job_id).first()
    if may_b:
        may_b.id = request.json['id']
        may_b.team_leader = request.json['team_leader']
        may_b.job = request.json['job']
        may_b.work_size = request.json['work_size']
        may_b.collaborators = request.json['collaborators']
        may_b.is_finished = request.json['is_finished']
        session.add(may_b)
        session.commit()
        return jsonify({'success': 'OK'})
    else:
        return jsonify({'error': 'Not found'})


@blueprint.route('/api/delete_job/<int:job_id>', methods=['DELETE', 'GET'])
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})




@blueprint.route('/api/all_jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                    'start_date', 'end_date', 'is_finished', 'user.name'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job':
                job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                  'start_date', 'end_date', 'is_finished', 'user.name'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    may_b = session.query(Jobs).filter(Jobs.id == request.json['id']).first()
    if may_b:
        return jsonify({'error': 'Id already exists'})

    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})
