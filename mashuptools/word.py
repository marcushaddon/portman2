"""A class for representing a dictionary entry."""

class Word(object):
    """A word with a definition and part of speech."""

    def __init__(self, word: str, pos: str, definition: str):
        """Instantiate a Word."""
        self.word = word
        self.pos = pos
        self.definition = definition
    
    def __repr__(self):
        """Represent instance."""
        definition = self.definition.replace('\n', "")

        return f"""
Word: {self.word}
POS: {self.pos}
Definition: {definition}
"""
