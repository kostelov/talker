from client import response
import time

message = {
    "action": "presence",
    "time": time.time(),
    "type": "status",
    "user": {
        "account_name": "name",
        "status": "В сети"
    }
}

msg = {
    "action": "presence",
    "time": time.time(),
    "type": "status",
    "user": {
        "account_name": "name",
        "status": "Занят"
    }
}

def test_response():
    assert response({'response': 400, 'error': 'не верный запрос'}) == 'не верный запрос'
    assert response({'response': 200, 'message': message['user']['status']}) == 'В сети'
    assert response({'response': 200, 'message': msg['user']['status']}) == 'Занят'
