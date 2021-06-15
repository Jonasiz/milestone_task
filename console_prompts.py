from PyInquirer import prompt, Separator
from prompt_toolkit.validation import Validator, ValidationError
from regex import regex

main_actions = {
    'show': 'Show MQTT clients',
    'add': 'Add MQTT client',
    'remove': 'Remove (disconnect) MQTT client',
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

