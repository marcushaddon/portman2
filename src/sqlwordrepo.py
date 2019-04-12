"""A SQL based implementation of WordRepo."""
import os
from typing import List, Tuple

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
    
    # TODO: Close connection on disposal!
    # TODO: ignore case when querying!

    @classmethod
    def default(cls):
        """Get default connection."""
        return SQLWordRepo(
            host=os.environ["MYSQL_HOST"],
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            db=os.environ["MYSQL_DB"]
        )
    
    def lookup(self, word: str) -> List[Word]:
        """Look up a word."""
        cursor = self.db.cursor()
        query = f"""
        SELECT * FROM entries
        WHERE word = "{word}"
        """
        cursor.execute(query)

        return [
            Word(res[0], res[1], res[2], res[3], res[4], res[5], res[6])
            for res in cursor
        ]
    
    def get_random_by_prefix(self, prefix: str) -> Word:
        """Get words that start with a prefix."""
        cursor = self.db.cursor()
        length = len(prefix)
        query = f"""
        SELECT * FROM entries
        WHERE word LIKE '{prefix}%'
        AND CHAR_LENGTH(word) > {length}
        ORDER BY RAND() LIMIT 1
        """
        cursor.execute(query)

        result = cursor.fetchone()
        if result == None:
            return result
        
        return Word(result[0], result[1], result[2], result[3], result[4], result[5], result[6])

    def get_random(self) -> Word:
        """Get random word."""
        cursor = self.db.cursor()
        query = f"SELECT * FROM entries ORDER BY RAND() LIMIT 1"
        cursor.execute(query)

        result = cursor.fetchone()

        if result == None:
            return result
        
        return Word(
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5],
            result[6]
        )
    
    def raw_query(self, query: str, fields: Tuple) -> List[Word]:
        """Execute a raw query."""
        cursor = self.db.cursor()
        cursor.execute(query, fields)

        res = [
            Word(res[0], res[1], res[2], res[3], res[4], res[5], res[6])
            for res in cursor
        ]

        return res


"""Driver code."""
if __name__ == "__main__":
    import os
    wr = SQLWordRepo(
        host=os.environ["MYSQL_HOST"],
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        db=os.environ["MYSQL_DB"],
    )

    print(wr.get_random_by_prefix("dog"))
    print(wr.get_random())