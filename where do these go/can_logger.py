
import can
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="/var/log/can_logger.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def setup_can_interface(channel="can0", bitrate=500000):
    # Modify channel or bitrate as needed for your hardware
    return can.interface.Bus(channel=channel, bustype='socketcan')

def main():
    print("Starting CAN logger...")
    bus = setup_can_interface()

    # Optional: add CAN ID filters here
    # Example: [{'can_id': 0x7E8, 'can_mask': 0x7FF}]
    filters = []  # Leave empty to log all messages
    if filters:
        bus.set_filters(filters)

    try:
        while True:
            msg = bus.recv()
            if msg:
                log_line = f"ID: {hex(msg.arbitration_id)} DLC: {msg.dlc} Data: {' '.join(f'{b:02X}' for b in msg.data)}"
                logging.info(log_line)
    except KeyboardInterrupt:
        print("CAN logger stopped by user.")
    except Exception as e:
        logging.error(f"CAN logger error: {e}")

if __name__ == "__main__":
    main()
