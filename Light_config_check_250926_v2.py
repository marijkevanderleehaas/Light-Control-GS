import json
import websocket
import time
import ssl
import logging
import LightControl_250925_v4
from SendEmail_250924_v1 import SendEmail

CONFIG_FILE = "light_gs_config.json"
LOG_FILE_config = "config_check.log"
IP = "10.73.178.242"
PORT = 27950
ws_url = f"wss://{IP}:{PORT}"

# Setup logging
logging.basicConfig(
    level=logging.INFO,  # log INFO and above
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_config, encoding="utf-8"),
        logging.StreamHandler()  # also print to console
    ]
)

def load_message():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"{CONFIG_FILE} not found — starting fresh.")
        return None

count = 0
def listen_and_check(ws_url, retry_delay):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    was_connected = False
    disconnect_reported = False
    while True:
        connection_lost = False
        
        try:
            logging.info(f"Trying to connect to {ws_url}")
            ws = websocket.create_connection(
                ws_url,
                sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})
            
            if not was_connected:
                logging.info("Connected successfully")
                subject = "Raspberry: Checkpoint: config check has connection"
                body = f"Connected successfully"
                SendEmail(subject, body)
            was_connected = True
            disconnect_reported = False

            stored_message = json.dumps(load_message(), sort_keys = True)

            while True:
                try:
                    response = ws.recv()
                    new_message = json.dumps(response, sort_keys = True)

                    #logging.info(f"Received message: {new_message}")

                    if stored_message:
                        if new_message[:50] != stored_message[:50]:
                            #logging.info("Identifier does not match — ignoring message.")
                            continue  # go back to start of loop

                        if new_message != stored_message:
                            LightControl_250925_v4.apply_light_settings()
                            print("Messages are different")
                            logging.warning("Messages differ — resending settings.")
                            logging.info(f"Stored message: {stored_message}")
                            logging.info(f"New message:    {new_message}")

                        else:
                            #logging.info("Messages matched - waiting on next message")
                            connection_lost = False
                            continue
                except websocket.WebSocketConnectionClosedException:
                    logging.error("WebSocket closed unexpectedly. Reconnecting...")
                    logging.warning(f"Connection failed: {e}. Retrying in {retry_delay} seconds...")
                    subject = "Raspberry: Err: WebSocket closed unexpectedly"
                    body = f"Connection failed: WebSocket closed unexpectedly"
                    SendEmail(subject, body)
                    was_connected = False
                    connection_lost = True
                    break
                except Exception as e:
                    logging.error(f"Error: {e}")
                    connection_lost = True
                    as_connected = False
                    break
                print("sleeping for 0.1 seconds")
                time.sleep(0.1)  # Avoid busy loop
                
        except Exception as e:
            if not disconnect_reported:
                logging.warning(f"Connection failed: {e}. Retrying in {retry_delay} seconds...")
                subject = "Raspberry: Err: Connection failed"
                body = f"Connection failed: {e}"
                SendEmail(subject, body)
                disconnect_reported = True
                time.sleep(retry_delay)
            
            logging.warning(f"Connection failed: {e}. Retrying in {retry_delay} seconds...")
            connection_lost = True
        if connection_lost:
            time.sleep(0.1)
        else:
            print("End of outer loop, sleeping for 5 seconds")
            time.sleep(5)
                


print(listen_and_check(ws_url, 30))

#if __name__ == "__main__":
    #listen_and_check()

    #cron job : 2 8 * * * pkill -f /media/RASPi_OGRE/MarijkePhDData/WP3/Light_config_check_250525_v1.py; cd /media/RASPi_OGRE/MarijkePhDData/WP3 && /usr/bin/python3.11 Light_config_check_250525_v1.py >> /media/RASPi_OGRE/MarijkePhDData/WP3/config_check.log 2>&1