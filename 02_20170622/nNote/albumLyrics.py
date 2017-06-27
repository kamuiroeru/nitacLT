# coding: utf-8
from bs4 import BeautifulSoup
import requests
from getLyrics import getTouhouLyrics
from urllib.parse import urljoin

def procedure(title, urlAlbum):
    songname = title.text
    print('processing: ' + songname)
    lyricURL = urljoin(urlAlbum, title.get('href'))
    lyric = getTouhouLyrics(lyricURL)
    if lyric:
        open(songname + '.txt', 'w').write(lyric)

def getLyricsInAlbum(urlAlbum):
    r = requests.get(urlAlbum)
    albumName = urlAlbum.split('/')[-1]

    # 3回まで再試行
    if r.status_code != 200:
        i = 0
        while r.status_code != 200:
            sleep(0.5)
            r = requests.get(touhouWikiURL)
            i += 1
            if i >= 3:
                print('3回試行しましたが取得できませんでした。')
                exit(1)

    import os
    os.makedirs(albumName, exist_ok=True)
    os.chdir(albumName)

    soup = BeautifulSoup(r.content, 'html.parser')
    soup.select('a[title^="Lyrics"]')  # 前方一致
    titles = soup.select('a[title^="Lyrics"]')

    # 無限に s を作るジェネレータ
    def genString(s):
        while 1:
            yield s

    from multiprocessing import Pool
    with Pool() as p:
        p.starmap(procedure, zip(titles, genString(urlAlbum)))
    # for title in titles:
    #     songname = title.text
    #     print('processing: ' + songname)
    #     lyricURL = urljoin(urlAlbum, title.get('href'))
    #     lyric = getTouhouLyrics(lyricURL)
    #     if lyric:
    #         open(songname + '.txt', 'w').write(lyric)

if __name__ == '__main__':
    from sys import argv
    getLyricsInAlbum(argv[1])
