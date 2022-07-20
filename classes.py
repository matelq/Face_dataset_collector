import os

class frame_face_box:
    def __init__(self, is_face_on_frame, bbox, frame_number):
        self.is_face_on_frame = is_face_on_frame
        self.bbox = bbox
        self.frame_number = frame_number

class chain:
    def __init__(self, start_frame, end_frame):
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.len = end_frame - start_frame

class video_chains_and_ffb:
    def __init__(self, chains, video_face_boxes, yt_id):
        self.yt_id = yt_id
        self.chains = chains
        self.video_face_boxes = video_face_boxes

    def save(self):
        os.makedirs(self.yt_id, exist_ok=True)

        chains_csv = open('{0}/chains.csv'.format(self.yt_id), 'w')
        for chain in self.chains:
            chains_csv.write(str(chain.start_frame) + ', ' + str(chain.end_frame) + ', ' + str(chain.len) + '\n')
        chains_csv.close()

        vfb_csv = open('{0}/vfb.csv'.format(self.yt_id), 'a')
        for ffb in self.video_face_boxes:
            vfb_csv.write(str(ffb.frame_number) + ', ' + str(ffb.bbox[0]) + ', ' + str(ffb.bbox[1]) + ', '
                          + str(ffb.bbox[2]) + ', ' + str(ffb.bbox[3]) + '\n')
        vfb_csv.close()