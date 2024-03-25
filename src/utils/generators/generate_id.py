import random
from typing import Optional

from src.data.constants import ENG_RANDOM_CHARS, NUMBERS
from src.enums import IDTagEnum


def generate_id(
        tag: IDTagEnum | str = '',
        length: int = 15,
        characters: Optional[str] = ENG_RANDOM_CHARS,
        numbers: Optional[str] = NUMBERS,
        sep: str = '_'
) -> str:
    if not characters and not numbers:
        raise ValueError('It is not possible to generate an ID because no characters or numbers are specified.')

    new_id = '{tag}{sep}'.format(tag=tag, sep=sep)
    for _ in range(length):
        new_id += random.choice(characters + numbers)
    return new_id
