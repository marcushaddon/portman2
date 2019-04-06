"""Module for combining two words."""
from typing import Tuple

def find_overlapping_letters(a: str, b: str) -> str:
    """Find overlapping letters at end of a, beginning of b."""
    best = ""
    for i in range(len(a) - 1, -1, -1):
        substr = a[i:]
        if b.find(substr) == 0 and len(substr) > len(best):
            best = substr
    
    return best


def combine_with_overlap(a: str, b: str) -> Tuple[str, int]:
    """Combine using exact matching overlap and indicate length of overlap."""
    overlap = find_overlapping_letters(a, b)

    return (
        f"{a}{b.replace(overlap, '')}",
        len(overlap)
    )


# Driver code.
if __name__ == "__main__":
    print(find_overlapping_letters("marcus", "customer")) # -> cus
    print ("marcus + customarily = ")
    print(combine_with_overlap("marcus", "custumarily"))