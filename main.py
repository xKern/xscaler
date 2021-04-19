from xscaler import XScale
import ffmpeg
from prettyprinter import pprint as pp

a = XScale('test.mp4', output_directory='output', frame_output_directory='thumb')
a.output()
print(a.sha1)
print(a.thumb_sha1)
print(a.output_file_path)
print(a.output_thumb_path)
