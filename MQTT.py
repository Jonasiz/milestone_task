import threading

import paho.mqtt.client as mqtt

import logger


def _on_message_callback(client, userdata, message):
    print_msg = 'Received {0} on topic: {1} with QoS {2}'.format(
        message.payload, message.topic, message.qos
    )

    client.logger.info(print_msg)


class MQTTClient(mqtt.Client):

    def __init__(self, client_id, clean_session):
        super().__init__(client_id, clean_session)

        log_file = './logs/{0}'.format(client_id + '.log')
        self.logger = logger.get_logger(client_id, log_file)
        self.enable_logger(self.logger)

        self.loop_thread = None

    def connect_client(self, host, port, keepalive):
        self.connect(host, port=port, keepalive=keepalive)
        self.on_message = _on_message_callback

        self.loop_thread = threading.Thread(target=self._loop)
        self.loop_thread.start()

        self.logger.info('Connected. Background thread is running.')

    def disconnect_client(self):
        self.disconnect()
        self.loop_thread.join(timeout=5.0)
        self.logger.info('Disconnected. Background thread stopped.')

    def publish_message(self, topic, data, qos=1):
        self.publish(topic, data, qos=qos)
        self.logger.info('Published data to topic: {0}'.format(topic))

    def subscribe_topic(self, topic, qos):
        self.subscribe(topic, qos)

    def unsubscribe_topic(self, topic):
        self.unsubscribe(topic)
        self.logger.info('Unsubscribed from topic: {0}'.format(topic))

    def _loop(self):
        self.logger.info('Looping...')
        self.loop_forever()
