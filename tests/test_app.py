from http import HTTPStatus

from fast_basic.schemas import UserPublic


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
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    data = {'username': 'bar', 'email': 'foo@email.com', 'password': '123'}
    response = client.put(
        f'/users/{user.id}',
        json=data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    print(response.json())
    assert response.json()['username'] == data['username']


def test_update_user_invalid_id(client, token):
    data = {'username': 'bar', 'email': 'foo@email.com', 'password': '123'}
    response = client.put(
        '/users/2', json=data, headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_integrity_error(client, user, token):
    client.post(
        'users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    response.status_code == HTTPStatus.CONFLICT
    response.json() == {'detail': 'User or email already exists'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/user/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    print(response.json())
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_invalid_id(client, token):
    response = client.delete(
        '/user/2', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
