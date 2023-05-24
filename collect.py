#!/usr/bin/env python3
from datetime import datetime, timedelta
import os
import requests
import time
import argparse

def mkdirs(d):
    os.makedirs(d, exist_ok=True)

def fmtymd(d):
    date_format = "%Y%m%d"
    return d.strftime(date_format)

def fmtamtrak(d):
    return d.strftime('%m/%d/%Y')

URL = 'http://localhost:3000/request'
def fetch(origin, dest, d, folder):
    ymd = fmtymd(d)
    damtrak = fmtamtrak(d)
    now = datetime.now().strftime('%Y%m%d-%H%M')
    print('damtrak: %s now: %s' % (damtrak, now))
    url = URL + '?origin=%s&dest=%s&date=%s' % (origin, dest, damtrak)
    print(url)
    r = requests.get(url, timeout=120) # 2 minutes
    if r.status_code // 100 == 2:
        if r.text.startswith('{"error"'):
            print('Amtrak ratelimit', origin, dest, d, r.text)
        else:
            open('%s/%s-%s/%s/%s.json' % (folder, origin, dest, ymd, now), 'w').write(r.text)
            print('OK', origin, dest, d)
    else:
        print('Server Error', origin, dest, d, r.text)

def add_if_pos(days, dt):
    now = datetime.now()
    if now <= dt:
        days.append(dt)
    return days

def main(args):
    origin = args.origin
    dest = args.dest
    if not origin or not dest:
        print('No origin or dest')
        return
    def future(n):
        return datetime.now() + timedelta(days=n)
    days = []
    if not args.exclude_today:
        days += [datetime.now()]
    for i in range(1, 1+args.future_days):
        days += [future(i)]
    for i in args.days: # YYYYMMDD
        days += [datetime(i//10000, (i//100)%100, i%100)]
    print('days: %s', days)
    for day in days:
        mkdirs('%s/%s-%s/%s' % (args.output, origin, dest, fmtymd(day)))
        try:
            fetch(origin, dest, day, args.output)
        except Exception as e:
            print("Exception:", e)
        time.sleep(30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--origin', type=str, help='the origin station')
    parser.add_argument('--dest', type=str, help='the destination station')
    parser.add_argument('--future-days', type=int, default=0, help='future days to scrape for (with n=1, scrape today and tomorrow)')
    parser.add_argument('--days', type=int, nargs='+', help='dates in YYYYMMDD format to scrape')
    parser.add_argument('--exclude-today', action='set_true', help='excludes today')
    parser.add_argument('--output', type=str, help='the output folder', default='data')

    main(parser.parse_args())
