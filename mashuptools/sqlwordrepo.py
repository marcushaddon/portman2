"""A SQL based implementation of WordRepo."""
from typing import List

import mysql.connector

from wordrepo import WordRepo
from word import Word

class SQLWordRepo(WordRepo):
    """A SQL based implementation of WordRepo."""

    def __init__(self, host: str, db: str, user: str, password: str):
        """Instantiate a SQL Word Repo."""
        self.db = mysql.connector.connect(
            host = host,
            user = user,
            passwd = password,
            database = db,
        )
    
    def get_by_prefix(self, prefix: str) -> List[Word]:
        """Get words that start with a prefix."""
        cursor = self.db.cursor()
        query = f"SELECT * FROM entries WHERE word LIKE '{prefix}%'"
        cursor.execute(query)

        return [Word(result[0], result[1], result[2]) for result in cursor]


"""Driver code."""
if __name__ == "__main__":
    import os
    wr = SQLWordRepo(
        host=os.environ["MYSQL_HOST"],
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        db=os.environ["MYSQL_DB"],
    )

    print(wr.get_by_prefix("ass")[10].definition)