import json

import schedule


def read_json(param, filename='../secret.json'):
    """Return result of a given parameter from a JSON file
        param - dictionary key within specified file
        filename - path to JSON file
    """
    with open(filename, 'r') as json_file:
        json_string = json_file.read()
    datastore = json.loads(json_string)
    if param in datastore:
        return datastore[param]
    else:
        raise ValueError('Error: `{}` not in: {}'.format(param, json_string))


def schedule_weekdays(*days):
    """Helper for schedule batch days"""
    # Source: https://github.com/dbader/schedule/issues/99#issuecomment-292523927
    for day in (days or ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']):
        job = schedule.every()
        yield getattr(job, day)


if __name__ == '__main__':
    # Example Script
    for param in ['balloon_dir', 'access_token']:
        print('{}: {}'.format(param, read_json(param)))
