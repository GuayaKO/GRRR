import urllib.request

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
    URL = 'https://www.goodreads.com/search.xml?'

    def __init__(self, key):
        if not isinstance(key, str) or not key.isalnum():
            raise ValueError("Invalid key!") 
        self.url = 'https://www.goodreads.com/search.xml?key={}&'.format(key)
        self.books = []

    def search_by_title(self, title, page=1, search="all", save=False):
        query = urllib.parse.urlencode({
            'q': title,
            'page': page,
            'search': search
        })
        response = urllib.request.urlopen(self.url+query)
        xml = response.read().decode("utf-8")
        entry = find_in_xml(xml, '<work')
        result = {
            "rating_count": find_in_xml(entry, '<ratings_count'),
            "review_count": find_in_xml(entry, '<text_reviews_count'),
            "year": find_in_xml(entry, '<original_publication_year'),
            "average_rating": find_in_xml(entry, '<average_rating'),
            "title": find_in_xml(entry, '<title'),
            "author": find_in_xml(entry, '<name'),
            "image_url": find_in_xml(entry, '<image_url')
        }
        if save:
            self.books.append(result)
        return result

if __name__ == '__main__':
    print('\n\nbuilt by Manuel Velarde to gather data for roBERTo.wtf\n')