import json
import click

@click.group()
def collection():
    pass

@collection.command('setall')
@click.argument('path', type=click.Path(exists=True))
@click.argument('key')
@click.argument('value')
def set_all(path, key, value):
    with open(path, 'w+') as file:
        data = json.load(file)
        # Set key of all poems
        for poem_data in data:
            poem_data[key] = value
        json.dump(data, file)

if __name__ == '__main__':
    collection()