path=$(dirname $0)
dot_doctor="/dotdoctor.py"
ln -s $path$dot_doctor "/usr/local/bin/dotdoctor"
chmod +x "/usr/local/bin/dotdoctor"
