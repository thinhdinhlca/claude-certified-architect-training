#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'calendar' / 'cca_daily_plan.json'


def main():
    p = argparse.ArgumentParser(description='Show CCA plan for a date')
    p.add_argument('--date', default=str(date.today()), help='YYYY-MM-DD')
    args = p.parse_args()

    data = json.loads(PLAN.read_text(encoding='utf-8'))
    day = data.get(args.date)
    if not day:
        print(f'No plan entry for {args.date}')
        return

    print(f"Date: {args.date}")
    print(f"Focus: {day['focus']}")
    print(f"Reading: {day['reading']}")
    if day.get('review_slot_4pm'):
        print('4-5 PM review: ' + ' | '.join(day['review_slot_4pm']))
    print('Test sources:')
    for s in day['test_sources']:
        print(f'  - {s}')
    print('Test command:')
    print('  ' + day['test_command'])


if __name__ == '__main__':
    main()
