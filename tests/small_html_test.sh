#!/bin/sh

test_url=https://getlantern.org/en_US/index.html
opath_1=./test_file
opath_2=./test_file_curl

curl --ipv4 -o $opath_2 $test_url # > /dev/null 2>&1
python ms_downloader.py --url $test_url --outfile-path $opath_1

cmp $opath_1 $opath_2

rm $opath_1
rm $opath_2
