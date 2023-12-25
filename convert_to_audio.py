import soundfile
from soundfile import write


def convert_mp3_to_wav(input_file, output_file):
    with soundfile.SoundFile(input_file) as sf:
        write(output_file, sf.samplerate, sf.channels, sf.frame_rate, sf.frames)


input_file = 'input.mp3'
output_file = 'output.wav'
convert_mp3_to_wav(input_file, output_file)
