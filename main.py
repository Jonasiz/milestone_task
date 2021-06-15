import json
import os
import random
import time

from dotenv import load_dotenv
from MQTT import MQTTClient


def main():
    load_dotenv()
    broker_domain = str(os.getenv('BROKER_HOST'))
    broker_port = int(os.getenv('BROKER_PORT'))

    living_room_sensor = 'interview/ioma/sensors/temperature/living_room/ABC1'
    freezer_sensor = 'interview/ioma/sensors/temperature/freezer/CBA1'

    # Freezer client/sensor
    freezer_client = MQTTClient('client_a_unique_id', clean_session=True)
    freezer_client.connect(broker_domain, port=broker_port, keepalive=120)
    freezer_client.subscribe(living_room_sensor, qos=1)

    # Living room client/sensor
    living_room_client = MQTTClient('client_b_unique_id', clean_session=True)
    living_room_client.connect(broker_domain, port=broker_port, keepalive=60)
    living_room_client.subscribe(freezer_sensor, qos=1)

    print('Both clients started! Check log files')

    try:
        while True:
            freezer_client.publish(
                freezer_sensor,
                json.dumps({'freezer_temp': random.randint(-40, -20)})
            )
            time.sleep(1)

            living_room_client.publish(
                living_room_sensor,
                json.dumps({'living_room_temp': random.randint(5, 30)})
            )
            time.sleep(1)

    except KeyboardInterrupt:
        freezer_client.disconnect()
        living_room_client.disconnect()
        print('Interrupted, exiting...')


if __name__ == '__main__':
    main()
