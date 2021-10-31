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
    with open(path, 'r+') as file:
        data = json.load(file)
        # Set key of all poems
        for poem_data in data:
            poem_data[key] = value
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

@collection.command('removeall')
@click.argument('path', type=click.Path(exists=True))
@click.argument('key')
def set_all(path, key):
    with open(path, 'r+') as file:
        data = json.load(file)
        # Remove key of all poems
        for poem_data in data:
            del poem_data[key]
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

if __name__ == '__main__':
    collection()