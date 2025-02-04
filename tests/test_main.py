# tests/test_main.py
def test_home(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert "Placeholder - Might be used for POC demos later." in response.text