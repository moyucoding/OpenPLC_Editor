#!/bin/bash
echo "Installing OpenPLC Editor"
echo "Please be patient. This may take a couple minutes..."
echo ""
echo "[INSTALLING DEPENDENCIES]"
sudo apt-get -y -qq update
#Main packages
sudo apt-get -y -qq install curl build-essential pkg-config bison flex autoconf automake libtool make git libssl-dev python-wxgtk3.0
#Python 2. Some distros call it python2, some others call it python2.7. Try instaling both
sudo apt-get -y -qq install python2
sudo apt-get -y -qq install python2.7
#For Python sslpsk
sudo apt-get -y -qq install libssl-dev
#For Python lxml
sudo apt-get -y -qq install libxml2-dev libxslt1-dev
#Fixes python.h include issues
sudo apt-get -y -qq install python2-dev
sudo apt-get -y -qq install python2.7-dev
#Get pip manually
curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
sudo python2.7 get-pip.py
#Fix for Debian Buster
sudo apt-get -y -qq install libpng libfreetype6-dev
pip2 install future zeroconf==0.19.1 numpy==1.16.5 matplotlib==2.0.2 lxml pyro sslpsk -i https://mirrors.aliyun.com/pypi/simple
echo ""
echo "[COMPILING MATIEC]"
cd matiec
autoreconf -i
./configure
make -s
echo ""
echo "[FINALIZING]"
cd ..
WORKING_DIR=$(pwd)
echo -e "#!/bin/bash\n\
cd \"$WORKING_DIR/editor\"\n\
python2.7 Beremiz.py" > openplc_editor.sh
chmod +x ./openplc_editor.sh
cd ~/.local/share/applications
echo -e "[Desktop Entry]\n\
Name=OpenPLC Editor v1.0\n\
Exec=\"$WORKING_DIR/openplc_editor.sh\"\n\
Icon=\"$WORKING_DIR/editor/images/brz.ico\"\n\
Type=Application\n\
Terminal=false" > OpenPLC_Editor.desktop
