"""Module for creating portmanteaus."""

"""
IDEAS:
1. Index the second part of each word when hypenated
and whether it starts with a consonant or a vowel, look
up words with complementary second part (consonant -> vowel,
vowel -> consonant).
2. Index first part of word when hyphenated, look up words with
first part matching last part.
3. Index first phoneme, look up words with first phonemes compatible
with last phoneme and then just smoosh them together.

TODO: Break out mashup word functionality from mate selection
functionality.
TODO: Inject SQLWordrepo
"""

import re
import random
from typing import List

import hyphenate
import pronouncing

from sqlwordrepo import SQLWordRepo
from word import Word


def overlapping_last_syllable(syllables: List[str]) -> Word:
    """Create portmanteau for given word."""
    wr = SQLWordRepo.default()

    end = syllables[-1]
    mate = wr.get_random_by_prefix(end)

    return mate

def _similiar_pronounciation(word: str) -> List[str]:
    """Find possible mates using pronunciation search."""
    mates = []
    first_phones = pronouncing.phones_for_word(word)[0]
    phones = first_phones.split(" ")
    i = 0
    while not mates and i < len(phones):
        # TODO: Generalize consonant sounds
        search_pattern = f"^{' '.join(phones[i:])}"
        matches = pronouncing.search(search_pattern)
        distinct_matches = [match for match in matches if match.find(word) < 0]

        if len(distinct_matches) > 0:
            mates = distinct_matches
        else:
            i += 1
        
    return mates

def similar_pronounciation(word: str) -> Word:
    """Use pronunciation search."""
    # NOTE: This can sometimes fail due to pronouncing
    # containing words not in our SQL db, and needs to
    # be tried in a try/catch loop. Actually this whole
    # project has several points of non deterministic 
    # branching behavior so... TODO: refactor each method
    # to return all results so random choices can be 
    # made by a higher level process.
    possible_mates = _similiar_pronounciation(word)

    looked_up = None
    wr = SQLWordRepo.default()
    mates_table = {
        mate: True for mate in possible_mates
    }
    while not looked_up and mates_table:
        possible = random.choice(list(mates_table.keys()))
        results = wr.lookup(possible)
        if len(results) > 0:
            looked_up = results
            break
        del mates_table[possible]
    
    if not looked_up:
        raise Exception("Bad luck this time")
    
    def_lengths = [len(w.definition) for w in looked_up]
    longest = max(def_lengths)
    index = def_lengths.index(longest)
    
    return results[index]



"""Driver code."""
if __name__ == "__main__":
    s = hyphenate.hyphenate_word("aspirated")
    print(overlapping_last_syllable(s))