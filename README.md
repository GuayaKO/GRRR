# GRRR
Python `class` to query the **Goodreads** API. All you need is a _Goodreads API key_, and you'll be ready to query!
```
from grrr import Grrr

db = Grrr(YOUR_KEY)
db.search_by_title('The Aleph', save=True)
```
Now if you check `db.books` you will find:
```
[{
    'rating_count': '28015',
    'review_count': '1079',
    'year': '1945',
    'average_rating': '4.38',
    'title': 'The Aleph and Other Stories',
    'author': 'Jorge Luis Borges'
}]
```
