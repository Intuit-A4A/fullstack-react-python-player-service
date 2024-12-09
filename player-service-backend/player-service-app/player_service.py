import sqlite3
from sqlalchemy import create_engine
from typing import List, Optional
from datetime import date

# Type annotations to handle validation, conversion, and parsing
from pydantic import BaseModel


class Player(BaseModel):
    playerId: str
    birthYear: float
    birthMonth: float
    birthDay: float
    birthCountry: str
    birthState: Optional[str]
    birthCity: str
    deathYear: Optional[float]
    deathMonth: Optional[float]
    deathDay: Optional[float]
    deathCountry: Optional[str]
    deathState: Optional[str]
    deathCity: Optional[str]
    nameFirst: str
    nameLast: str
    nameGiven: str
    weight: float
    height: float
    bats: str  # 'R', 'L' or switch hitter
    throws: str  # 'R' or 'L'
    debut: date
    finalGame: date
    retroID: str
    bbrefID: str

    def to_dict(self) -> dict:
        res = self.model_dump()
        res["debut"] = res["debut"].isoformat()
        res["finalGame"] = res["finalGame"].isoformat()

        return res


class Pagination(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int


class PlayerResponse(BaseModel):
    players: List[Player]
    pagination: Pagination


class PlayerService:
    def __init__(self):
        conn = sqlite3.connect("player.db")
        self.conn = conn
        self.cursor = conn.cursor()

    def get_all_players(self, page=1, per_page=10) -> PlayerResponse:
        # Validate types
        try:
            page = int(page)
            per_page = int(per_page)
        except (TypeError, ValueError):
            raise ValueError("page and per_page must be valid numbers")

        # Validate ranges
        if page < 1:
            raise ValueError("page must be greater than 0")
        if per_page < 1:
            raise ValueError("per_page must be greater than 0")
        if per_page > 100:
            raise ValueError("per_page cannot exceed 100")

        offset = (page - 1) * per_page
        query = f"SELECT * FROM players LIMIT {per_page} OFFSET {offset}"
        players = self.cursor.execute(query).fetchall()

        columns = [column[0] for column in self.cursor.description]
        # zip: pairs - column name -> value ('birthYear' -> 1987)
        # dict: {'birthYear': 1987}
        # ** unpacks the dictionary as keyword arguments
        player_list = [Player(**dict(zip(columns, player))) for player in players]

        total_count = self.cursor.execute("SELECT COUNT(*) FROM players").fetchone()[0]

        return PlayerResponse(
            players=player_list,
            pagination=Pagination(
                total=total_count,
                page=page,
                per_page=per_page,
                total_pages=total_count // per_page
                + (1 if total_count % per_page else 0),
            ),
        )

    def search_by_player(self, player_id):
        query = f"SELECT * FROM players WHERE playerId='{player_id}'"
        players = self.cursor.execute(query).fetchall()
        columns = [column[0] for column in self.cursor.description]
        response = []

        for player in players:
            response.append(dict(zip(columns, player)))

        return response
