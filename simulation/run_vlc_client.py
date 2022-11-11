import vlc
import os
import time
import sys
from datetime import datetime

BASEDIR = os.getcwd()

from threading import Timer
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def init_results_file(filename):
    file = open(filename, 'w')
    file.write(
        'time,'
        'demux_bytes_read,'
        'demux_bitrate,'
        'demux_corrupted,'
        'frames_displayed,'
        'frames_lost,'
        'buffers_played,'
        'buffers_lost\n'
    )
    return file

def write_stat(file, start_time, media):
    stats = vlc.MediaStats()
    vlc.libvlc_media_get_stats(media, stats)
    file.write((
        f'{time.time() - start_time:.2f},'
        f'{stats.demux_read_bytes},'
        f'{stats.demux_bitrate*8000:.6f},'
        f'{stats.demux_corrupted},'
        f'{stats.displayed_pictures},'
        f'{stats.lost_pictures},'
        f'{stats.played_abuffers},'
        f'{stats.lost_abuffers}\n'
    ))

def run(results_filename, logfilename, media_url, duration):
    results_file = init_results_file(results_filename)

    vlc_instance = vlc.Instance(
        f'-vvv --file-logging --logfile={logfilename} '
        '--vout=vdummy --aout=adummy --codec=dummy --no-sout-display-video --no-sout-display-audio '
        '--rtsp-timeout=300 --rtsp-session-timeout=300 '
        '--no-playlist-autostart --no-video-deco --quiet'
    )

    # Set up player
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(media_url)
    player.set_media(media)
    player.play()
    time.sleep(1)

    # Repeatedly run write_stat every 5 seconds, for the specified duration
    start_time = time.time()
    rt = RepeatedTimer(5, write_stat, results_file, start_time, media)
    try:
        time.sleep(int(duration) + 1)
    finally:
        rt.stop()
        results_file.close()
        sys.exit()

if __name__ == '__main__':
    run(*sys.argv[1:])
