from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sys
# import timeit

print("Enter user id:", end='')
userId = input()
# startTime = timeit.default_timer()
url = 'http://www.imdb.com/user/ur' + userId + '/ratings'
baseUrl = url
page = urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
title = soup.find('title').text
if title == 'IMDb: ':
    print('Error: Cannot access the ratings list! Please make sure that the rating list is public.')
    sys.exit()
title = re.search(r'IMDb: (.+)\'s Ratings', title).group(1)
pageNo = re.search(r'Page [0-9]+ of ([0-9]+)', soup.find('div', 'desc').text)
if pageNo is None:
    pageNo = 1
else:
    pageNo = int(pageNo.group(1))
number = imdbRating = yourRating = 0
curPage = 1
while curPage <= pageNo:
    ratingsList = soup.find_all('div', 'list_item')
    number += len(ratingsList)
    for item in ratingsList:
        name = item.find_next('b').find('a').text
        rating1 = float(re.search(r'Users rated this ([0-9]+.[0-9])', item.find('div', 'rating-list').get('title')).group(1))
        rating2 = int(re.search(r'rated this ([0-9]+).', item.find('div', 'quoted_rating').text).group(1))
        imdbRating += rating1
        yourRating += rating2
        # print(name, rating2, rating1)
    if curPage != pageNo:
        url = baseUrl + '?start=' + str(curPage * 100 + 1) + '&view=detail&sort=ratings_date:desc'
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
    curPage += 1
print('Total reviews:', number)
print(title + '\'s average rating: %.2f' % (yourRating / number))
print('IMDB average rating: %.2f' % (imdbRating / number))
# print(timeit.default_timer() - startTime)