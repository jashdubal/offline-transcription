
import os
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
pipeline = KPipeline(lang_code='a')

text = "The sky above the port was the color of television, tuned to a dead channel."

generator = pipeline(
    text, voice='af_bella',
    speed=1, split_pattern=r'\n+'
)

if not os.path.exists('tmp'):
    os.makedirs('tmp', exist_ok=True)    

for i, (gs, ps, audio) in enumerate(generator):
    print(i)  # i => index
    print(gs) # gs => graphemes/text
    print(ps) # ps => phonemes
    display(Audio(data=audio, rate=24000, autoplay=i==0))
    sf.write(f'tmp/{i}.wav', audio, 24000) # save each audio file
