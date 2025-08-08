from http import HTTPStatus

from fast_basic.schemas import UserPublic


def test_read_users(client, user, token):
    print(user)
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    print(response.json())
    assert response.json() == {
        'users': [{'username': 'foo', 'email': 'foo@email.com', 'id': 1}]
    }


def test_read_users_with_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

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
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
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
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    print(response.json())
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_invalid_id(client, token):
    response = client.delete(
        '/users/2', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
