import json
import io, os
import glob
from bs4 import BeautifulSoup
from google.cloud import vision
from google.protobuf import json_format


def extract_text(file_source):
    import os, io
    import re

    with open(file_source, encoding="UTF-8") as f:
        data = json.load(f)
    if 'responses' not in data:
        return

    print('reading' + file_source)
    s = ''
    length = len(data['responses'])
    print(length)
    for i in range(length):
        response = data['responses'][i]
        if 'fullTextAnnotation' not in response:
            print(file_source + "No fullTextAnnotation at page:", i)
            continue
        fullTextAnnotation = data['responses'][i]['fullTextAnnotation']
        if 'text' not in fullTextAnnotation:
            print(file_source + "No text  at page:", i)
            continue

        s = s + fullTextAnnotation['text']

    f = open(file_source + '.txt', 'w+', encoding="UTF-8")
    f.write(s)
    print('just printed file' + file_source)
    f.close()

for filename in glob.glob('*.json'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
    extract_text(filename)
