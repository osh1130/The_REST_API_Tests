import requests
import uuid

ENDPOINT='https://todo.pixegami.io/'

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def new_task_payload():
    user_id = f'test_user_{uuid.uuid4().hex}'
    content = f'contene_{uuid.uuid4().hex}'
    return {
            "content": content,
            "user_id": user_id,
            #"task_id": "string",
            "is_done": False,
        }

def create_task(payload):
    return requests.put(ENDPOINT + '/create-task', json = payload)

def get_task(task_id):
    return requests.get(ENDPOINT+f'/get-task/{task_id}')

def update_task(payload):
    return requests.put(ENDPOINT + '/update-task', json = payload)

def list_tasks(user_id):
    return requests.get(ENDPOINT+f'/list-tasks/{user_id}')

def detete_task(task_id):
    return requests.delete(ENDPOINT+f'/delete-task/{task_id}')

def test_can_create_task():
    #create a task
    #get the task
    #check the detail with the
    payload = new_task_payload()
    response = create_task(payload)
    assert response.status_code == 200
    data = response.json()
    #print(data)

    task_id = data['task']['task_id']
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data['content'] == payload['content']
    assert get_task_data['user_id'] == payload['user_id']



def test_can_update_task():
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']

    # update the task
    new_payload = {
      "user_id": payload['user_id'],
      "task_id": task_id,
      "content": "update_string",
      "is_done": True
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == new_payload['content']
    assert get_task_data['is_done'] == new_payload['is_done']

def test_can_list_tasks():
    #create n tasks
    n = 3
    payload = new_task_payload()
    #task_id is generate by server automatically
    for i in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    #list tasks and check that there are n tasks
    user_id = payload['user_id']
    list_tasks_response = list_tasks(user_id)
    assert list_tasks_response.status_code == 200
    data = list_tasks_response.json()
    tasks = data['tasks']
    assert len(tasks) == n
    #print(data)

def test_can_delete_task():
    #create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200

    #delete the task
    data = create_task_response.json()
    task_id = data['task']['task_id']
    detete_task_response = detete_task(task_id)

    #get the task and check that its not found
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404

