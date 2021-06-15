from PyInquirer import prompt, Separator


def main_menu():
    questions = [{
        'type': 'list',
        'name': 'theme',
        'message': 'Choose an action:',
        'choices': [
            'Show MQTT clients',
            'Add MQTT client',
            'Remove (disconnect) MQTT client',
            'Publish to a topic',
            'Subscribe client to a topic',
            'Unsubscribe client from a topic'
        ]
    }]

    return prompt(questions).get('theme')


def show_clients():
    pass


def add_client():
    pass


def remove_client():
    pass


def subscribe_client():
    pass


def unsubscribe_client():
    pass


def publish():
    pass


def load_preset():
    pass

