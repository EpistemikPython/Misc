
import os
import sys
import moviepy.video.io.VideoFileClip as vfc


def convert_video_to_audio(video_file, output_ext="mp3"):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    filename, ext = os.path.splitext(video_file)
    clip = vfc.VideoFileClip(video_file)
    clip.audio.write_audiofile(f"{filename}.{output_ext}")


if __name__ == "__main__":
    vf = sys.argv[1]
    convert_video_to_audio(vf)
    exit()
