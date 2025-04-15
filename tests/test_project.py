import pytest
from app import create_app, db
from app.models.project import Project
from datetime import date

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_project(client):
    response = client.post('/api/v1/projects', json={
        'name': 'Test Project',
        'description': 'Test Description',
        'start_date': date.today().isoformat(),
        'status': 'Not Started'
    })
    
    assert response.status_code == 201
    assert response.json['name'] == 'Test Project'
    assert response.json['status'] == 'Not Started'
