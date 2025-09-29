
import argparse
import getpass
import sys
from typing import List
from .hibp import check_pwned
from .utils import estimate_entropy, estimate_bruteforce_time, human_readable_time, read_common_passwords
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
DEFAULT_RATES = [1e3, 1e6, 1e9]

def build_parser():
    p = argparse.ArgumentParser(prog='expass', description='Password Strength Tester CLI')
    p.add_argument('--password', '-p', type=str, help='Password to check (not recommended on CLI)')
    p.add_argument('--interactive', '-i', action='store_true', help='Prompt for password (hidden input)')
    p.add_argument('--check-hibp', action='store_true', help='Check Have I Been Pwned API (requires internet)')
    p.add_argument('--common-dict', type=str, help='Path to common passwords file (one per line)')
    p.add_argument('--rates', nargs='*', type=float, help='Attack rates (attempts/sec)')
    return p

def analyze_password(pw: str, rates: List[float], common_dict_path: str=None, check_hibp_flag: bool=False):
    entropy = estimate_entropy(pw)
    table = Table(title='Password Analysis')
    table.add_column('Metric', style='cyan', no_wrap=True)
    table.add_column('Value', style='magenta')
    table.add_row('Length', str(len(pw)))
    table.add_row('Entropy (bits)', f"{entropy:.2f}")

    rates = rates or DEFAULT_RATES
    bf_table = Table(title='Brute-force estimates')
    bf_table.add_column('Rate (attempts/sec)')
    bf_table.add_column('Estimated time')
    for r in rates:
        sec = estimate_bruteforce_time(entropy, attempts_per_second=r)
        bf_table.add_row(f"{int(r):,}", human_readable_time(sec))

    console.print(table)
    console.print(bf_table)

    
    common_hits = []
    if common_dict_path:
        common = read_common_passwords(common_dict_path)
        if pw in common:
            common_hits.append('Found in provided common-passwords file.')
    builtin = {'password','123456','qwerty','12345678','111111'}
    if pw.lower() in builtin:
        common_hits.append('Very common password (builtin check).')
    console.print(Panel('\n'.join(common_hits) if common_hits else 'No common-password hits detected', title='Common Passwords'))

    # HIBP
    if check_hibp_flag:
        try:
            cnt = check_pwned(pw)
            if cnt:
                console.print(Panel(f'Found in HIBP {cnt} times', title='Have I Been Pwned'))
            else:
                console.print(Panel('Not found in HIBP', title='Have I Been Pwned'))
        except Exception as e:
            console.print(f"[yellow]HIBP check failed:[/] {e}")

    
    recs = []
    if entropy < 28:
        recs.append('Very weak — use a passphrase >12 chars.')
    elif entropy < 50:
        recs.append('Weak — increase length and mix character types.')
    else:
        recs.append('Good — high entropy. Use a password manager if needed.')
    if any(ch.isalpha() for ch in pw) and not any(ch.isupper() for ch in pw):
        recs.append('Add uppercase letters.')
    if any(ch.isdigit() for ch in pw) and len(pw) < 10:
        recs.append('Increase length; digits alone are not enough.')
    if not any(ch.isdigit() for ch in pw):
        recs.append('Add digits.')
    if not any(ch in "!@#$%^&*()-_=+[]{}|;:\'\",.<>/?`~" for ch in pw):
        recs.append('Add special characters for variety.')

    console.print(Panel('\n'.join(recs[:10]), title='Recommendations'))    

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.password and not args.interactive:
        parser.print_help()
        sys.exit(0)
    pw = args.password
    if args.interactive:
        pw = getpass.getpass('Enter password (hidden): ')
    if not pw:
        console.print('[red]No password provided.[/]')
        sys.exit(1)
    analyze_password(pw, args.rates, common_dict_path=args.common_dict, check_hibp_flag=args.check_hibp)
