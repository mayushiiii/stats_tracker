import os
import json
from app import webserver
from flask import request, jsonify



# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}
        # Sending back a JSON response
        return jsonify(response)
    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405

# request de get. se cauta in results daca s a terminat jobul si
# daca da, returnam rezultatul(continutul fisierului),
# altfel este considerat ca fiind running inca (asteptam rezultatul)
@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    # Check if job_id is valid
    if int(job_id) - 1 > webserver.job_counter:
        print(f"Invalid job ID {job_id}")
        return jsonify({"status": "Invalid job ID"})
    # Check if job_id is done and return the result
    #    res = res_for(job_id)
    #    return jsonify({
    #        'status': 'done',
    #        'data': res
    #    })
    if os.path.exists(f"results/{job_id}.json"):
        with open(f"results/{job_id}.json", "r", encoding="utf-8") as f:
            res = json.load(f)
            return jsonify({
                'status': 'done',
                'data': res
            })
    # If not, return running status
    #print(f"Returning running status")
    return jsonify({'status': 'running'})

# toate posturile opereaza la fel:
# incrementam job_counter (inainte de adaugarea in q)
# pt ca o daca o fac dupa, are loc o discrepanta si nu
# poate gasi fisierul cu id_ul dorit (va sari pe primul mereu)
# adaugam in in queue sub forma unui tuplu deoarece am mai multe
# informatii relevante aici (job_counter, intrebarea si tipul de request)
@webserver.route('/api/states_mean', methods=['POST'])
# states mean = media pe fiecare stat, sortata crescator
def states_mean_request():
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.job_queue.put((data, webserver.job_counter, "states_mean"))
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/state_mean', methods=['POST'])
# state mean = media pe un singur stat
def state_mean_request():
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.job_queue.put((data, webserver.job_counter, "state_mean"))
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/best5', methods=['POST'])
# best5 = top 5 state uri in functie de medie (si intrebare teoretic)
def best5_request():
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.job_queue.put((data, webserver.job_counter, "best5"))
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/worst5', methods=['POST'])
# la fel ca mai sus dar invers
def worst5_request():
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.job_queue.put((data, webserver.job_counter, "worst5"))
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/global_mean', methods=['POST'])
# global mean = media TUTUROR
def global_mean_request():
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.job_queue.put((data, webserver.job_counter, "global_mean"))
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/diff_from_mean', methods=['POST'])
# diff from mean = diferenta dintre media globala si media pe fiecare stat
def diff_from_mean_request():
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.job_queue.put((data, webserver.job_counter, "diff_from_mean"))
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
# idem dar cu media acelui stat
def state_diff_from_mean_request():
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.job_queue.put((data, webserver.job_counter, "state_diff_from_mean"))
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/mean_by_category', methods=['POST'])
# mean by category = media pt stratification
def mean_by_category_request():
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.job_queue.put((data, webserver.job_counter, "mean_by_category"))
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
# idem doar ca cu statul dat. acum ca o zic asa puteam face mai eficient. dar aia e
def state_mean_by_category_request():
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.job_queue.put((data, webserver.job_counter, "state_mean_by_category"))
    return jsonify({"job_id": webserver.job_counter})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes

@webserver.route('/api/jobs', methods=['GET'])
# caut toate fisierele ca sa stiu care joburi sunt facute si ce status au.
def get_jobs():
    jobs = []
    for job_id in range(1, webserver.job_counter):
        status = "running"
        if os.path.exists(f"results/{job_id}.json"):
            status = "done"
        jobs.append({f"job_id_{job_id}": status})
    return jsonify({"status": "done", "data": jobs})
# caut care inca au status running
@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    num_jobs = 0;
    for job_id in range(1, webserver.job_counter):
        if (get_response(job_id) == jsonify({'status': 'running'})):
            num_jobs +=1;
    return jsonify({"status": "done", "data": num_jobs})
# dau parametrul in tasks_runner si astept sa se termine
@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    webserver.tasks_runner.graceful_shutdown.set()
    return jsonify({"status": "done"})