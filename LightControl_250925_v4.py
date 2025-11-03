#!/usr/bin/env python3
import json
import datetime
import logging
from pathlib import Path
import schedule
import time
import ssl
import websocket
from SendEmail_250924_v1 import SendEmail

SETTINGS_DIR = Path("light_settings")
CURRENT_FILE = Path("current.json")
CONFIG_FILE = Path("light_gs_config.json")
LOG_FILE = "light_settings.log"


IP = "10.73.178.242"
PORT = 27950
ws_url = f"wss://{IP}:{PORT}"
retry_delay = 30  # send every 30 seconds

logging.basicConfig(
    level=logging.INFO,  # log INFO and above
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # also print to console
    ]
)

def save_current_settings(settings):
    with open("current.json", "w") as f:
        json.dump(settings, f)
    logging.info("Saved settings to current.json")

def save_config(message):
    with open(CONFIG_FILE, "w") as f:
        json.dump(message, f, indent =2)

def load_settings_for_today():
    today = datetime.datetime.now().strftime("%y%m%d")
    
    file_path = SETTINGS_DIR / f"light_{today}.json"

    if not file_path.exists():
        print(f"No settings file for today: {file_path}")
        logging.warning(f"No settings file for today: {file_path}")
        subject = "Raspberry: Err: No settings file for today"
        body = "No settings file was found for today"
        SendEmail(subject, body)
        return None, today

    try:
        with open(file_path, "r") as f:
            settings = json.load(f)
        save_current_settings(settings)
        logging.info(f"Loaded today's settings from {file_path}")
        with open("last_loaded_day.txt", "w") as f:
            f.write(str(today))
        subject = "Raspberry: Checkpoint: new file was loaded"
        body = f"File with correct settings for {today} was loaded"
        SendEmail(subject, body)
        return settings, today
    except Exception as e:
        print(f"Failed to load settings: {e}")
        logging.error(f"Failed to load {file_path}: {e}")
        return None, today

def send_message(ws_url, message, retry_delay):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    count = 0
    
    while True:
        try:
            logging.info(f"Trying to connect to {ws_url}")
            ws = websocket.create_connection(
                ws_url,
                sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False}
            )
            logging.info("Connected successfully")

            ws.send(json.dumps(message))
            logging.info(f"Message sent: {message}")

            # Optional: receive a single response
            try:
                response = ws.recv()
                save_config(response)
                logging.info(f"Received response: {response}")
            except websocket.WebSocketTimeoutException:
                logging.warning("No response received from server")
            except Exception as e:
                    logging.error(f"Error: {e}")

            ws.close()
            subject = "Raspberry: Checkpoint: settings were loaded to system"
            body = "Settings were loaded into system"
            SendEmail(subject, body)
            logging.info("Connection closed")
            break  # exit loop after success
        
        except Exception as e:
            if count != 0:
                logging.warning(f"Connection failed: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.warning(f"Connection failed: {e}. Retrying in {retry_delay} seconds...")
                subject = "Raspberry: Err: Connection failed"
                body = f"Connection failed: {e}"
                SendEmail(subject, body)
                count += 1
                time.sleep(retry_delay)
        return response


def apply_light_settings():
    if not CURRENT_FILE.exists():
        logging.warning("No current.json available. Nothing to apply.")
        return None

    try:
        with open(CURRENT_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        with open("last_loaded_day.txt", "r") as f:
            Last_day = f.read().strip()
        logging.info(f"Opening settings for {Last_day}")
        print(f"Opening settings for {Last_day}:", settings)
        send_message(ws_url, settings, retry_delay)
        return settings
    except Exception as e:
        logging.error(f"Failed to apply settings from {CURRENT_FILE}: {e}")
        return None


def start_light_check_sequence():
    """
    Apply the light and start checks:
    - Every 10 minutes for 1 hour
    - Then every hour until next scheduled day
    """
    load_settings_for_today()
    apply_light_settings()


start_light_check_sequence()
# --- Start ---
#if __name__ == "__main__":
#    start_light_check_sequence()
