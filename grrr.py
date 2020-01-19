import urllib.request
import re


def find_in_xml(xml, tag, position=1):
    length = len(tag)
    start = 0
    while position > 0:
        start = xml[start:].find(tag)
        if start == -1:
            return None
        position -= 1
        start += length
    start += xml[start:].find('>')+1
    end = start+xml[start:].find('</'+tag[1:])
    return xml[start:end]


class Grrr:
    def __init__(self, key):
        if not isinstance(key, str) or not key.isalnum():
            raise ValueError("Invalid key!") 
        self.url_search = 'https://www.goodreads.com/search/index.xml?key={}&'.format(key)
        self.url_review = 'https://www.goodreads.com/book/title.xml?key={}&'.format(key)
        self.books = []

    def search_by_title(self, title, save=False):
        query = urllib.parse.urlencode({
            'q': title
        })
        response = urllib.request.urlopen(self.url_search+query)
        xml = response.read().decode("utf-8")
        entry = find_in_xml(xml, '<work')
        result = {
            "rating_count": int(find_in_xml(entry, '<ratings_count')),
            "review_count": int(find_in_xml(entry, '<text_reviews_count')),
            "year": int(find_in_xml(entry, '<original_publication_year')),
            "average_rating": float(find_in_xml(entry, '<average_rating')),
            "title": find_in_xml(entry, '<title'),
            "author": find_in_xml(entry, '<name')
        }
        if save:
            self.books.append(result)
        return result
    
    def get_book_tags(self, title, rating=None):
        query = urllib.parse.urlencode({
            'title': title
        })
        response = urllib.request.urlopen(self.url_review+query)
        xml = response.read().decode("utf-8")
        shelf = find_in_xml(xml, '<popular_shelves')
        result = {}
        tags = [
            ['re-?reads?" count="[0-9]+', 'reread'],
            ['[a-z]*favou?rites?[-a-z]*" count="[0-9]+', 'favorite'],
            ['[a-z]*-?own[-a-z]*" count="[0-9]+', 'own']
        ]
        for pattern in tags:
            result[pattern[1]] = 0
            for match in re.findall(pattern[0], shelf, flags=0):
                result[pattern[1]] += int(match[match.find('="')+2:])
        return result


if __name__ == '__main__':
    print('\n\nbuilt by Manuel Velarde to gather data for roBERTo.wtf\n')

    # KEY = None
    # with open("key.json") as file:
    #     KEY = json.load(file)['key']

    # test = Grrr(KEY)
    # print(test.get_book_tags("Harry Potter and the Sorcerer's Stone"))