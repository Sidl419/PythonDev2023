from collections import defaultdict

def bullscows(guess: str, secret: str) -> tuple[int, int]:
    bulls, cows = 0, 0
    secret_chars = defaultdict(int)
    for c in secret:
        secret_chars[c] += 1
    for i in range(len(guess)):
        if i < len(secret) and guess[i] == secret[i]:
            bulls += 1
            secret_chars[guess[i]] -= 1
        elif secret_chars[guess[i]]:
            secret_chars[guess[i]] -= 1
            cows += 1
    return bulls, cows
