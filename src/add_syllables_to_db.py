"""Add hypenation info to SQL DB."""
import hyphenate

from sqlwordrepo import SQLWordRepo

LAST_UPDATED_FILE = "./latest_updated.txt"

def add_syllables_to_db():
    """Add hyphenation to db."""
    wr = SQLWordRepo.default()
    # SUCH a hack but I don't care!
    db = wr.db
    read_cursor = db.cursor(buffered=True)
    write_cursor = db.cursor()

    last_updated = 0
    try:
        f = open(LAST_UPDATED_FILE, "r")
        last_updated = int(f.read())
        f.close()
    except:
        pass

    print(f"starting from {last_updated}")

    query = """
    SELECT * FROM `entries` ORDER BY `word` ASC"""

    if last_updated > 0:
        query += f" LIMIT 180000 OFFSET {last_updated}"
    
    query += ";"
    
    try:
        read_cursor.execute(query)
    except:
        print(query)
    seen = {}
    
    while True:
        row = read_cursor.fetchone()
        if row is None:
            break
        
        word = row[0]

        if word in seen:
            continue

        parts = hyphenate.hyphenate_word(word)

        second_to_last = None
        last = None
        first = None
        second = None

        if len(parts) == 1:
            second_to_last = parts[0]
            last = parts[0]
            first = parts[0]
            second = parts[0]
        else:
            second_to_last = parts[-2]
            last = parts[-1]
            first = parts[0]
            second = parts[1]
        
        query = """
        UPDATE entries
        SET
        second_to_last_syllable = %s,
        last_syllable = %s,
        first_syllable = %s,
        second_syllable = %s
        WHERE word = %s 
        """


        write_cursor.execute(query, (second_to_last, last, first, second, word))
        seen[word] = True
        last_updated += 1
        
        if last_updated % 100 == 0:
            print(f"Progress: {last_updated}")
            with open(LAST_UPDATED_FILE, "w") as outf:
                outf.write(str(last_updated))

if __name__ == "__main__":
    add_syllables_to_db()
