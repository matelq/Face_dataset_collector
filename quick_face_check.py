import os
import cv2
import subprocess
import ffmpeg
import numpy as np
import mediapipe as mp

from classes import frame_face_box, chain, video_chains_and_ffb
from video_to_images_etc import video_to_images, crop_image, images_to_video
from pytube import YouTube

from memory_profiler import profile

@profile
def face_detect(yt_id, out_dir, inp_dir):
    os.makedirs(yt_id, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs('{0}/{1}'.format(out_dir, yt_id), exist_ok=True)
    quick_chains_csv = open('{0}/quick_chains.csv'.format(yt_id), 'w')
    quick_chains_csv.close()

    chain_flag = False
    start_sec = 0
    end_sec = 0

    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    IMAGE_FILES = []
    for i in range(1, len(os.listdir(path='./{0}/{1}'.format(inp_dir, yt_id)))):
        IMAGE_FILES.append('./{0}/{1}/{2}.png'.format(inp_dir, yt_id, str(i)))
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(file)
            # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
            results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Draw face detections of each face.
            if not results.detections:
                chain_flag = False
                end_sec = idx - 1

                if(end_sec - start_sec >= 4):
                    quick_chains_csv = open('{0}/quick_chains.csv'.format(yt_id), 'a')
                    quick_chains_csv.write(str(start_sec) + ', ' + str(end_sec) + '\n')
                    quick_chains_csv.close()
                start_sec = end_sec
                continue
            elif(chain_flag == False):
                start_sec = idx
                chain_flag = True
            annotated_image = image.copy()
            for detection in results.detections:
                mp_drawing.draw_detection(annotated_image, detection)

            cv2.imwrite('./{0}/{1}/'.format(out_dir, yt_id) + str(idx) + '.jpg', annotated_image)
    #images_to_video(out_dir, inp_dir, yt_id)


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
        face_detect(yt.video_id, 'face_detected', out_dir)

        #images_to_video(out_dir, out_dir, yt.video_id)
        break


