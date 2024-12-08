TABLE_NAME = "players"

SCHEMA = f"""
    CREATE TABLE {TABLE_NAME} (
        playerId TEXT,
        nameFirst TEXT,
        nameLast TEXT,
        birthYear INTEGER,
        birthMonth INTEGER,
        birthDay INTEGER
    )
"""

TEST_DATA = [
    {
        "playerId": "aaronha01",
        "nameFirst": "Hank",
        "nameLast": "Aaron",
        "birthYear": 1934,
        "birthMonth": 2,
        "birthDay": 5,
    },
    {
        "playerId": "aardsda01",
        "nameFirst": "David",
        "nameLast": "Aardsma",
        "birthYear": 1981,
        "birthMonth": 12,
        "birthDay": 27,
    },
]
