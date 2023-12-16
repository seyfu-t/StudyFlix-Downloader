import requests
from bs4 import BeautifulSoup
import subprocess
import argparse
import sys
import os

# Audio:        ffmpeg -analyzeduration 100M -probesize 100M -i "https://ducsmxsiuk0zw.cloudfront.net/video_1325/1142/1142.m3u8" -vn -ar 48000 -ac 2 -c:a copy audio.aac
# Video:        ffmpeg -i "https://ducsmxsiuk0zw.cloudfront.net/video_1325/1142/1142.m3u8" -an -c:v copy video.mp4
# Combining:    ffmpeg -i video.mp4 -i audio.aac -c:v copy -c:a copy -shortest output.mp4


def download_video(url, m3u8_selector, title_selector):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    m3u8_url = soup.select_one(m3u8_selector)['content']
    title = soup.select_one(title_selector).text.strip().replace(' ', '_')

    #ffmpeg_command = [
    #    'ffmpeg',
    #    '-http_proxy', 'socks5://localhost:25344',  # Uncomment to use a proxy
    #    '-i', m3u8_url,
    #    '-c', 'copy',
    #    f'{title}.mp4'
    #]

    ffmpeg_audio=[
        "ffmpeg",
        "-y",
        "-analyzeduration","100M",
        "-probesize","100M",
        "-i",m3u8_url,
        "-vn",
        "-ar","48000",
        "-ac","2",
        "-c:a","copy",
        "cache/"+title+".aac"
    ]
    ffmpeg_video=[
        "ffmpeg",
        "-y",
        "-i",m3u8_url,
        "-an",
        "-c:v","copy",
        "cache/"+title+".mp4"
    ]
    ffmpeg_combine=[
        "ffmpeg",
        "-y",
        "-i","cache/"+title+".mp4",
        "-i","cache/"+title+".aac",
        "-c:v","copy",
        "-c:a","copy",
        "-shortest",
        "final/"+title+".mp4"
    ]
    if not os.path.exists("./cache"):
        os.makedirs("./cache")
    if not os.path.exists("./final"):
        os.makedirs("./final")

    print(ffmpeg_audio)
    print(ffmpeg_video)
    print(ffmpeg_combine)

    subprocess.run(ffmpeg_audio)
    subprocess.run(ffmpeg_video)
    subprocess.run(ffmpeg_combine)


def process_file(file_path, m3u8_selector, title_selector):
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            if url:
                download_video(url, m3u8_selector, title_selector)


def main():
    parser = argparse.ArgumentParser(description='Download videos from URLs.')
    parser.add_argument('--file', '-f', type=str,
                        help='Path to a file with URLs, one per line.')
    parser.add_argument('urls', nargs='*', help='Direct URL input')

    args = parser.parse_args()

    m3u8_sel = 'meta[itemprop="contentUrl"]'
    title_sel = "h1.h2"

    if args.file:
        process_file(args.file, m3u8_sel, title_sel)

    for url in args.urls:
        download_video(url, m3u8_sel, title_sel)


if __name__ == '__main__':
    main()
