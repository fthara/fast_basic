from dataclasses import asdict

from sqlalchemy import select

from fast_basic.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='test', email='test@test.com', password='test'
        )

        session.add(new_user)
        session.commit()

        user = session.scalar(
            select(User).where(User.username == new_user.username)
        )

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
        'password': 'test',
        'created_at': time,
    }
