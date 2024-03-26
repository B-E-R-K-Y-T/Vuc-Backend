from typing import Optional

import psycopg2

from config import app_settings


class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=app_settings.POSTGRES_DB,
            user=app_settings.POSTGRES_USER,
            password=app_settings.POSTGRES_PASSWORD,
            host=app_settings.POSTGRES_HOST,
            port=app_settings.POSTGRES_PORT
        )
        self.cur = self.conn.cursor()

    def execute(self, query: str, vars: Optional[tuple] = None):
        self.cur.execute(query, vars)

        return self

    def fetch_all(self) -> list[tuple]:
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

    def __del__(self):
        self.close()


class DatabaseWorker:
    def __init__(self):
        self.manager = DatabaseManager()

    def get_current_day_of_week_users_id(self, day_number: int) -> list:
        query = "SELECT id FROM users WHERE users.platoon_number - %s * 100 < 99;"
        self.manager.execute(query, (day_number,))

        users_id: list[tuple] = self.manager.fetch_all()
        res = []

        for user_id in users_id:
            if user_id:
                res.append(user_id[0])

        return res

    def set_attend(self, user_id: int):
        stmt = """ 
            INSERT INTO attend (user_id, date_v, visiting, semester, confirmed)
            SELECT %s, DATE(now()), 2, 1, false
            WHERE NOT EXISTS (
                SELECT 1
                FROM attend
                WHERE date_v = DATE(now()) AND user_id = %s
            );
"""
        vars = (user_id, user_id)

        self.manager.execute(stmt, vars)
        self.manager.commit()
