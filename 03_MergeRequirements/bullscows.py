from collections import defaultdict
from typing import Optional
from random import choice


def bullscows(guess: str, secret: str) -> tuple[int, int]:
    bulls, cows = 0, 0

    secret_chars = defaultdict(int)
    for c in secret:
        secret_chars[c] += 1

    for i, guess_char in enumerate(guess):
        if (i < len(secret)) and (guess_char == secret[i]):
            bulls += 1
            secret_chars[guess_char] -= 1
        elif secret_chars[guess_char]:
            cows += 1
            secret_chars[guess_char] -= 1
            
    return bulls, cows


def ask(prompt: str, valid: Optional[list[str]] = None) -> str:
    guess = input(prompt)

    if not valid:
        while guess not in valid:
            guess = input(prompt)

    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = choice(words)
    count = 0

    while True:
        count += 1
        guess = ask("Введите слово: ", words)

        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)

        if bulls == len(secret):
            break
        
    return count
