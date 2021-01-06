import sqlite3
from sqlite3 import Error
import os

class DB:
    def __init__(self, path):
        self.path = path
        self.conn = None

    def create_db(self):
        """ create a database connection to a SQLite database

        https://www.sqlitetutorial.net/sqlite-python/creating-database/
        """

        if os.path.exists(self.path):
            conn = None
            try:
                conn = sqlite3.connect(self.path)
                print(f'Created {self.path} as sqlite3 version {sqlite3.version}')
                success = True
            except Error as e:
                print(e)
                success = False
            finally:
                if conn:
                    conn.close()
                    self.conn = None
                return success

        return True

    def connect(self):
        self.conn = sqlite3.connect(self.path)

    def commit(self):
        self.conn.commit()

    def execute(self, *args):
        if not self.conn:
            self.connect()
        self.conn.execute(*args)
        self.commit()

    def executemany(self, *args):
        if not self.conn:
            self.connect()
        self.conn.execute(*args)
        self.commit()

    def close(self):
        if self.conn:
            self.commit()
            self.conn.close()
            self.conn = None