import sqlite3

from app_paths import PLAYER_DB


class PlayerService:
    def __init__(self):
        conn = sqlite3.connect(PLAYER_DB)
        self.conn = conn
        self.cursor = conn.cursor()

    def get_all_players(self):
        query = "SELECT * FROM players"
        players = self.cursor.execute(query).fetchall()
        columns = [column[0] for column in self.cursor.description]
        response = []

        for player in players:
            response.append(dict(zip(columns, player)))

        return response

    def search_by_player(self, player_id):
        query = "SELECT * FROM players WHERE playerId='{}'".format(player_id)
        players = self.cursor.execute(query).fetchall()
        columns = [column[0] for column in self.cursor.description]
        response = []

        for player in players:
            response.append(dict(zip(columns, player)))

        return response
