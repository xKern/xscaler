from .xscale import XScale
import os

if __name__ == "__main__":
    files = [f'./input/{f}' for f in os.listdir('input')]
    videos = [XScale(path) for path in files]

    for video in videos:
        video.output()
