"""A class for representing a dictionary entry."""
import hyphenate

class Word(object):
    """A word with a definition and part of speech."""

    def __init__(
        self, word: str = None,
        pos: str = None,
        definition: str = None,
        first_syllable: str = None,
        second_syllable: str = None,
        second_to_last_syllable: str = None,
        last_syllable: str = None,
    ):
        """Instantiate a Word."""
        self.word = word
        self.pos = pos
        self.definition = definition
        self.second_to_last_syllable = second_to_last_syllable
        self.last_syllable = last_syllable
        self.first_syllable = first_syllable
        self.second_syllable = second_syllable
    
    @property
    def syllables(self):
        return hyphenate.hyphenate_word(self.word)

    
    def __repr__(self):
        """Represent instance."""
        definition = self.definition.replace('\n', "")

        return f"""
Word: {self.word}
POS: {self.pos}
Definition: {definition}
Relevant Syllables: {"-".join([
    self.first_syllable,
    self.second_syllable,
    self.second_to_last_syllable,
    self.last_syllable,
])}
"""
