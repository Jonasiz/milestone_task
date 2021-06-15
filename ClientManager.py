import MQTT


def msg_handler(client, userdata, message):
    print_msg = 'Received {0} on topic: {1} with QoS {2}'.format(
        message.payload, message.topic, message.qos
    )

    client.logger.info(print_msg)


class ClientManager:
    """ Keeps track of MQTT clients and conducts operations on them """

    def __init__(self):
        self.clients = []

    def add_client(self, client_id, host, port, keepalive, clean_session):
        client = MQTT.MQTTClient(client_id, clean_session=clean_session,
                                 msg_handler=msg_handler)
        client.connect(host, port=port, keepalive=keepalive)
        self.clients.append(client)

    def disconnect_all(self):
        for client in self.clients:
            client.disconnect()

    def remove_client(self, client_id):
        found_client = self._find_client(client_id)
        self.clients.remove(found_client)

    def client_publish(self, client_id, topic, data, qos):
        found_client = self._find_client(client_id)
        found_client.publish(topic, payload=data, qos=qos)

    def client_subscribe(self, client_id, topic, qos):
        found_client = self._find_client(client_id)
        found_client.subscribe(topic, qos=qos)

    def client_unsubscribe(self, client_id, topic):
        found_client = self._find_client(client_id)
        found_client.unsubscribe(topic)

    def _find_client(self, client_id):
        filtered = [client for client in self.clients if client.client_id == client_id]

        if not filtered:
            raise ValueError('Client ID not found in client list')

        return filtered[0]
