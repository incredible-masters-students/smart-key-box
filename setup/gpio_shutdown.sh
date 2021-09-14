# Create backup file
DATETIME=$(date '+%Y%m%d_%H%M%S')
TARGET_FILENAME=/boot/config.txt
BACKUP_FILENAME=/boot/config_$DATETIME.txt
sudo cp $TARGET_FILENAME $BACKUP_FILENAME

# Add shutdown settings
echo dtparam=act_led_trigger=heartbeat | sudo tee -a $TARGET_FILENAME
echo dtoverlay=gpio-shutdown,debounce=1000 | sudo tee -a $TARGET_FILENAME
