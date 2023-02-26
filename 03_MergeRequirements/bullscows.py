from cowsay import cowsay, get_random_cow
from collections import defaultdict
from typing import Optional
from random import choice
import argparse
from urllib import request
import os


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
    prompt = f"""
      ________________ 
     < {prompt} >
      ---------------- 
      \   ^__^
       \  (*o)\_______        
          (__)\       )\/\ 
              ||----W |    
              ||     ||
    """
    guess = input(prompt)

    if not valid:
        while guess not in valid:
            guess = input(prompt)

    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay(message=format_string.format(bulls, cows), cow=get_random_cow()) + '\n')


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='bulls and cows game')
    parser.add_argument('dictionary', type=str, nargs=1, help='allowed words dictionary')
    parser.add_argument('--length', type=int, default=5, required=False, help='length of allowed words')
    args = parser.parse_args()

    if os.path.exists(args.dictionary[0]):
        file_name = args.dictionary[0]
    else:
        file_name = args.dictionary[0].split('/')[-1]
        request.urlretrieve(args.dictionary[0], file_name)

    allowed_words = []
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            if len(line) == args.length:
                allowed_words.append(line)
    
    count = gameplay(ask=ask, inform=inform, words=allowed_words)
    print(cowsay(message=f"Верно! Вы использовали {count} попыток", cow=get_random_cow()) + '\n')
