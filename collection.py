import json
import click

@click.group()
def collection():
    pass

@collection.command('setall')
@click.argument('collection_path', type=click.Path(exists=True))
@click.argument('key')
@click.argument('value')
def set_all(collection_path, key, value):
    with open(collection_path, 'r+') as file:
        data = json.load(file)
        # Set key of all poems
        for poem_data in data:
            poem_data[key] = value
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        file.close()

@collection.command('removeall')
@click.argument('collection_path', type=click.Path(exists=True))
@click.argument('key')
def remove_all(collection_path, key):
    with open(collection_path, 'r+') as file:
        data = json.load(file)
        # Remove key of all poems
        for poem_data in data:
            del poem_data[key]
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        file.close()

@collection.command('usetext')
@click.argument('collection_path', type=click.Path(exists=True))
@click.argument('text_path', type=click.Path(exists=True))
def use_text(collection_path, text_path):
    with open(collection_path, 'r+') as collection_file, open(text_path, 'r') as text_file:
        data = json.load(collection_file)

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
        
        # Rewrite collection
        collection_file.seek(0)
        json.dump(data, collection_file, indent=4)
        collection_file.truncate()

        text_file.close()
        collection_file.close()

@collection.command('splitkey')
@click.argument('collection_path', type=click.Path(exists=True))
def split_key(collection_path):
    with open(collection_path, 'r+') as file:
        data = json.load(file)
        # Convert key of each poem line from string to array of chars
        for poem_data in data:
            for line_data in poem_data['lines']:
                line_data['key'] = list(line_data['key'])
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        file.close()

if __name__ == '__main__':
    collection()