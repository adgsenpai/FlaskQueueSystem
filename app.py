from flask import Flask, jsonify
import redis
from rq import Queue
from worker import background_task
from flask import render_template

app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

@app.route('/start_task', methods=['GET'])
def start_task():
    job = q.enqueue(background_task, 42)  # Just using 42 as a sample input
    return jsonify({"message": "Task started!", "job_id": job.id})

@app.route('/task_status/<job_id>', methods=['GET'])
def task_status(job_id):
    job = q.fetch_job(job_id)
    if job:
        print(job.get_status())
        print(job.result)
        print(job.meta.get('progress', 0))
        return jsonify({"status": job.get_status(), "result": job.result, "progress": job.meta.get('progress', 0)})
    else:
        return "No such job!", 404

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
