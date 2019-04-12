"""Module for creating portmanteaus."""
from word import Word
from sqlwordrepo import SQLWordRepo
from choose_mate import similar_pronounciation, overlapping_last_syllable, compatible_sounds
from mashup_words import combine_with_overlap
from mashup_definitions import pos_swap, pos_swaps, np_swap
from pos import poss

class Portmanteau(object):
    """Represents a portmanteau."""

    def __init__(self, a, b, p):
        """Initialize a portmanteau."""
        self.word_a = a
        self.word_b = b
        self.portmanteau = p

def create_portmanteau() -> Portmanteau:
    """Create a portmanteau."""
    wr = SQLWordRepo.default()
    a = wr.get_random()

    b = overlapping_last_syllable(a.syllables)

    new_word, _ = combine_with_overlap(a.word.lower(), b.word.lower())

    print(f"{a.word} + {b.word} = {new_word}")

    score, new_def_a, new_def_b = pos_swaps(a.definition, b.definition, poss)
    print(f"""
        {a.definition}

        +

        {b.definition}

        = 

        {new_def_a}

        {new_def_b}
""")


    return new_word
    

if __name__ == '__main__':
    res = create_portmanteau()
    print(res)