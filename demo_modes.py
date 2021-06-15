import json
import os
import random
import time

from dotenv import load_dotenv

from ClientManager import ClientManager
from MQTT import MQTTClient
import console_prompts


def freezer_callback(client, userdata, message):
    print_msg = 'Received {0} on topic: {1} with QoS {2}'.format(
        message.payload, message.topic, message.qos
    )

    client.logger.info(print_msg)

    living_room_temp = json.loads(message.payload)['temp']
    client.temperature = living_room_temp - 30
    client.logger.info('Updated freezer temperature to {0} C (living room temp: {1})'.format(
        client.temperature, living_room_temp
    ))


def living_room_callback(client, userdata, message):
    print_msg = 'Received {0} on topic: {1} with QoS {2}'.format(
        message.payload, message.topic, message.qos
    )

    client.logger.info(print_msg)

    freezer_temp = json.loads(message.payload)['temp']
    client.temperature = freezer_temp + 30
    client.logger.info('Updated living room temperature to {0} C (freezer temp: {1})'.format(
        client.temperature, freezer_temp
    ))


def main():
    load_dotenv()
    broker_domain = str(os.getenv('BROKER_HOST'))
    broker_port = int(os.getenv('BROKER_PORT'))

    living_room_sensor = 'interview/ioma/sensors/temperature/living_room/ABC1'
    freezer_sensor = 'interview/ioma/sensors/temperature/freezer/CBA1'

    # Freezer client/sensor
    freezer_client = MQTTClient('freezer_id', clean_session=True,
                                msg_handler=freezer_callback)
    freezer_client.connect(broker_domain, port=broker_port, keepalive=120)
    freezer_client.subscribe(living_room_sensor, qos=1)

    # Living room client/sensor
    living_room_client = MQTTClient('living_room_id', clean_session=True,
                                    msg_handler=living_room_callback)
    living_room_client.connect(broker_domain, port=broker_port, keepalive=60)
    living_room_client.subscribe(freezer_sensor, qos=1)

    print('Both clients started! Check log files')

    try:
        while True:
            # Fluctuate freezer temperature
            freezer_temp = freezer_client.temperature + random.randint(-5, 5)
            freezer_client.publish(freezer_sensor,
                                   json.dumps({'temp': freezer_temp}),
                                   qos=1)
            time.sleep(random.randint(1, 2))

            # Fluctuate living room temperature
            living_room_temp = living_room_client.temperature + random.randint(-5, 5)
            living_room_client.publish(living_room_sensor,
                                       json.dumps({'temp': living_room_temp}),
                                       qos=1)
            time.sleep(random.randint(1, 2))

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
                unsub_id = console_prompts.unsubscribe_client_id(client_ids)

                client = [client for client in client_manager.clients
                          if client.client_id == unsub_id][0]

                unsub_topic = console_prompts.unsubscribe_client_topic(client)

                if unsub_topic is not None:
                    client_manager.client_unsubscribe(client.client_id, unsub_topic)

                    print('Unsubscribed client "{0}" from topic "{1}"'.format(
                        unsub_id, unsub_topic
                    ))
    except (EOFError, KeyError):
        print('Interrupted, exiting...')
        client_manager.disconnect_all()
        print('Done.')
