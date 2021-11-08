import json, urllib.request, ssl
from datetime import date, datetime
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR')

context = ssl._create_unverified_context()

def get_photos(json):
    photos = []
    for photo in json:
        try:
            photos.append(photo['md5'])
        except:
            pass
    return photos


def get_journal(file):
    with open(file, 'r') as myfile:
        journal_dict = json.load(myfile)

    journal_list = []
    journal = {}

    for entrie in journal_dict['entries']:
        try:
            text = entrie['text'].split('![]')
            text = text[0].replace('\\', '')
            title = text.split('\n')[0]
            text = text.replace('\n', '<br/>')
            date_json = entrie['creationDate'].split('T')[0]
            date_json = datetime.strptime(date_json, '%Y-%m-%d')
            page = date_json.strftime("%B").capitalize() + date_json.strftime("%Y")
            date_json = date_json.strftime("%A %d %B %Y")

            print(date_json)
            journal = {'title': title, 'date': date_json, 'text': text, 'photos': get_photos(entrie['photos']), 'page': page}
        except:
            journal = {'title': '', 'date': '', 'text': '', 'photos': '', 'page': ''}

        journal_list.append(journal)

    return journal_list

# for journal in journal_dict:
    # print(journal_dict['entries'])


def get_json_ratp(url):
    try:
        with urllib.request.urlopen(url, context=context) as url:
            data = json.loads(url.read().decode())
    except:
        data = "404"
    return data
