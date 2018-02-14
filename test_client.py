from client import response


def test_response():
    assert response({'response': 400, 'error': 'не верный запрос'}) == 'не верный запрос'
    assert response({'response': 200}) == 'OK'
