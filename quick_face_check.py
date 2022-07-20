import os
import cv2
import subprocess
import ffmpeg
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from classes import frame_face_box, chain, video_chains_and_ffb

from downscale import downscale
from video_to_images_etc import video_to_images, crop_image, images_to_video
from pytube import YouTube





def face_detect(yt_id, out_dir, inp_dir):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs('{0}/{1}'.format(out_dir, yt_id), exist_ok=True)

    video_face_boxes = list()
    chains = list()
    chain_flag = True
    start_sec = 0
    end_sec = 0

    app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))

    for i in range(1, len(os.listdir(path='./{0}/{1}'.format(inp_dir, yt_id)))):
        print(i)
        img = ins_get_image('D:/WORK/avspeech/{0}/{1}/{2}'.format(inp_dir, yt_id, str(i)))
        faces = app.get(img)

        if (len(faces) == 1):
            ffb = frame_face_box(True, faces[0].bbox, i)

            if((ffb.bbox[2] - ffb.bbox[0]) / (ffb.bbox[3] - ffb.bbox[1]) <= 0.8
                    and (ffb.bbox[2] - ffb.bbox[0]) / (ffb.bbox[3] - ffb.bbox[1]) >= 0.65
                    and ffb.bbox[2] - ffb.bbox[0] > 40
                    and ffb.bbox[3] - ffb.bbox[1] > 40):

                if(chain_flag == False):
                    start_sec = i
                    chain_flag = True

                video_face_boxes.append(ffb)
                #crop_image(inp_dir, out_dir, yt_id, i, ffb.bbox) #for testing

            else:
                if(chain_flag == True):
                    end_sec = i - 1
                    chains.append(chain(start_sec, end_sec))
                    chain_flag = False
        else:
            if (chain_flag == True):
                end_sec = i - 1
                chains.append(chain(start_sec, end_sec))
                chain_flag = False




                #rimg = app.draw_on(img, faces)
                #cv2.imwrite('./{0}/{1}/{2}.jpg'.format(out_dir, yt_id, str(i)), rimg)
    #images_to_video(out_dir, inp_dir, yt_id)
    vcaf = video_chains_and_ffb(chains, video_face_boxes, yt_id)
    return vcaf





def quick_face_check():
    out_dir = 'converted_to_1fps'
    os.makedirs(out_dir, exist_ok=True)

    class UrlInfo:
        def __init__(self, url, key):
            self.url = url
            self.key = key

    with open('urls_from_keys.csv', 'r') as f:
        lines = f.readlines()
        lines = [x.split(',') for x in lines]
        url_infos = [UrlInfo(x[0], x[1]) for x in lines]

    for ui in url_infos:
        yt = YouTube(ui.url)
        print('\n', yt.video_id, '\n')
        #yt.streams.get_by_resolution('360p').download(None, 'input.mp4')
        #downscale(yt.video_id, out_dir) upgraded to video_to_images
        #video_to_images(yt.video_id, out_dir, 1)
        vcaf = face_detect(yt.video_id, 'face_detected', out_dir)
        vcaf.save()
        #print(vcaf)
        #images_to_video(out_dir, out_dir, yt.video_id)
        break


