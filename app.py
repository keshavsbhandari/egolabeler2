from flask import Flask, render_template, request, redirect, jsonify
import utils
import random
import projector
import time
import os
from pathlib import Path

app = Flask(__name__, template_folder='template', static_folder='static')


@app.route("/getdata")
def getdata():
    target = lambda vidname: f"static/temp/{Path(vidname).stem}-canvas.MP4"
    videos = None
    result = {'data': utils.getdatasource()}
    activefolder = [False] * len(result['data'])
    default = True
    vidname = None
    default = False
    videos, paths = utils.getvidlist(request.args.get('datafolder'))
    active = 0
    if request.args.get('vidname'):
        vidname = f"{request.args.get('vidname').split('.')[1]}.MP4"
        active = int(request.args.get('vidname').split('.')[0]) - 1
        utils.getvideo(vidname)
        result.update(utils.getstats(vidname, len(videos)))

    total = len(videos)
    selected = [False] * total
    selected[active] = True
    utils.getvideo(videos[active])
    activefolder[result['data'].index(request.args.get('datafolder'))] = True
    status = [utils.exists(v) for v in videos]
    videos = [{'sno': str(i + 1).zfill(3), 'name': v, 'target': target(v), 'done': s, 'active': a, 'path': p} for
              v, i, s, a, p in
              zip(videos, range(total), status, selected, paths)]

    for v in videos:
        if v['active']:
            result.update(utils.getstats(v['name'], total))

    if default and utils.getdatasource():
        activefolder[0] = True

    if videos:
        result['videos'] = videos
        result['total'] = len(videos)
        if vidname:
            result['target'] = f"static/temp/{Path(vidname).stem}-canvas.MP4"

    result['vdata'] = [{'folder': f, 'active': a} for f, a in zip(result['data'], activefolder)]
    # print(result.keys())
    return result


@app.route("/", methods=['POST', 'GET'])
def main():
    videos = None
    result = {'data': utils.getdatasource()}
    activefolder = [False] * len(result['data'])
    default = True
    vidname = None
    if request.method == 'POST':
        default = False
        videos, paths = utils.getvidlist(request.form.get('datafolder'))
        total = len(videos)

        active = 0
        if request.form.get('vidname'):
            vidname = f"{request.form.get('vidname').split('.')[1]}.MP4"
            active = int(request.form.get('vidname').split('.')[0]) - 1
            utils.getvideo(vidname)
            result.update(utils.getstats(vidname, total))

        total = len(videos)
        selected = [False] * total
        selected[active] = True
        utils.getvideo(videos[active])
        activefolder[result['data'].index(request.form.get('datafolder'))] = True
        status = [utils.exists(v) for v in videos]
        videos = [{'sno': str(i + 1).zfill(3), 'name': v, 'done': s, 'active': a, 'path': p} for v, i, s, a, p in
                  zip(videos, range(total), status, selected, paths)]
    if default and utils.getdatasource():
        activefolder[0] = True

    if videos:
        result['videos'] = videos
        result['total'] = total
        if vidname:
            result['target'] = f"static/temp/{Path(vidname).stem}-canvas.MP4"

    result['vdata'] = [{'folder': f, 'active': a} for f, a in zip(result['data'], activefolder)]
    return render_template('home.html', result=result)


# @app.route('/getlabelandstat')
# def getlabelandstat():
#     vidname = request.args.get('vidname', None, type=str)
#     total = request.args.get('total', None, type=int)
#     result = {}
#     label = utils.getlabel(vidname)
#     result['egosummary'] = label['egosummary']
#     result['sursummary'] = label['sursummary']
#     result['ncount'] = utils.countcurrent()
#     result['percentstr'] = '%.2f' % (result['ncount'] / total)
#     result['percent'] = result['ncount'] // total
#     return result

@app.route('/getstats')
def getstats():
    vidname = request.args.get('vidname', None, type=str)
    total = request.args.get('total', None, type=int)
    # targetname = f"static/temp/{Path(vidname).stem}-canvas.MP4"
    result = utils.getstats(vidname, total)
    # result.update({'target': targetname})
    # print('I am here')
    return result


@app.route('/getvideo')
def getvideo():
    vidname = f"data/{request.args.get('vidpath', None, type=str)}"
    total = request.args.get('total', None, type=int)
    targetname = f"static/temp/{Path(vidname).stem}-canvas.MP4"
    result = {'result': targetname}
    if not os.path.exists(targetname):
        projector.canvas_to_video(vidname=vidname, target=targetname)
    result.update(utils.getstats(request.args.get('vidname', None, type=str), total))
    return result


@app.route('/saveresponse')
def saveresponse():
    vidname = request.args.get('vidname', None, type=str)
    egosummary = request.args.get('ego', None, type=str)
    sursummary = request.args.get('sur', None, type=str)
    total = request.args.get('total', None, type=int)
    utils.update(vidname, egosummary, sursummary)
    return utils.getstats(request.args.get('vidname', None, type=str), total)


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


if __name__ == "__main__":
    app.run(debug=True)
