import pytest
import sqlite3
from player_service import PlayerService
from .data.players import TABLE_NAME, SCHEMA, TEST_DATA  # Import specific items


@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(SCHEMA)

    for player in TEST_DATA:
        placeholders = ",".join(["?"] * len(player))
        insert_query = f"INSERT INTO {TABLE_NAME} VALUES ({placeholders})"
        cursor.execute(insert_query, tuple(player.values()))

    conn.commit()
    return conn


@pytest.fixture
def player_service(monkeypatch, mock_db):
    def mock_connect(*args, **kwargs):
        return mock_db

    monkeypatch.setattr("sqlite3.connect", mock_connect)
    return PlayerService()


def test_get_all_players(player_service):
    players = player_service.get_all_players()
    assert len(players) == len(TEST_DATA)  # Cleaner reference
    assert players[0]["playerId"] == TEST_DATA[0]["playerId"]  # Cleaner reference


def test_search_by_player(player_service):
    player = player_service.search_by_player(
        TEST_DATA[0]["playerId"]
    )  # Cleaner reference
    assert len(player) == 1
    assert player[0]["nameFirst"] == TEST_DATA[0]["nameFirst"]
