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
            'message': 'Client ID'
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
            'type': 'input',
            'name': 'clean_session',
            'message': 'Clean session? (y/n)',
            'default': 'y',
            'validate': lambda val: val in ['y', 'n'] or 'type "y" or "n"'
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
    if not client_ids:
        print('Please create a client first!')
        return None

    questions = [
        {
            'type': 'list',
            'name': 'pub_id',
            'message': 'Choose client for publishing:',
            'choices': [str(client_id) for client_id in client_ids]
        },
        {
            'type': 'input',
            'name': 'qos',
            'message': 'Quality of service (QoS):',
            'default': '1',
            'validator': PositiveNumberValidator
        },
        {
            'type': 'input',
            'name': 'topic',
            'message': 'Write your topic:',
            'default': 'interview/ioma/sensors/temperature/living_room/ABC1'
        },
        {
            'type': 'input',
            'name': 'data',
            'message': 'Data to publish:',
            'default': '{"temp": 32}'
        }
    ]

    return prompt(questions)


def subscribe_client():
    pass


def unsubscribe_client():
    pass


def load_preset():
    pass

