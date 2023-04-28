import os
import requests
import m3u8
import subprocess
import imageio_ffmpeg as ffmpeg
import shutil

name = 'NAME OF VIDEO'

## CREATE PATH FOR FINAL FILE ##
destination_folder = r'DESTINATION FOLDER'
extension = '.mp4'
export_file = name + extension

## STORE MANIFEST URL COMPONENTS ## ----- F12 -> network -> refresh page -> copy link address of 1080p .mp3u8 file
url_manifest = 'URL OF MANIFEST FILE'
url_base = url_manifest.split('/')[0:-1]
url_base = '/'.join(url_base) + '/'

## RETRIEVE PLAYLIST OF TS FILES ##
r = requests.get(url_manifest)
playlist = m3u8.loads(r.text)

## DOWNLOAD AND CONCATENATE TS FILES ##
with open("video.ts", 'wb') as f:
    for segment in playlist.data['segments']:
        url_ts = url_base + segment['uri']
        r = requests.get(url_ts)
        f.write(r.content)

## CONVERT TO MP4 ##
ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
subprocess.run([ffmpeg_exe, '-i', 'video.ts', '-c', 'copy', name + extension])

## MOVE FILE TO DESTINATION FOLDER ##
shutil.move(export_file, destination_folder + '/' + export_file)

## DELETE TS FILE ##
os.remove('video.ts')
