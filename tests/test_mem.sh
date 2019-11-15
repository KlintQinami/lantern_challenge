# Get maximum resident set size in bytes of python process when downloading
# 100mb. Should be less than 100mb.

/usr/bin/time -l python ms_downloader.py --url http://212.183.159.230/100MB.zip --outfile-path ./testmem.html --chunk-size 2000000

