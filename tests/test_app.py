from http import HTTPStatus


def test_read_root_shold_return_ok_and_ola_mundo(client):
    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert (verificação)
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert (verificação)


def test_ola_mundo_should_return_html(client):
    response = client.get('/ola-mundo')

    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert '<h1>Ol\xe1 Mundo!</h1>' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={'username': 'foo', 'email': 'foo@email.com', 'password': 'bar'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'foo@email.com',
        'username': 'foo',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'email': 'foo@email.com',
                'username': 'foo',
            },
        ]
    }


def test_update_user(client):
    data = {'username': 'bar', 'email': 'foo@email.com', 'password': '123'}
    response = client.put('/users/1', json=data)

    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == 'bar'


def test_update_user_invalid_id(client):
    data = {'username': 'bar', 'email': 'foo@email.com', 'password': '123'}
    response = client.put('/users/2', json=data)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/user/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bar',
        'email': 'foo@email.com',
        'id': 1,
    }


def test_delete_user_invalid_id(client):
    response = client.delete('/user/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
