# Python 3.11.4

from bs4 import BeautifulSoup
from os.path import join, isdir
from os import walk
import json

PREVIEW_LENGTH = 140

def main():
    if not isdir('src/tidings'):
        raise Exception('no `src/tidings/` folder found in current directory')

    index = {}

    for root, _, posts in walk('src/tidings'):
        for post in posts:
            with open(join(root, post), 'r') as f:
                soup = BeautifulSoup(f, 'html.parser')
            title = str(soup.title.string)
            date = str(soup.find(id='date').string)
            content = soup.main
            if not content:
                content = BeautifulSoup('', 'html.parser')
            for header in content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                if header:
                    header.decompose()
            content.find(id='date').decompose()
            plain_text = ' '.join(content.stripped_strings)
            preview = plain_text[:PREVIEW_LENGTH] + '...'
            index[post] = {'title': title, 'date': date, 'preview': preview}
    
    with open('tidings.json', 'w') as f:
        json.dump(index, f)

if __name__ == '__main__':
    main()
