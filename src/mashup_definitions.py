"""Tools for mashing up text."""
from typing import Dict, List, Tuple
from collections import defaultdict

from textblob import TextBlob

# THIS SUCKS
def dereassemble(aye: str, bee: str) -> str:
    """De assemble then re assemble."""
    a, b = TextBlob(aye), TextBlob(bee)
    apos, bpos = a.pos_tags, b.pos_tags
    
    aparts = defaultdict(lambda: [])
    bparts = defaultdict(lambda: [])

    for p in apos:
        aparts[p[1]].append(p[0])
    for p in bpos:
        bparts[p[1]].append(p[0])

    amash = []
    for p in apos:
        pos = p[1]
        if len(bparts[pos]) >= 1:
            amash.append(bparts[pos].pop())
        else:
            amash.append(aparts[pos].pop())
    
    bmash = []
    for p in bpos:
        pos = p[1]
        if len(aparts[pos]) >= 1:
            bmash.append(aparts[pos].pop())
        else:
            bmash.append(bparts[pos].pop())
    


    return " ".join(bmash)

# Pretty good!
def np_swap(aye: str, bee: str) -> Tuple[str, str]:
    """Swap every other noun phrase."""
    a, b = TextBlob(aye), TextBlob(bee)
    a_nps, b_nps = a.noun_phrases, b.noun_phrases

    i = 0
    while i < len(a_nps) and i < len(b_nps):
        if i % 2 != 0:
            anp, bnp = a_nps[i], b_nps[i]
            a = a.replace(anp, bnp)
            b = b.replace(bnp, anp)
        i += 1

    return (a.raw, b.raw)

# Really good!
def pos_swap(aye: str, bee: str, pos: str) -> Tuple[int, str, str]:
    """Swap a given part of speech."""
    # TODO: Replace instances of subword in own definition.
    swaps = 0
    a, b = TextBlob(aye), TextBlob(bee)
    apos, bpos = a.pos_tags, b.pos_tags
    aps = [p for p in apos if p[1] == pos]
    bps = [p for p in bpos if p[1] == pos]

    for i in range(min([len(aps), len(bps)])):

        ap = aps[i][0]
        bp = bps[i][0]
        a = a.replace(ap, bp)
        b = b.replace(bp, ap)
        swaps += 1


    return (swaps, a.raw, b.raw)

def pos_swaps(a: str, b: str, poses: List[str]) -> Tuple[int, str, str]:
    total_swaps = 0
    for pos in poses:
        swaps, a, b = pos_swap(a, b, pos)
        total_swaps += swaps
    
    return (total_swaps, a, b)

# def choose_pos(aye: str, bee: str) -> str:


if __name__ == "__main__":
    a = "Any one of numerous species of elasmobranch fishes of the order Plagiostomi, found in all seas."
    b = "The place in which public records or historic documents are kept."

    c = "A pointed missile weapon, intended to be thrown by the hand; a short lance; a javelin; hence, any sharp-pointed missile weapon, as an arrow."
    d = "The utterance of the elementary sounds of a language by the appropriate movements of the organs, as in pronunciation; as, a distinct articulation."

    swaps, e, f = pos_swaps(a, b, ["NNS"])
    print(swaps)
    print(e)
    print(f)