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
