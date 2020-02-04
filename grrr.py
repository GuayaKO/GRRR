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


def find_iframe_src(xml):
    tag = "<iframe"
    start = 0
    start = xml[start:].find(tag)
    start += xml[start:].find('src="')+5
    end = start+xml[start:].find('"')
    return xml[start:end]



class Grrr:
    def __init__(self, key):
        if not isinstance(key, str) or not key.isalnum():
            raise ValueError("Invalid key!") 
        self.url_search = 'https://www.goodreads.com/search/index.xml?key={}&'.format(key)
        self.url_tags = 'https://www.goodreads.com/book/title.xml?key={}&'.format(key)
        self.url_reviews = 'https://www.goodreads.com/book/show/{}.xml?'+'key={}'.format(key)
        self.books = []

    def search_by_title(self, title, save=False):
        query = urllib.parse.urlencode({
            'q': title
        })
        response = urllib.request.urlopen(self.url_search+query)
        xml = response.read().decode("utf-8")
        entry = find_in_xml(xml, '<work')
        result = {
            "book_id": int(find_in_xml(entry, '<id', 2)),
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
    
    def get_book_tags(self, title):
        query = urllib.parse.urlencode({
            'title': title
        })
        response = urllib.request.urlopen(self.url_tags+query)
        xml = response.read().decode("utf-8")
        shelf = find_in_xml(xml, '<popular_shelves')
        result = {}
        tags = [
            ['[a-z]*re-?reads?[-a-z]*" count="[0-9]+', 'reread'],
            ['[a-z]*favou?rites?[-a-z]*" count="[0-9]+', 'favorite'],
            ['[a-z]*-?own[-a-z]*" count="[0-9]+', 'own'],
            ['[a-z]*business[-a-z]*" count="[0-9]+', 'business'],
            ['[a-z]*data[-a-z]*" count="[0-9]+', 'data'],
            ['[a-z]*math[-a-z]*" count="[0-9]+', 'math'],
            ['[a-z]*statistics?[-a-z]*" count="[0-9]+', 'stats'],
            ['[a-z]*computer[-a-z]*" count="[0-9]+', 'compsci'],
            ['[a-z]*economics?[-a-z]*" count="[0-9]+', 'economics'],
            ['[a-z]*complex[-a-z]*" count="[0-9]+', 'complexity'],
            ['[a-z]*psychology[-a-z]*" count="[0-9]+', 'psychology'],
            ['[a-z]*behavio[-a-z]*" count="[0-9]+', 'behaviour'],
            ['[a-z]*politics[-a-z]*" count="[0-9]+', 'politics'],
            ['[a-z]*sociology[-a-z]*" count="[0-9]+', 'sociology'],
            ['[a-z]*anthropology[-a-z]*" count="[0-9]+', 'anthropology'],
            ['[a-z]*history[-a-z]*" count="[0-9]+', 'history'],
            ['[a-z]*biology[-a-z]*" count="[0-9]+', 'biology'],
            ['[a-z]*evolution[-a-z]*" count="[0-9]+', 'evolution'],
            ['[a-z]*health[-a-z]*" count="[0-9]+', 'health'],
            ['[a-z]*cogniti[-a-z]*" count="[0-9]+', 'cognitive'],
            ['[a-z]*neuro[-a-z]*" count="[0-9]+', 'neuroscience']
        ]
        for pattern in tags:
            result[pattern[1]] = 0
            for match in re.findall(pattern[0], shelf, flags=0):
                result[pattern[1]] += int(match[match.find('="')+2:])
        return result

    def get_book_reviews(self, book_id):
        reviews = []
        links = []
        iframe_response = urllib.request.urlopen(self.url_reviews.format(book_id))
        iframe_xml = iframe_response.read().decode("utf-8")
        response = urllib.request.urlopen(find_iframe_src(iframe_xml))
        xml = response.read().decode("utf-8")
        body = find_in_xml(xml, '<body')
        link_pattern = r'https:\/\/www\.goodreads\.com\/review\/show\/[0-9]+"'
        for match in re.findall(link_pattern, body, flags=0):
            links.append(match[:-1])
        for link in links:
            review_response = urllib.request.urlopen(link)
            review_xml = review_response.read().decode("utf-8")
            review_pattern = r'<div class="reviewText mediumText description readable" itemprop=\'reviewBody\'>((.|\n)*?)</div>'
            for match in re.findall(review_pattern, review_xml, flags=0):
                reviews.append(match[0])
        return reviews



if __name__ == '__main__':
    print('\n\nbuilt by Manuel Velarde to gather data for liBER-Trinus.wtf\n')

    # import json
    # KEY = None
    # with open("key.json") as file:
    #     KEY = json.load(file)['key']

    # test = Grrr(KEY)
    # print("The Model Thinker\n", test.search_by_title("The Model Thinker: What You Need to Know to Make Data Work for You"))
    # print("\nThe Model Thinker\n", test.get_book_reviews(39088592))
    # print("\nThe Model Thinker\n", len(test.get_book_reviews(39088592)))
    # print("\nBehave: The Biology of Humans at Our Best and Worst\n", test.get_book_reviews("Behave: The Biology of Humans at Our Best and Worst"))