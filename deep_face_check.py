import gc
import os
import cv2
import sys
import gc
import numpy as np
import mediapipe as mp

from classes import frame_face_box, chain, video_chains_and_ffb
from video_to_images_etc import video_to_images, crop_image, images_to_video
from pytube import YouTube


from memory_profiler import profile

@profile
def face_detect(yt_id, out_dir, inp_dir, chains, fps):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs('{0}/{1}'.format(out_dir, yt_id), exist_ok=True)
    deep_face_box_csv = open('{0}/deep_face_box.csv'.format(yt_id), 'w')
    deep_face_box_csv.close()
    deep_chains_csv = open('{0}/deep_chains.csv'.format(yt_id), 'w')
    deep_chains_csv.close()

    chain_flag = False
    start_frame = 0
    end_frame = 0

    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.8) as face_detection:
        for ch in chains:
            for idx in range(ch.start_frame * fps, ch.end_frame * fps):
                file = './{0}/{1}/{2}.png'.format(inp_dir, yt_id, str(idx))
                image = cv2.imread(file)
                # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
                results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                # Draw face detections of each face.
                if not results.detections:
                    chain_flag = False
                    end_frame = idx - 1

                    if (end_frame - start_frame >= 4*fps):
                        quick_chains_csv = open('{0}/deep_chains.csv'.format(yt_id), 'a')
                        quick_chains_csv.write(str(start_frame) + ', ' + str(end_frame) + '\n')
                        quick_chains_csv.close()
                    start_frame = end_frame
                    continue
                elif (chain_flag == False):
                    start_frame = idx
                    chain_flag = True
                annotated_image = image.copy()
                for detection in results.detections:
                    mp_drawing.draw_detection(annotated_image, detection)
                    deep_face_box_csv = open('{0}/deep_face_box.csv'.format(yt_id), 'a')
                    deep_face_box_csv.write(str(idx) + ', '
                                            + str(detection.location_data.relative_keypoints[2].x) + ', '
                                            + str(detection.location_data.relative_keypoints[2].y) + ', '
                                            + str(detection.location_data.relative_bounding_box.width) + ', '
                                            + str(detection.location_data.relative_bounding_box.height) + '\n')

                cv2.imwrite('./{0}/{1}/'.format(out_dir, yt_id) + str(idx) + '.jpg', annotated_image)





def deep_face_check():
    out_dir = 'converted_to_30fps'
    os.makedirs(out_dir, exist_ok=True)
    fps = 30
    class UrlInfo:
        def __init__(self, url, key):
            self.url = url
            self.key = key

    with open('urls_from_keys.csv', 'r') as f:
        lines = f.readlines()
        lines = [x.split(',') for x in lines]
        url_infos = [UrlInfo(x[0], x[1]) for x in lines]

    results_csv = open('results.csv', 'w')
    results_csv.close()

    for ui in url_infos:
        yt = YouTube(ui.url)
        print('\n', yt.video_id, '\n')

        results_csv = open('results.csv', 'a')
        results_csv.write(yt.video_id + ', ' + str(fps) + '\n')
        results_csv.close()

        with open('{0}/quick_chains.csv'.format(yt.video_id), 'r') as f:
            lines = f.readlines()
            lines = [x.split(',') for x in lines]
            chains = [chain(int(x[0]), int(x[1])) for x in lines]

        #print(yt.streams)
        # try:
        yt.streams.get_by_resolution('720p').download(None, 'input.mp4')
        video_to_images(yt.video_id, out_dir, fps)
        face_detect(yt.video_id, 'deep_face_detected', out_dir, chains, fps)



        # except:
        #    return_msg = '{}, ERROR (deep_face_check)!'.format(yt.video_id)
        #    return return_msg
        break
