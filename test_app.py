from app import create_app


def test_home_page_loads():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Bonnyrigg Pizza Blog' in response.data


def test_recipes_page_loads():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.get('/recipes')
    assert response.status_code == 200
    assert b'Recipe Search & Filter' in response.data
