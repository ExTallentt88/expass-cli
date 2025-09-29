
import hashlib, requests
HIBP_RANGE_URL = 'https://api.pwnedpasswords.com/range/{}'
def sha1_hex(s: str) -> str:
    return hashlib.sha1(s.encode('utf-8')).hexdigest().upper()
def check_pwned(password: str):
    sh = sha1_hex(password)
    prefix, suffix = sh[:5], sh[5:]
    url = HIBP_RANGE_URL.format(prefix)
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"HIBP returned status {resp.status_code}")
    for line in resp.text.splitlines():
        h,c = line.split(':')
        if h == suffix:
            return int(c)
    return 0
