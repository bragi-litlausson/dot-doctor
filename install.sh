#!/usr/bin/env sh
path=$(dirname $0)
dot_doctor="/dotdoctor.py"
symlinkpath="/usr/local/bin/dotdoctor"
echo "$path $dot_doctor"
echo "$symlinkpath"
ln -s $path$dot_doctor $symlinkpath
chmod +x "/usr/local/bin/dotdoctor"
