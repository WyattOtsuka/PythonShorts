from gtts import gTTS
from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects
from mutagen.mp3 import MP3
import math

language = 'en'


# Take in a text file for a reddit story

# Filter out profane language

# Slice the story into strings of less than x char to the nearest whole word
def split_story(story, max_length):
    text_substrings = []

    while (len(story) > max_length):
        sample_substring = story[:max_length]
        last_space_index = sample_substring.rfind(' ')
        new_line_index = sample_substring.rfind('\n')
        if new_line_index != -1:
            text_substrings.append(story[:new_line_index])
            story = story[new_line_index+1:]
        elif last_space_index != -1: 
            text_substrings.append(story[:last_space_index])
            story = story[last_space_index+1:]
        else:
            raise Exception
    text_substrings.append(story)

    print("Substrings Generated")
    return text_substrings

# Generate a mp3 file for each substring
def generate_audio(story):
    for i in range(0, len(text_substrings), 5):
        if i + 5 > len(text_substrings): 
            snippet = ' '.join(text_substrings[i:])
        else:
            snippet = ' '.join(text_substrings[i:i+5])
        audio = gTTS(text=snippet, lang=language)
        audio.save("audio/audio_{:03d}.mp3".format((int)(i/5)))
    
    audio = gTTS(text=story, lang=language) 
    audio.save("audio/master_audio.mp3")
    print("Audio Generated")


# Loop a video of an MC parkour and place mp3 and subtitles over it
def edit_video(text_substrings):

    bg_video = VideoFileClip("static/bg.mp4", audio=False).\
        crop(width = 1080, height = 1920)
    screensize = (1080,1920)

    subtitles = []
    for i in range(0, len(text_substrings), 5):
        audio = MP3("audio/audio_{:03d}.mp3".format((int)(i/5)))

        txtClip = TextClip("\n".join(text_substrings[i:i+5]),color='white', font="Amiri-Bold", fontsize=32).\
        on_color(size = (405, 1080), color = (50,50,50), col_opacity = 0.5).\
        set_duration(audio.info.length * 2 / 3 - 0.25)

        subtitles.append(txtClip)
        

    concat_subtitles = concatenate_videoclips(subtitles)
    concat_audio = concatenate_audioclips([AudioFileClip("audio/master_audio.mp3"), AudioFileClip("audio/silence.mp3")])
    cvc = CompositeVideoClip([bg_video, concat_subtitles.set_pos('center')], use_bgclip=True, size=screensize).\
        crop(width = 405, height = 1920, x_center = 640, y_center = 360).\
        fx( vfx.speedx, 2/3) 


    cvc = cvc.set_audio(concat_audio).\
        fx( vfx.speedx, 3/2).\
        set_duration(MP3("audio/master_audio.mp3").info.length * 2 / 3 + 2)

    print("Video edited")
    return cvc
    

# Cut into 55 second segments
def slice_video(full_video):
    for i in range(0, math.ceil(full_video.duration), 55):
        if i +55 > full_video.duration:
            subclip= full_video.subclip(i, full_video.duration)
        else:
            subclip = full_video.subclip(i, i + 55)
        subclip.write_videofile(f'slices/product_{(int)(i/55)}.mp4', fps=24,codec='libx264')
    full_video.write_videofile('product.mp4', fps=24,codec='libx264')
    print("Video Sliced")


# Upload to youtube API
def upload():
    pass



with open('stories/story.txt') as file:
    story = file.read()

text_substrings = split_story(story, 25)

# generate_audio(story)

full_video = edit_video(text_substrings)

slice_video(full_video)