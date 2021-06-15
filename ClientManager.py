import MQTT


class ClientManager:
    """ Keeps track of clients and topics they are subscribed to """

    def __init__(self):
        self.clients = []

    def add_client(self, client_id, host, port, keepalive, clean_session):
        client = MQTT.MQTTClient(client_id, clean_session=clean_session)
        client.connect(host, port=port, keepalive=keepalive)
        self.clients.append(client)

    def disconnect_all(self):
        for client in self.clients:
            client.disconnect()

    def remove_client(self, client_id):
        filtered = [client for client in self.clients if client.client_id == client_id]

        if filtered:
            found_client = filtered[0]
            found_client.disconnect()
            self.clients.remove(found_client)
        else:
            raise ValueError('Client ID not found when removing')

    def client_publish(self, client_id, topic, data, qos):
        filtered = [client for client in self.clients if client.client_id == client_id]

        if filtered:
            found_client = filtered[0]
            found_client.publish(topic, payload=data, qos=qos)
        else:
            raise ValueError('Client ID not found when publishing')
