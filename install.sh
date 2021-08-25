path=$(dirname $0)
dot_doctor="/dotdoctor.py"
symlinkpath="/usr/local/bin/dotdoctor"
ln -s $path$dot_doctor
echo $path$dot_doctor
echo
chmod +x "/usr/local/bin/dotdoctor"
