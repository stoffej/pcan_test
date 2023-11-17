from PCANBasic import *
import threading
import time

# Function to be called when a new message is received
def on_message_received(msg, timestamp):
    # id = msg.DATA[0]
    # if id == 0x0
    print("Data:" + str(msg.DATA[0]))

# Thread function for continuously checking for new messages
def read_messages(pcan, callback):
    while True:
        result, msg, timestamp = pcan.Read(PCAN_USBBUS1)
        if result == PCAN_ERROR_OK:
            callback(msg, timestamp)
        time.sleep(0.01)  # To prevent high CPU usage


# Function to send a message
def send_message(pcan, message):
    result = pcan.Write(PCAN_USBBUS1, message)
    if result != PCAN_ERROR_OK:
        print("Failed to send message:", pcan.GetErrorText(result))
    else:
        print("Message sent")
        
# Create an instance of the PCANBasic class
pcan = PCANBasic()

# Initialize a PCAN channel
result = pcan.Initialize(PCAN_USBBUS1, PCAN_BAUD_250K)

if result != PCAN_ERROR_OK:
    print("Initialization failed:", pcan.GetErrorText(result))
else:
    print("Initialized PCAN USB channel")

    # Start the read thread
    read_thread = threading.Thread(target=read_messages, args=(pcan, on_message_received))
    read_thread.start()

    try:
        # Main loop
        while True:
            # Prepare a message to send
            message = TPCANMsg()
            message.ID = 0x123  # Example CAN ID
            message.MSGTYPE = PCAN_MESSAGE_STANDARD
            message.LEN = 2  # Number of data bytes
            message.DATA = (0x11, 0x22)  # Data to be sent

            # Send the message
            send_message(pcan, message)

            # Wait for a second
            time.sleep(1)

            # Main thread can perform other tasks or simply sleep
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping program")

    # Stop the read thread
    read_thread.join()

    # Uninitialize the channel
    pcan.Uninitialize(PCAN_USBBUS1)
