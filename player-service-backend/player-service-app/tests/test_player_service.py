import pytest
import sqlite3
import pandas as pd
from datetime import date
from player_service import PlayerService
from player_service import Player
from app import TABLE_NAME_PLAYERS

mock_players = [
    Player(
        playerId="aardsda01",
        birthYear=1981,
        birthMonth=12,
        birthDay=27,
        birthCountry="USA",
        birthState="CO",
        birthCity="Denver",
        deathYear=None,
        deathMonth=None,
        deathDay=None,
        deathCountry=None,
        deathState=None,
        deathCity=None,
        nameFirst="David",
        nameLast="Aardsma",
        nameGiven="David Allan",
        weight=215,
        height=75,
        bats="R",
        throws="R",
        debut=date(2004, 4, 6),
        finalGame=date(2015, 8, 23),
        retroID="aardd001",
        bbrefID="aardsda01",
    ),
    Player(
        playerId="aaronha01",
        birthYear=1934,
        birthMonth=2,
        birthDay=5,
        birthCountry="USA",
        birthState="AL",
        birthCity="Mobile",
        deathYear=None,
        deathMonth=None,
        deathDay=None,
        deathCountry=None,
        deathState=None,
        deathCity=None,
        nameFirst="Hank",
        nameLast="Aaron",
        nameGiven="Henry Louis",
        weight=180,
        height=72,
        bats="R",
        throws="R",
        debut=date(1954, 4, 13),
        finalGame=date(1976, 10, 3),
        retroID="aaroh101",
        bbrefID="aaronha01",
    ),
]


@pytest.fixture
def mock_db():
    # Read schema from CSV (just get headers)
    df = pd.read_csv(
        "Player.csv",
        nrows=0,
    )
    conn = sqlite3.connect(":memory:")

    # Create table with same schema as CSV
    df.to_sql(TABLE_NAME_PLAYERS, conn, index=False, if_exists="replace")

    cursor = conn.cursor()
    for player in mock_players:
        player_dict = player.to_dict()
        placeholders = ",".join(["?"] * len(player_dict))
        insert_query = f"INSERT INTO {TABLE_NAME_PLAYERS} VALUES ({placeholders})"
        cursor.execute(insert_query, tuple(player_dict.values()))

    conn.commit()
    return conn


@pytest.fixture
def player_service(monkeypatch, mock_db):
    def mock_connect(*args, **kwargs):
        return mock_db

    monkeypatch.setattr("sqlite3.connect", mock_connect)
    return PlayerService()


def test_get_all_players(player_service):
    response = player_service.get_all_players()
    assert len(response.players) == len(mock_players)
    assert response.players[0].playerId == mock_players[0].playerId
    assert response.players[1].playerId == mock_players[1].playerId


def test_get_all_players_pagination(player_service):
    response = player_service.get_all_players(page=2, per_page=1)
    assert len(response.players) == 1
    assert response.players[0].playerId == mock_players[1].playerId
    assert response.pagination.total == 2
    assert response.pagination.total_pages == 2


def test_search_by_player(player_service):
    player = player_service.search_by_player(mock_players[0].playerId)
    assert len(player) == 1
    assert player[0]["nameFirst"] == mock_players[0].nameFirst
