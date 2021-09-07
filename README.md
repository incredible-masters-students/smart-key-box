# Smart Key Box

## Preparation

### Install Additional Packages

Run command as follows.

```bash:installation
sudo apt install python3-gpiozero && \
python3 -m venv .env && \
source .env/bin/activate && \
pip install -r requirements.txt
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
sudo systemctl start key_and_rpi.service  # Start service
sudo systemctl stop key_and_rpi.service　 # Stop service
sudo systemctl enable key_and_rpi.service   # Enable service start at boot
sudo systemctl disable key_and_rpi.service　 # Disable service start at boot
```
