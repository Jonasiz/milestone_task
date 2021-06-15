import json
import os
import random
import time

from dotenv import load_dotenv

from ClientManager import ClientManager
from MQTT import MQTTClient
import console_prompts


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


def main_interactive():
    load_dotenv()
    broker_domain = str(os.getenv('BROKER_HOST'))
    broker_port = int(os.getenv('BROKER_PORT'))
    client_manager = ClientManager()

    try:
        while True:
            client_ids = [client.client_id for client in client_manager.clients]
            choice = console_prompts.main_menu()

            if choice == console_prompts.main_actions['show']:
                console_prompts.show_clients(client_ids)
            elif choice == console_prompts.main_actions['add']:
                inputs = console_prompts.add_client(client_ids, broker_domain, broker_port)

                client_manager.add_client(inputs['client_id'],
                                          inputs['host'],
                                          int(inputs['port']),
                                          int(inputs['keepalive']),
                                          inputs['clean_session'] == 'y')

                print('Client added and connected.')
            elif choice == console_prompts.main_actions['remove']:
                removed_id = console_prompts.remove_client(client_ids)

                if removed_id is not None:
                    client_manager.remove_client(removed_id)
                    print('Client removed and disconnected.')

            elif choice == console_prompts.main_actions['pub']:
                inputs = console_prompts.publish(client_ids)

                if inputs is not None:
                    client_manager.client_publish(inputs['pub_id'],
                                                  inputs['topic'],
                                                  inputs['data'],
                                                  int(inputs['qos']))

                    print('Published "{0}" to topic {1} for client "{2}" (qos={3})'.format(
                        inputs['data'], inputs['topic'],
                        inputs['pub_id'], inputs['qos']
                    ))
            elif choice == console_prompts.main_actions['sub']:
                inputs = console_prompts.subscribe_client(client_ids)

                if inputs is not None:
                    client_manager.client_subscribe(inputs['sub_id'],
                                                    inputs['topic'],
                                                    int(inputs['qos']))

                    print('Subscribed client "{0}" to topic "{1}" (QoS: {2})'.format(
                        inputs['sub_id'], inputs['topic'], inputs['qos']
                    ))
            elif choice == console_prompts.main_actions['unsub']:
                console_prompts.unsubscribe_client()

    except EOFError:
        client_manager.disconnect_all()
        print('Interrupted, exiting...')


if __name__ == '__main__':
    main_interactive()
