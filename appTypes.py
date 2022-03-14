from typing import List, Sequence
from dataclasses import dataclass

@dataclass
class ReturnedLyrics:
    '''
    Data type for the songs returned whose lyrics matches the keyword
    '''
    name: str
    lyrics: str
    snippets: Sequence[str]
    keywords: Sequence[str]
    