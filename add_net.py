#!/usr/bin/env python3
"""Interactively append a net to the Net Tracking Calendar nets.json file.

Usage: python3 add_net.py [path/to/nets.json]
Times are entered and saved in UTC. Weekdays: Sunday=0 ... Saturday=6.
"""
import json
import re
import sys
import uuid
from pathlib import Path

DAYS = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
MODES = ('SSB', 'FM', 'Digital', 'CW')


def prompt(label, default=None, required=False):
    suffix = f' [{default}]' if default is not None else ''
    while True:
        value = input(f'{label}{suffix}: ').strip()
        if value:
            return value
        if default is not None:
            return str(default)
        if not required:
            return ''
        print('  This field is required.')


def choose(label, choices):
    print(f'\n{label}')
    for index, option in enumerate(choices, 1):
        print(f'  {index}. {option}')
    while True:
        answer = prompt('Choose number')
        if answer.isdigit() and 1 <= int(answer) <= len(choices):
            return int(answer) - 1
        print('  Enter a listed number.')


def get_time():
    while True:
        value = prompt('Start time UTC (HH:MM)', required=True)
        if re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', value):
            return value
        print('  Use 24-hour UTC time, e.g. 23:30.')


def get_duration():
    while True:
        value = prompt('Duration in minutes', 60)
        if value.isdigit() and 1 <= int(value) <= 1440:
            return int(value)
        print('  Enter a whole number between 1 and 1440.')


def get_recurrence():
    choice = choose('Repeat schedule:', ('Daily', 'Selected weekdays', 'Nth weekday of month'))
    if choice == 0:
        return {'type': 'daily'}
    if choice == 1:
        print('  Weekdays: ' + ', '.join(f'{i}={d}' for i, d in enumerate(DAYS)))
        while True:
            raw = prompt('Days (comma-separated, e.g. 1,3,5)', required=True)
            parts = [p.strip() for p in raw.split(',')]
            if all(p in '0123456' and len(p) == 1 for p in parts):
                return {'type': 'weekdays', 'days': sorted(set(map(int, parts)))}
            print('  Use values 0 through 6, separated by commas.')
    ordinal_idx = choose('Week of month:', ('First', 'Second', 'Third', 'Fourth', 'Fifth (if present)', 'Last'))
    weekday = choose('Day of week:', DAYS)
    ordinal = (1, 2, 3, 4, 5, -1)[ordinal_idx]
    return {'type': 'monthly', 'ordinal': ordinal, 'weekday': weekday}


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('nets.json')
    if not path.is_file():
        sys.exit(f'File not found: {path}\nPlace add_net.py beside nets.json or specify the path.')
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, OSError) as exc:
        sys.exit(f'Cannot read JSON: {exc}')
    if not isinstance(data, dict) or not isinstance(data.get('nets'), list):
        sys.exit('Invalid file: expected an object with a "nets" array.')

    print(f'\nAdd a net to {path}\n(All scheduling times/days are UTC.)\n')
    name = prompt('Net name', required=True)
    freq = prompt('Frequency / channel (e.g. 146.940 MHz)')
    mode = MODES[choose('Mode:', MODES)]
    start = get_time()
    duration = get_duration()
    recurrence = get_recurrence()
    notes = prompt('Notes / PL tone / Winlink address')

    record = {
        'id': f'net-{uuid.uuid4().hex[:12]}',
        'name': name,
        'frequency': freq,
        'mode': mode,
        'notes': notes,
        'startUtc': start,
        'durationMinutes': duration,
        'recurrence': recurrence,
        'enabled': True,
    }
    print('\nNew entry:')
    print(json.dumps(record, indent=2, ensure_ascii=False))
    if prompt('Add this net? (y/N)', 'N').lower() not in ('y', 'yes'):
        print('Cancelled; no changes made.')
        return

    data['nets'].append(record)
    # Write to a temporary file and replace the original only after writing succeeds.
    temp = path.with_name(path.name + '.tmp')
    try:
        with temp.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)
    print(f'\nSaved! {len(data["nets"])} nets in {path}.')


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nCancelled.')
        sys.exit(1)
