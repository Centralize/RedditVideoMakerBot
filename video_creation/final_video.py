from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    concatenate_audioclips,
    CompositeAudioClip,
    CompositeVideoClip,
)
from utils.console import print_step, print_substep


W, H = 1080, 1920


def make_final_video(number_of_clips):
    try:
        print_step("Creating the final video 🎥")
        VideoFileClip.reW = lambda clip: clip.resize(width=W)
        VideoFileClip.reH = lambda clip: clip.resize(width=H)

        background_clip = VideoFileClip("assets/mp4/clip.mp4").without_audio()

        if background_clip.w > background_clip.h:
            background_clip.resize(height=H).crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)

        # Gather all audio clips
        audio_clips = []
        for i in range(0, number_of_clips):
            audio_clips.append(AudioFileClip(f"assets/mp3/{i}.mp3"))
        audio_clips.insert(0, AudioFileClip(f"assets/mp3/title.mp3"))
        audio_concat = concatenate_audioclips(audio_clips)
        audio_composite = CompositeAudioClip([audio_concat])

        # Gather all images
        image_clips = []
        for i in range(0, number_of_clips):
            image_clips.append(
                ImageClip(f"assets/png/comment_{i}.png")
                .set_duration(audio_clips[i + 1].duration)
                .set_position("center")
                .resize(width=background_clip.w - (background_clip.w * 0.05)),
            )
        image_clips.insert(
            0,
            ImageClip(f"assets/png/title.png")
            .set_duration(audio_clips[0].duration)
            .set_position("center")
            .resize(width=background_clip.w - (background_clip.w * 0.05)),
        )
        image_concat = concatenate_videoclips(
            image_clips, method="compose"
        ).set_position(("center", 0.3), relative=True)
        image_concat.audio = audio_composite
        final = CompositeVideoClip([background_clip, image_concat])
        final.write_videofile(
            "assets/final_video.mp4",
            fps=30,
            audio_codec="aac",
            audio_bitrate="192k",
            preset="ultrafast",
        )
        print_substep("WOOHOO! Video is saved at assets/final_video.mp4 🎉")
    except Exception as e:
        print(e)
