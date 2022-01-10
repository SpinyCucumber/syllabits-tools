import json
import click

@click.group()
def collection():
    pass

def collection_transformer(func):
    @click.argument('path', type=click.Path(exists=True))
    def wrapped(path, *args, **kwargs):
        with open(path, 'r+') as file:
            data = json.load(file)
            # Transform collection data and write aback to file
            func(data, *args, **kwargs)
            file.seek(0)
            json.dump(data, file)
            file.truncate()
            file.close()
    return wrapped

def poem_transformer(func):
    @collection_transformer
    def wrapped(data, *args, **kwargs):
        # Apply transformer to each poem in collection
        for poem in data:
            func(poem, *args, **kwargs)
    return wrapped

@collection.command('setall')
@click.argument('key')
@click.argument('value')
@poem_transformer
def set_all(poem, key, value):
    poem[key] = value

@collection.command('removeall')
@click.argument('key')
@poem_transformer
def remove_all(poem, key):
    del poem[key]

@collection.command('usetext')
@click.argument('text_path', type=click.Path(exists=True))
@collection_transformer
def use_text(data, text_path):
    with open(text_path, 'r') as text_file:
        poem_index = 0
        line_index = 0
        for line in text_file:
            stripped = line.rstrip()
            if (stripped):
                # Copy line into collection
                data[poem_index]['lines'][line_index]['text'] = stripped
                line_index += 1
            else:
                poem_index += 1
                line_index = 0
        text_file.close()

@collection.command('splitkey')
@poem_transformer
def split_key(poem):
    for line in poem['lines']:
        line['key'] = list(line['key'])

@collection.command('generateorders')
@poem_transformer
def generate_orders(poem):
    order = 0
    for line in poem['lines']:
        line['order'] = order
        order += 1

if __name__ == '__main__':
    collection()