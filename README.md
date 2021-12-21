# Smart Key Box

## Environment

### Raspberry Pi OS

```bash:env-raspberry-pi-os
$ cat /etc/os-release
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
NAME="Raspbian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
```

### Python

```bash:env-python
$ python3 --version
Python 3.7.3
```

## Preparation

### Install Additional Packages

Run command as follows.

```bash:installation
sudo apt install python3-gpiozero && \
python3 -m venv .env && \
source .env/bin/activate && \
.env/bin/pip install -U pip
.env/bin/pip install -r requirements.txt
```

### Save Slack Token and Channel ID

Create `settings.cfg` from `settings.org.cfg`.

```ini:settings.cfg
[SLACK]
SLACK_BOT_TOKEN = <Your Slack Bot Token>
CHANNEL_ID = <Your Channel ID>
```

### Setup service

Create `key_and_rpi.service`.

```bash:create_key_and_rpi.service
python3 setup/create_service_file.py && \
sudo cp setup/smart_key_box.service /lib/systemd/system/
```

Run command as follows.

```bash:setup-service
sudo systemctl start smart_key_box.service  # Start service
sudo systemctl stop smart_key_box.service  # Stop service
sudo systemctl enable smart_key_box.service   # Enable service start at boot
sudo systemctl disable smart_key_box.service  # Disable service start at boot
```
