import requests
from bs4 import BeautifulSoup

# specify the URL of the webpage you want to start scraping from
url = 'https://www.youtube.com/watch?v=25QQ2Jw3Cdw'

# send a GET request to the URL and store the response
response = requests.get(url)

# parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# save the HTML content of the webpage to a file
with open('html.txt', 'w', encoding='utf-8') as f:
    f.write(str(soup))

# create a list to store all the links found on the page
links = []

# create a set to store the visited links
visited_links = set()

# find all the links on the page and append their href attributes to the list
for link in soup.find_all('a'):
    href = link.get('href')
    if href is not None:
        links.append(href)

# continue scraping all the links on the page until there are no more new links to follow
while links:
    # pop the next link from the list to scrape
    next_link = links.pop(0)

    # check if the link has already been visited
    if next_link in visited_links:
        continue

    # add the link to the set of visited links
    visited_links.add(next_link)

    # if the link is not an absolute URL, prepend the base URL
    if not next_link.startswith('http'):
        next_link = url + next_link

    # send a GET request to the next link and store the response
    response = requests.get(next_link)
    
    # parse the content type of the response
    content_type = response.headers['Content-Type']

    # if the response contains JavaScript, save it to a file
    if 'javascript' in content_type:
        with open('javascript.txt', 'a', encoding='utf-8') as f:
            f.write(response.text + '\n')
    # if the response contains CSS, save it to a file
    elif 'css' in content_type:
        with open('css.txt', 'a', encoding='utf-8') as f:
            f.write(response.text + '\n')
    # otherwise, parse the HTML content of the response using BeautifulSoup
    else:
        soup = BeautifulSoup(response.content, 'html.parser')

        # save the HTML content of the webpage to a file
        with open('html.txt', 'a', encoding='utf-8') as f:
            f.write(str(soup) + '\n')

        # find all the links on the page and append their href attributes to the list
        for link in soup.find_all('a'):
            link_url = link.get('href')

            # add the link to the list if it hasn't been added already
            if link_url is not None and link_url not in links and link_url not in visited_links:
                # if the link is not an absolute URL, prepend the base URL
                if not link_url.startswith('http'):
                    link_url = url + link_url

                links.append(link_url)

# append all the links found on the page to a file
with open('links.txt', 'a', encoding='utf-8') as f:
    for link in visited_links:
        f.write(link + '\n')