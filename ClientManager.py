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

