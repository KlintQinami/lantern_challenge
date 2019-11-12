import os
import sys
import threading
import urllib
import requests
import shutil

from utils import argparser, verify_with_etag


def single_stream_download(url, buffersize, filename):
    with urllib.request.urlopen(url) as r, open(filename, 'wb') as outfile:
        shutil.copyfileobj(r, outfile, buffersize)


def download_chunks(thread_idx, url, nthreads, chunk_size, outfile):
    start_byte = thread_idx*chunk_size

    try:
        while True:
            end_byte = start_byte+chunk_size - 1

            req = urllib.request.Request(url)
            req.headers['Range'] = 'bytes={}-{}'.format(start_byte, end_byte)
            resp = urllib.request.urlopen(req).read()

            with open('{}_{}'.format(outfile, start_byte), 'wb+') as f:
                f.write(resp)

            start_byte += nthreads*chunk_size

    except urllib.error.HTTPError as e:
        # Since we do not assume knowledge of the file size, we terminate when
        # we receive the error HTTP Error 416: Requested Range Not Satisfiable.
        # This occurs when the beginning of the byte range requested is beyond
        # the size of the file.
        if e.code == 416:
            return
        else:
            print('Bad error code received. Expected HTTP Error 416.')
            sys.exit()


def combine_chunks(chunk_size, outfile):
    start_byte = 0

    if os.path.exists(outfile):
        os.remove(outfile)

    out = open(outfile, 'ab')

    chunk_path = '{}_{}'.format(outfile, start_byte)
    while os.path.exists(chunk_path):
        chunk_file = open(chunk_path, 'rb')
        shutil.copyfileobj(chunk_file, out)
        chunk_file.close()
        os.remove(chunk_path)

        start_byte += chunk_size
        chunk_path = '{}_{}'.format(outfile, start_byte)

    out.close()


def multi_stream_download(url, nthreads, chunk_size, outfile):
    downloaders = [
        threading.Thread(
            target=download_chunks,
            args=(idx, url, nthreads, chunk_size, outfile),
        )
        for idx in range(nthreads)
    ]

    for th in downloaders:
        th.start()

    for th in downloaders:
        th.join()

    combine_chunks(chunk_size, outfile)


def handle_request(url, nthreads, chunk_size, outfile, verify):
    try:
        request = urllib.request.Request(url, method='HEAD')
        response = urllib.request.urlopen(request)
        response.close()
    except Exception as e:
        print(e)
        sys.exit()

    etag = response.headers['Etag'][1:-1]

    if not response.headers['Accept-Ranges'] == 'bytes':
        # Revert to single stream downloading if the server doesn't support
        # byte range requests.
        print('Server does not accept byte range requests. Reverting to a '
              'single stream download.')
        single_stream_download(url, chunk_size, outfile)
    else:
        multi_stream_download(url, nthreads, chunk_size, outfile)

    if verify:
        verify_with_etag(etag, outfile)


if __name__ == '__main__':
    # TODO:
    # Profile memory usage
    # Check if compressed files work
    # Check if chunked target encoding and other target encodings work
    # chunked_url = "https://www.httpwatch.com/httpgallery/chunked/chunkedimage.aspx"
    # Pick a decent big file as the default URL
    # Verify by comparing files with what curl grabs, automated script would be
    # nice

    args = argparser()

    handle_request(
        args.url,
        args.nthreads,
        args.chunk_size,
        args.outfile_path,
        args.verify_with_md5
    )

