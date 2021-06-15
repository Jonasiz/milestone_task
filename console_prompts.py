from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError


main_actions = {
    'show': 'Show MQTT clients',
    'add': 'Add an MQTT client',
    'remove': 'Remove/Disconnect an MQTT client',
    'pub': 'Publish to a topic',
    'sub': 'Subscribe client to a topic',
    'unsub': 'Unsubscribe client from a topic'
}


class PositiveNumberValidator(Validator):
    def validate(self, document):
        try:
            cast_digit = int(document.text)

            if cast_digit <= 0:
                raise ValueError()
        except ValueError:
            raise ValidationError(
                message='Please enter a valid positive number',
                cursor_position=len(document.text)
            )


def main_menu():
    questions = [{
        'type': 'list',
        'name': 'action',
        'message': 'Choose an action:',
        'choices': [
            main_actions['show'],
            main_actions['add'],
            main_actions['remove'],
            main_actions['pub'],
            main_actions['sub'],
            main_actions['unsub'],
        ]
    }]

    return prompt(questions).get('action')


def show_clients(client_ids):
    if client_ids:
        print('List of active clients:')
        for client_id in client_ids:
            print('\tID: ' + str(client_id))
    else:
        print('No clients running!')


def add_client(client_ids, default_host, default_port):
    questions = [
        {
            'type': 'input',
            'name': 'client_id',
            'message': 'Client ID',
            'validate': lambda val: len(val) > 0 or 'ID is required'
        },
        {
            'type': 'input',
            'name': 'host',
            'message': 'Broker host',
            'default': default_host
        },
        {
            'type': 'input',
            'name': 'port',
            'message': 'Broker port',
            'default': str(default_port),
            'validate': PositiveNumberValidator
        },
        {
            'type': 'input',
            'name': 'keepalive',
            'message': 'Keep Alive (sec)',
            'default': '60',
            'validate': PositiveNumberValidator
        },
        {
            'type': 'confirm',
            'name': 'clean_session',
            'message': 'Clean session?',
            'default': True
        },
    ]

    return prompt(questions)


def remove_client(client_ids):
    if not client_ids:
        print('No clients to remove!')
        return None

    questions = [{
        'type': 'list',
        'name': 'remove_id',
        'message': 'Choose client to remove:',
        'choices': [str(client_id) for client_id in client_ids]
    }]

    return prompt(questions).get('remove_id')


def publish(client_ids):
    questions = [
        {
            'type': 'list',
            'name': 'pub_id',
            'message': 'Choose client for publishing:',
            'choices': [str(client_id) for client_id in client_ids]
        },
        {
            'type': 'input',
            'name': 'topic',
            'message': 'Write your topic:',
            'default': 'interview/ioma/sensors/temperature/living_room/ABC1'
        },
        {
            'type': 'input',
            'name': 'qos',
            'message': 'Quality of service (QoS):',
            'default': '1',
            'validate': PositiveNumberValidator
        },
        {
            'type': 'input',
            'name': 'data',
            'message': 'Data to publish:',
            'default': '{\"temp\": 32}'
        },
    ]

    return prompt(questions)


def subscribe_client(client_ids):
    if not client_ids:
        return None

    questions = [
        {
            'type': 'list',
            'name': 'sub_id',
            'message': 'Choose client for subscribing:',
            'choices': [str(client_id) for client_id in client_ids]
        },
        {
            'type': 'input',
            'name': 'topic',
            'message': 'Enter topic to subscribe to:',
            'default': 'interview/ioma/sensors/temperature/living_room/ABC1'
        },
        {
            'type': 'input',
            'name': 'qos',
            'message': 'Quality of service (QoS):',
            'default': '1',
            'validate': PositiveNumberValidator
        },
    ]

    return prompt(questions)


def unsubscribe_client_id(client_ids):
    if not client_ids:
        print('Please create a client first!')
        return None

    question = {
        'type': 'list',
        'name': 'unsub_id',
        'message': 'Choose client for unsubscribing:',
        'choices': [str(client_id) for client_id in client_ids]
    }

    return prompt([question]).get('unsub_id')


def unsubscribe_client_topic(client):
    if not client.sub_topics:
        print('Client is not subscribed to any topics!')
        return None

    question = {
        'type': 'list',
        'name': 'topic',
        'message': 'Choose topic to unsubscribe from:',
        'choices': client.sub_topics
    }

    return prompt([question]).get('topic')
