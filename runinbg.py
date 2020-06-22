from pathlib import Path
import argparse
import os
from tqdm import tqdm
import projector

get_target = lambda vidname: f"static/temp/{Path(vidname).stem}-canvas.MP4"
notexists = lambda path: not os.path.exists(get_target(path))

parser = argparse.ArgumentParser(description='Example with long option names')

parser.add_argument('--data', dest="data", type=str, help="Folder inside 'data' folder")
parser.add_argument('--n', action="store", default=1, dest="n", type=int, help="Number of videos ")
parser.add_argument('--all', action="store_true", default=False, dest="all",
                    help="pass this argument if you want to transform all video")


def getargs():
    args = parser.parse_args()
    return args.data, args.n, args.all


def convert(data, n = None):
    source = [*Path(f"{data}").glob("*.MP4")]
    if not source:
        print(f"No data found @ {data}")
        return
    source = [*filter(notexists, source)]
    if not source:
        print(f"All conversion completed")
        return

    if n:
        if len(source) <= n:
            print(f"Running smaller or same batch since {n} <= remaining {len(source)}")
        else:
            source = source[:n]
    else:
        print(f"Running all {len(source)} remaining sample inside {data}")

    target = [*map(get_target, source)]
    for i in tqdm(range(len(source))):
        projector.canvas_to_video(source[i].as_posix(), target[i])


if __name__ == "__main__":
    data, n , all = getargs()
    assert n >= 1, 'n should be greater or equal 1'
    if all:
        convert(data)
    else:
        convert(data, n)




