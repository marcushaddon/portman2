"""Exercise to find best way to mash up definitions."""
import random
from textblob import TextBlob

from sqlwordrepo import SQLWordRepo

wr = SQLWordRepo.default()

words = [
    wr.get_random()
    for _ in range(10)
]

with open("worksheet.txt", "w") as worksheet:
    for _ in range(10):
        a = random.choice(words)
        b = random.choice(words)
        atoks = TextBlob(a.definition).pos_tags
        btoks = TextBlob(b.definition).pos_tags

        worksheet.write(f"""
{_ + 1}.
{atoks}

+ 

{btoks}

=

-----------------------------------------------






----------------------------------------------


""")