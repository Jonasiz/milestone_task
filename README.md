## MQTT interview task

Developed on python 3.8.5

#### Requirements:

    pip install paho-mqtt
    pip install PyInquirer
    pip install python-dotenv

Create an `.env` file and fill in your public MQTT broker details. Use 
`.dummy.env` for reference.

#### Usage:
`python3 main.py` or `python3 main.py --mode interactive` 
to launch in interactive CLI mode

`python3 main.py --mode plain` to launch a simple interaction 
demo between two MQTT clients

The client outputs are logged in the `log` directory. 
Each `*.log` file is named after the client ID of its corresponding MQTT client.  
