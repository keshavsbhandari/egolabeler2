from pathlib import Path
import pandas as pd
from datetime import datetime
import os
import projector
# datetime.timestamp(datetime.now())

label = 'label.csv'


def getvidlist(foldername):
    p = [*Path(foldername).glob('*.MP4')]
    key = lambda x: int(x.stem.split('-')[-1])
    p = sorted(p, key=key)
    name = [i.name for i in p]
    path = [f"{i.parent.name}/{i.name}" for i in p]
    return name, path

def getdatasource():
    return [p.as_posix() for p in Path('data').glob('*') if ((not p.name.startswith('.')) and p.is_dir())]

def getcsv():
    return pd.read_csv(label)

def update(vidname, egosummary, sursummary):
    print('I am here')
    record = {
        'time' : datetime.timestamp(datetime.now()),
        'vidname':vidname,
        'egosummary':egosummary,
        'sursummary':sursummary}
    csv = getcsv()
    csv = csv.append(record, ignore_index=True)
    csv.to_csv(label, index=None)

def countcurrent(vidname):
    key = vidname.split('-')[1]
    unq = [i for i in list(getcsv().vidname.unique()) if key in i]
    return len(unq)

def exists(vidname):
    return vidname in getcsv().vidname.values

def getlabel(vidname):
    csv = getcsv()
    csv = csv[csv['vidname'] == vidname].sort_values(by = ['time'], ascending=False)
    if not csv.empty:
        return csv.iloc[[0]].to_dict(orient='record')[0]
    else:
        return

def getstats(vidname, total):
    result = {}
    label = getlabel(vidname)
    result['total'] = total
    if label:
        result['egosummary'] = label['egosummary']
        result['sursummary'] = label['sursummary']
    else:
        result['egosummary'] = None
        result['sursummary'] = None
    result['ncount'] = countcurrent(vidname)
    result['percentstr'] = '%.2f' % ((result['ncount'] / total)*100)+"%"
    result['percent'] = int((result['ncount'] / total) * 100)
    return result

def getvideo(vidname):
    vidname = f"data/{vidname.split('-')[2]}/{vidname}"
    targetname = f"static/temp/{Path(vidname).stem}-canvas.MP4"
    if not os.path.exists(targetname):
        projector.canvas_to_video(vidname=vidname, target=targetname)