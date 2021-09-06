# Key and Rpi

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

Create `slack_bot_token.py`.

```python:slack_bot_token.py
SLACK_BOT_TOKEN = "hoge"
CHANNEL_ID = "foo"
```

### Setup service

Create `key_and_rpi.service`.

```bash:create_key_and_rpi.service
python3 create_service_file.py && \
sudo cp key_and_rpi.service /lib/systemd/system/
```

Run command as follows.

```bash:setup-service
sudo systemctl start key_and_rpi.service  # Start service
sudo systemctl stop key_and_rpi.service　 # Stop service
sudo systemctl enable key_and_rpi.service   # Enable service start at boot
sudo systemctl disable key_and_rpi.service　 # Disable service start at boot
```
