#!/bin/sh

test_url=http://212.183.159.230/20MB.zip
opath_1=./test_file
opath_2=./test_file_curl

python ms_downloader.py --url $test_url --outfile-path $opath_1 --chunk-size 1000000
curl -o $opath_2 $test_url > /dev/null 2>&1

cmp $opath_1 $opath_2

rm $opath_1
rm $opath_2
