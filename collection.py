import json
import click
import openpyxl

footLookup = {
    'u/': 'i',
    '/u': 't',
    '/uu': 'd',
    'uu/': 'a',
    '//': 's',
    'uu': 'p',
}

@click.group()
def collection():
    pass

def collection_transformer(func):
    @click.argument('file', type=click.File('r+'))
    def wrapped(file, *args, **kwargs):
        data = json.load(file)
        # Transform collection data and write aback to file
        func(data, *args, **kwargs)
        file.seek(0)
        json.dump(data, file)
        file.truncate()
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

@collection.command('useplaintext')
@click.argument('text_file', type=click.File())
@collection_transformer
def use_plaintext(data, text_file):
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

@collection.command('importworkbook')
@click.argument('workbook_path', type=click.Path(exists=True))
@collection_transformer
def import_workbook(data, workbook_path):
    # Load workbook and iterate through worksheets
    workbook = openpyxl.load_workbook(workbook_path)
    for worksheet in workbook:
        # Find corresponding poem (worksheet title should be index)
        poem_index = int(worksheet.title) - 1
        poem = data[poem_index]
        # Iterate over pairs of rows. First row is key, second is text
        rows = worksheet.rows
        line_index = 0
        for key_row, text_row in zip(rows, rows):
            # Convert rows into actual key and text
            # We slice the text to omit comments and such
            line = poem['lines'][line_index]
            key = [footLookup.get(cell.value, '') for cell in key_row if cell.value != None]
            line['key'] = key
            line['text'] = ' '.join([str(cell.value) for cell in text_row[:len(key)]])
            line_index += 1

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