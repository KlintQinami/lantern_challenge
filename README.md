# Multi-Source Downloader
The downloader attempts to download a file in chunks using a multi-threaded, parallel implementation in Python.

Example usage:

python ms_downloader.py --url https://getlantern.org/en_US/index.html --outfile-path index.html --chunk-size 8912 --nthreads 2 --verify-with-md5

optional arguments:

  -h, --help            show this help message and exit

  --url URL             URL of the file to download.

  --nthreads NTHREADS   Number of threads used to download file.

  --chunk-size CHUNK_SIZE
                        Size in bytes to use for requesting file chunks.

  --outfile-path OUTFILE_PATH
                        Path where to save file. Directory will also be used
                        to store intermediate chunks. Please ensure no name
                        conflicts.

  --verify-with-md5     Compute an md5 hash of the downloaded file and compare
                        against etag.

