# import sys
import os
import ffmpeg
import logzero
from logzero import logger
import cv2
import random

logzero.logfile('xscaler_output.log')


class XScale():
    desired_audio_bitrate = 131072
    desired_video_bitrate = 2500000

    def __init__(self,
                 input_file_path,
                 output_directory='output',
                 video_output_format='mp4',
                 frame_extraction_format='jpg'):

        self.__input_file_path = input_file_path
        self.__output_directory = output_directory

        self.video_output_format = video_output_format
        self.frame_extraction_format = frame_extraction_format

        self.video = ffmpeg.input(input_file_path)
        self.probe = ffmpeg.probe(input_file_path)

        self.full_input_path = self.probe['format']['filename']
        self.filename = os.path.basename(self.probe['format']['filename'])

        self.video_streams = [
            stream for stream in self.probe['streams']
            if stream['codec_type'] == 'video'
        ]
        self.audio_streams = [
            stream for stream in self.probe['streams']
            if stream['codec_type'] == 'audio'
        ]

        self.formats = self.probe['format']['format_name'].split(',')
        self.closest_video_stream = None
        self.closest_audio_stream = None
        self.output_audio_bitrate = None
        self.__process()

    def __process(self):
        if len(self.video_streams) > 1:
            # process it further and chose a stream
            # ( width, height )
            # 852 x 480
            ranges = [
                (stream['height'] - 480) for stream in self.video_streams
            ]
            closest = ranges.index(min(ranges))
            self.closest_video_stream = self.video_streams[closest]
        else:
            self.closest_video_stream = self.video_streams[0]

        if len(self.audio_streams) > 1:
            ranges = []
            for stream in self.audio_streams:
                try:
                    push = int(stream['bit_rate']) - self.desired_audio_bitrate
                except KeyError:
                    push = (
                        int(stream['sample_rate']) - self.desired_audio_bitrate
                        )
                ranges.append(push)
            closest = ranges.index(min(ranges))
            self.closest_audio_stream = self.audio_streams[closest]
        else:
            try:
                self.closest_audio_stream = self.audio_streams[0]
            except IndexError:
                # Is there no audio stream? That's sort of stupid
                # Yeah i didn't check for video, would be kind of
                # awkward to process a video where a video stream is not
                # present
                self.closest_audio_stream = None

        if self.closest_audio_stream:
            try:
                available_audio_bitrate = (
                    int(self.closest_audio_stream['bit_rate']))
            except KeyError:
                available_audio_bitrate = int(
                    self.closest_audio_stream['sample_rate']
                )
            if available_audio_bitrate <= self.desired_audio_bitrate:
                self.output_audio_bitrate = available_audio_bitrate
            else:
                self.output_audio_bitrate = available_audio_bitrate
        else:
            self.output_audio_bitrate = None

        # pp(self.closest_audio_stream)
        # pp(self.closest_video_stream)
        return -1

    def output(self):
        """ Generate output using ffmpeg """
        streams = []
        args = {}
        args['b:v'] = '2.5M'
        args['vcodec'] = 'libx264'

        ch_vid = str(self.closest_video_stream['index'])
        video = self.video.video
        video = self.video[ch_vid]
        video = video.filter('scale', 854, 480)
        video = video.filter('fps', 24)
        streams.append(video)

        try:
            ch_aud = str(self.closest_audio_stream['index'])
            audio = self.video[ch_aud]
            audio = self.video.audio
            args['acodec'] = 'libmp3lame'
            args['ac'] = 1
            args['b:a'] = self.output_audio_bitrate
            streams.append(audio)
        except TypeError:
            # There isn't an audio stream. Lets handle that
            pass
        filename = os.path.splitext(self.filename)[0]
        extsn = self.video_output_format
        output_path = (
            f'{self.__output_directory}/{filename}.{extsn}'
        )
        output = ffmpeg.output(*streams,
                               output_path,
                               **args)

        self.__debug_info(output.get_args())
        print(''.join(output.get_args()))
        try:
            output.run(overwrite_output=True, quiet=False)
            logger.info(f"{self.filename} processed")
            self.__process_frame()
        except ffmpeg.Error as e:
            logger.error(f'Processing {self.filename} failed due to')
            logger.error(e)

    def __process_frame(self):
        vid_extsn = self.video_output_format
        extsn = self.frame_extraction_format
        filename = os.path.splitext(self.filename)[0]
        # Extract frame
        vidcap = cv2.VideoCapture(
            f'./{self.__output_directory}/{filename}.{vid_extsn}')
        success, image = vidcap.read()
        success = True
        thumbs = []
        while success:
            success, image = vidcap.read()
            thumbs.append(image)

        # pick a frake
        logger.info("All frames extracted")
        frame = random.choice(thumbs)
        cv2.imwrite(f'./{self.__output_directory}/{filename}_thumb.{extsn}',
                    frame)
        logger.info("Extracted and saved single frame.")

    def __debug_info(self, args):
        num_streams_vid = num_streams_aud = 0
        try:
            num_streams_vid = len(self.video_streams)
        except TypeError:
            pass

        try:
            num_streams_aud = len(self.audio_streams)
        except TypeError:
            pass

        logger.debug(f'Processing {self.filename}')
        logger.debug(
            (f'Discovered {num_streams_vid} video streams and'
             f' {num_streams_aud} audio streams')
        )
        logger.debug('ffmpeg parameters:')
        logger.debug(
            ' '.join(args)
        )
