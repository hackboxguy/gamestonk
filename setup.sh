#!/bin/sh
#./setup.sh
USAGE="usage:sudo $0 "

if [ $(id -u) -ne 0 ]; then
	echo "Please run setup as root ==> sudo ./setup.sh"
	exit
fi

printf "Installing finnhub modules............................ "
pip -q install finnhub-python
test 0 -eq $? && echo "[OK]" || echo "[FAIL]"

printf "Installing tkinter module............................. "
apt-get install python3-tk
DEBIAN_FRONTEND=noninteractive apt-get install -qq python3-tk < /dev/null > /dev/null
git clone --quiet https://github.com/markbrody/tkinter-quotes.git /home/pi/gamestonk/tkinter-quotes > /dev/null
cd /home/pi/gamestonk/tkinter-quotes
python3 -m pip install -q -r requirements.txt --user
test 0 -eq $? && echo "[OK]" || echo "[FAIL]"

printf "Enabling ssh server .................................. "
systemctl enable ssh 1>/dev/null 2>/dev/null
systemctl start ssh 1>/dev/null 2>/dev/null
test 0 -eq $? && echo "[OK]" || echo "[FAIL]"

printf "Customizing rc.local ................................... "
cp /home/pi/gamestonk/rc.local /etc/
test 0 -eq $? && echo "[OK]" || echo "[FAIL]"

printf "Installing lcd module driver.......................... "
git clone --quiet https://github.com/waveshare/LCD-show.git /home/pi/gamestonk/LCD-show > /dev/null
cd /home/pi/gamestonk/LCD-show
chmod +x LCD35-show
#./LCD35-show 180
test 0 -eq $? && echo "[OK]" || echo "[FAIL]"
