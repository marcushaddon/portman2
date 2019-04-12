"""Tools for mashing up text."""
from typing import Dict, List, Tuple
from collections import defaultdict

from textblob import TextBlob

from sqlwordrepo import SQLWordRepo

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

# Second choice
def branch_on_pos(aye: str, bee: str, pos: str) -> str:
    """Graft on a POS."""
    atagged = TextBlob(a).pos_tags
    btagged = TextBlob(b).pos_tags

    awords = [tag[0] for tag in atagged]
    bwords = [tag[0] for tag in btagged]
    atags = [tag[1] for tag in atagged]
    btags = [tag[1] for tag in btagged]

    if not pos in atags or not pos in btags:
        return (None, -1)

    leading_cutoff = -1
    aposindex, bposindex = atags.index(pos), btags.index(pos)
    if aposindex > bposindex:
        leading_cutoff = aposindex
        composite = awords[:aposindex] + ["BREAK"] + bwords[bposindex:]
        pass
    else:
        leading_cutoff = bposindex
        composite = bwords[:bposindex] + ["BREAK"] + awords[aposindex:]
        pass


    return (' '.join(composite), leading_cutoff)




if __name__ == "__main__":
    wr = SQLWordRepo.default()
    a = wr.get_random().definition
    b = wr.get_random().definition

    print(f"""
    {a} 
    +
    {b}
    =
    """)
    print(branch_on_pos(a, b, 'IN'))