import pytest
from app import app, db, Client

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_add_client(client):
    response = client.post('/add_client', data={
        'document': '1234567890',
        'surname': 'Doe',
        'first_name': 'John',
        'patronymic': 'Smith',
        'birthday': '2000-01-01'
    }, follow_redirects=True)

    assert b'Doe John Smith' in response.data
    assert b'2000-01-01' in response.data
    assert Client.query.count() == 1

    # Добавляем клиента снова
    response = client.post('/add_client', data={
        'document': '1234567891',
        'surname': 'Johnson',
        'first_name': 'Alice',
        'patronymic': 'Doe',
        'birthday': '1995-05-05'
    }, follow_redirects=True)

    assert b'Johnson Alice Doe' in response.data
    assert b'1995-05-05' in response.data
    assert Client.query.count() == 2

def test_delete_client(client):
    # Добавим клиента
    client.post('/add_client', data={
        'document': '1234567890',
        'surname': 'Doe',
        'first_name': 'John',
        'patronymic': 'Smith',
        'birthday': '2000-01-01'
    }, follow_redirects=True)

    assert Client.query.count() == 1

    # Получим ID добавленного клиента
    client_id = Client.query.first().id

    # Удалим клиента
    client.post(f'/delete_client/{client_id}', follow_redirects=True)

    # После удаления клиента перезагрузим страницу
    response = client.get('/', follow_redirects=True)

    assert b'Doe John Smith' not in response.data
    assert b'2000-01-01' not in response.data
    assert Client.query.count() == 0
