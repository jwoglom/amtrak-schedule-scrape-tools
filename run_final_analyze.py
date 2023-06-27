import datetime
import os
import subprocess
import json

def datestr(d):
    return '%04.f%02.f%02.f' % (d.year, d.month, d.day)

def main(data_folder, out_folder, analyze_cwd):
    yday = datetime.datetime.now() - datetime.timedelta(days=1)
    ydaystr = datestr(yday.date())
    for folder in sorted(os.listdir(data_folder)):
        folder_path = os.path.join(data_folder, folder)
        if not os.path.isdir(folder_path):
            continue

        day = os.path.basename(folder_path)
        try:
            day = int(day)
        except Exception:
            pass
        if not day:
            continue
        if day >= int(ydaystr):
            continue
        outpath = os.path.join(out_folder, '%s.json' % str(day))
        if os.path.exists(outpath):
            continue
        print(folder_path, outpath)
        r = subprocess.run(['python3', './analyze.py', '--folder='+data_folder, '--date='+str(day), '--with-detail'], capture_output=True, cwd=analyze_cwd)
        out = r.stdout.decode()
        if not out:
            print('error', r.stderr.decode())
            exit(1)
        open(outpath, 'w').write(out)


if __name__ == '__main__':
    import argparse
    a = argparse.ArgumentParser()
    a.add_argument('--data-folder', default=None)
    a.add_argument('--out-folder', default=None)
    a.add_argument('--analyze-cwd', default=os.getcwd())
    args = a.parse_args()

    main(data_folder=args.data_folder, out_folder=args.out_folder, analyze_cwd=args.analyze_cwd)

