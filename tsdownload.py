""" download segmented mpeg video (.ts files) from streaming websites """
import sys
import os
import requests

REFERER = ""

OUTNAME = 'video.ts'  # default output file name
LOC = ""  # default save location

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": REFERER,
    "DNT": "1",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}


def getSegs(m3):
    """ figure out how many segments there are using the m3u8 file """
    lines = m3.text.split('\n')
    segments = []
    for line in lines:
        if '.ts' in line:
            segments.append(line)
    return segments


def dumpSegs(initUrl, segments, path, append=False):
    """ downlaod and combine the .ts files
    given the first seg's url, the number of segments and
    the destination download path """
    with open(path, 'ab' if append else 'wb') as f:
        for segment in segments:
            segurl = initUrl + '/' + segment
            success = False
            while not success:
                try:
                    seg = requests.get(segurl, headers=HEADERS)
                    success = True
                except:
                    print('retrying...')
            f.write(seg.content)


if __name__ == "__main__":
    DEST = LOC + OUTNAME
    SOURCE = sys.argv[1]
    if len(sys.argv) > 2:
        DEST = sys.argv[2]
    # validate destination:
    delim = ''
    if '\\' in DEST:
        delim = '\\'
    elif '/' in DEST:
        delim = '/'
    if delim:
        PATH = ''.join(DEST.split(delim)[:-1])
        if not os.path.isdir(PATH):
            print('INAVLID DESTINATION.')
            sys.exit(0)
    m3u8 = requests.get(SOURCE, headers=HEADERS)
    segments = getSegs(m3u8)
    url = '/'.join(SOURCE.split('/')[:-1])
    dumpSegs(url, segments, DEST)
