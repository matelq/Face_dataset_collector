import os
import subprocess
import ffmpeg

width_bbox_1080p = 240
height_bbox_1080p = 320

def images_to_video(inp_dir, yt_id, chain):
    try:
        #process_call_str = 'ffmpeg -f concat -safe 0 -i {0}/{1}/{2}_{3}/frame_info.txt -fps_mode vfr -pix_fmt yuv420p {4}/{2}_{3}.mp4'\
        process_call_str = 'ffmpeg -framerate 30 -i {0}/{1}/{2}_{3}/%d.jpg -loglevel error -y -pix_fmt yuv420p {4}/{2}_{3}.mp4'\
                    .format(inp_dir, yt_id, str(chain.start_frame), str(chain.end_frame), yt_id)
        status = subprocess.check_call(process_call_str, shell=True)
    except:
        return_msg = '{0} - im to vid, ERROR (ffmpeg)!'.format(yt_id)
        return return_msg

def crop_image(inp_dir, out_dir, yt_id, num, bbox, chain, ch_frame_num):

    try:
        process_call_str = 'ffmpeg -i {0}/{1}/{2}.jpg -y -loglevel error -vf "crop={3}:{4}:{5}:{6}" {7}/{8}/{9}_{10}/{11}.jpg'\
            .format(inp_dir, yt_id, str(num),
                    str(width_bbox_1080p),
                    str(height_bbox_1080p),
                    str(int((bbox[0] + bbox[2]) / 2 - width_bbox_1080p / 2)),
                    str(int((bbox[1] + bbox[3]) / 2 - height_bbox_1080p / 2)),
                    out_dir, yt_id, str(chain.start_frame), str(chain.end_frame), str(ch_frame_num))
        status = subprocess.check_call(process_call_str, shell=True)
    except:
        return_msg = '{0} - crop {1}.png, ERROR (ffmpeg)!'.format(yt_id, num)
        return return_msg


def video_to_images(yt_id, out_dir, fps):
    try:
        os.makedirs('{0}/{1}'.format(out_dir, yt_id), exist_ok=True)
        process_call_str = 'ffmpeg -i input.mp4 -vf fps={2} {0}/{1}/%d.png'.format(out_dir, yt_id, str(fps))
        status = subprocess.check_call(process_call_str, shell=True)

    except:
        return_msg = '{}, ERROR (ffmpeg)!'.format(yt_id)
        return return_msg

    return '{}, DONE!'.format(yt_id)




