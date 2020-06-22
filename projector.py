import py360convert as projector
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm
import os



def get_canvas(frame):
    cubes = projector.e2c(frame, cube_format='dict')
    F = cubes['F']
    D = cubes['D']
    B = cubes['B']
    L = cubes['L']
    R = cubes['R']
    U = cubes['U']

    FDB = np.concatenate([F, D, np.flipud(B)])
    LDR = np.rot90(np.concatenate([L, np.rot90(D, -1), np.fliplr(np.rot90(R, -2))], 0), 1)
    centre = np.ones((768, 768, 3)).astype(LDR.dtype) * 255
    centre[256:-256, :] = LDR
    centre[:, 256:-256, :] = FDB

    top = np.concatenate([L, F, np.fliplr(R)], 1)
    down = np.concatenate([np.rot90(L, -2), np.flipud(B), np.flipud(R)], 1)
    left = np.concatenate([np.rot90(F, 1), np.rot90(L, 1), np.rot90(np.flipud(B), -1)])
    right = np.concatenate([np.rot90(F, -1), np.fliplr(np.rot90(R, 1)), np.fliplr(np.rot90(B))])

    pad = 10
    canvas = np.ones((256 * 2 + 768 + pad * 2, 256 * 2 + 768 + pad * 2, 3)).astype(centre.dtype) * 255
    canvas[256 + pad:256 + pad + 768, 256 + pad:256 + pad + 768] = centre
    canvas[:256, 256 + pad:256 + pad + 768] = top
    canvas[-256:, 256 + pad:256 + pad + 768] = down
    canvas[256 + pad:256 + pad + 768, :256] = left
    canvas[256 + pad:256 + pad + 768, -256:] = right

    return canvas


def canvas_to_video(vidname='egok360-Lunch-Eating-2382.MP4', target = 'canvas.mp4'):
    cap = cv2.VideoCapture(vidname)
    fps = cap.get(cv2.CAP_PROP_FPS)
    canvas = cv2.VideoWriter(target, cv2.VideoWriter_fourcc(*'H264'), fps, (1300, 1300))
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    for _ in tqdm(range(int(frame_count))):
        ret, frame = cap.read()
        canvas.write(get_canvas(frame))
    cap.release()
    canvas.release()