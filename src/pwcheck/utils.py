
import math, string

def estimate_entropy(password: str) -> float:
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(c in string.punctuation for c in password): pool += len(string.punctuation)
    if any(ord(c) > 127 for c in password): pool += 50
    if pool == 0: return 0.0
    return len(password) * math.log2(pool)

def estimate_bruteforce_time(entropy_bits: float, attempts_per_second: float) -> float:
    if entropy_bits <= 0: return float('inf')
    avg_attempts = 2 ** (entropy_bits - 1)
    return avg_attempts / attempts_per_second

def human_readable_time(seconds: float) -> str:
    if seconds == float('inf'): return 'infinite'
    units = (('years',60*60*24*365),('days',60*60*24),('hours',60*60),('minutes',60),('seconds',1))
    parts = []
    for name, sec in units:
        if seconds >= sec:
            val = int(seconds // sec)
            seconds -= val*sec
            parts.append(f"{val} {name}")
    return ', '.join(parts) if parts else '<1 second'

def read_common_passwords(path: str):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return set(line.strip() for line in f if line.strip())
    except Exception:
        return set()
