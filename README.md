# XScale

XScale is a very simple python utility that sits atop ffmpeg and opencv to 
downscale videos and extract a thumbnail frame.  
This was developed for Xkern's in house use.

## Simple usage
```python
from xscaler import XScale
xscale = XScale('source/foo.mov', frame_extraction_format='png',
                output_directory='destination')
xscale.output()
```
