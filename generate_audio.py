from gtts import gTTS
  
# Language in which you want to convert
language = 'en'
  
def generate_audio(text_substrings):
  
    # The text that you want to convert to audio
    mytext = 'Welcome to geeksforgeeks!'
    

    for snippet, index in enumerate(text_substrings):
        audio = gTTS(text=snippet, lang=language)
        audio.save("audio_{:03d}.mp3".format(index))