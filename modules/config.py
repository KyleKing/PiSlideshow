import json


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


if __name__ == '__main__':
    # Example Script
    for param in ['balloon_dir', 'access_token']:
        print '{}: {}'.format(param, read_json(param))
