import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_players_returns_data(client):
    response = client.get("/v1/players")
    assert response.status_code == 200
    data = response.get_json()
    assert "players" in data
    assert isinstance(data["players"], list)
    assert len(data["players"]) > 0
    assert "playerId" in data["players"][0]
