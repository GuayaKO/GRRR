import urllib.request

class Grrr:
    URL = 'https://www.goodreads.com/search.xml?'
    def __init__(self, key):
        if not isinstance(key, str) or not key.isalnum():
            raise ValueError("Invalid key!") 
        self.key = key

if __name__ == '__main__':
    print('\n\nbuilt by Manuel Velarde to gather data for roBERTo.wtf\n')