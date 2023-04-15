# Python Shorts
This app is created to automate the purpose of turning short stories into YouTube Shorts. 

## How it works
### app.py
First, a short story is loaded into the `stories` directory. Then `app.py` is ran. This does several things. First, it breaks the story up into segments and adds them to a list called `text_substrings.` Each contains a few words. Every 5 `text_substrings` are grouped togther and used to generate audio files. A master audio file is also generated at this point. Then these same groupings of `text_substrings` are used to make `TextClips`. The audio files in the previous step are used to set the duration for each `TextClip`. The `TextClips` are then concatinated together, and laid over a background video. The master audio file is also included at this step. The full video is then sliced into 55 second segments and saved. 

### upload.py
After the segments are saved, they are then uploaded using code based on the YouTube getting started guide. Small modifications were made to move from Python2 to Python3