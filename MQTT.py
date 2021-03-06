import threading

import paho.mqtt.client as mqtt

import logger


class MQTTClient(mqtt.Client):

    def __init__(self, client_id, clean_session, msg_handler):
        super().__init__(client_id, clean_session)

        self.client_id = client_id
        self.on_message = msg_handler

        log_file = './logs/{0}'.format(client_id + '.log')
        self.logger = logger.get_logger(client_id, log_file)
        self.enable_logger(self.logger)

        self.loop_thread = None
        self.sub_topics = []
        self.temperature = 15

    def connect(self, host, port=1883, keepalive=60, bind_address="", bind_port=0,
                clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY, properties=None):

        super().connect(host, port, keepalive, bind_address, bind_port, clean_start, properties)

        self.loop_thread = threading.Thread(target=self._loop)
        self.loop_thread.start()

        self.logger.info('Connected. Background thread is running.')

    def disconnect(self, reasoncode=None, properties=None):
        super().disconnect(reasoncode, properties)

        if self.loop_thread is not None:
            self.loop_thread.join(timeout=3)
            self.logger.info('Disconnected. Background thread stopped.')

    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        super().publish(topic, payload, qos, retain, properties)
        self.logger.info('Published data to topic: {0}'.format(topic))

    def subscribe(self, topic, qos=0, options=None, properties=None):
        super().subscribe(topic, qos, options, properties)
        self.sub_topics.append(topic)
        self.logger.info('Subscribed to topic: {0}'.format(topic))

    def unsubscribe(self, topic, properties=None):
        super().unsubscribe(topic, properties)
        self.sub_topics.remove(topic)
        self.logger.info('Unsubscribed from topic: {0}'.format(topic))

    def _loop(self):
        self.logger.info('Looping...')
        self.loop_forever()
        self.logger.info('Looping finished')
