# import socket 

# HOST = 'www.google.com' # Server hostname or IP address
# PORT = 80

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = (HOST, PORT)
# client_socket.connect(server_address)

# request_header = b'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
# client_socket.sendall(request_header)

# response = ''
# while True:
#     recv = client_socket.recv(1024)
#     if not recv:
#         break
#     response += recv.decode('latin-1')

# print(response)
# client_socket.close()

# import urllib3

# using proxy
# user_agent_header = urllib3.make_headers(user_agent="<USER AGENT>")
# pool = urllib3.ProxyManager('<PROXY IP>', headers=user_agent_header)
# r = pool.request('GET', 'http://www.google.com')

# http = urllib3.PoolManager()
# r = http.request('GET', 'http://www.google.com')
# print(r.data)

# from lxml import html

# data_string = r.data.decode('latin-1', errors='ignore')

# tree = html.fromstring(data_string)

# links = tree.xpath('//a')

# for link in links:
#     print(link.get('href'))


import requests

# r = requests.get('https://www.scrapingninja.co')
# print(r.text)


# url = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_light_color_272x92dp.png'
# response = requests.get(url)
# with open('image.jpg', 'wb') as file:
#     file.write(response.content

from bs4 import BeautifulSoup

# BASE_URL = 'https://news.ycombinator.com'
# USERNAME = ""
# PASSWORD = ""

# S = requests.Session()

# data = {"goto": "news", "acct": USERNAME, "pw": PASSWORD}
# r = S.post(f'{BASE_URL}/login', data=data)

# soup = BeautifulSoup(r.text, 'html.parser')
# if soup.find(id='logout') is not None:
#     print('Successfully logged in')
# else:
#     print('Authetication Error')

r = requests.get('http://news.ycombinator.com')
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.findAll('tr', class_='athing')

formated_links = []

for link in links:
    data = {
        'id': link['id'],
        'title': link.find_all('td')[2].a.text,
        "url": link.find_all('td')[2].a['href'],
        "rank": int(link.find_all('td')[0].span.text.replace('.', ''))
    }
    formated_links.append(data)

import csv

csv_file = 'hacker_news_posts.csv'


with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'title', 'url', 'rank'])
    writer.writeheader()
    for row in formated_links:
        writer.writerow(row)


import psycopg2

con = psycopg2.connect(
    host="127.0.0.1",
    port="",
    user="",
    password="",
    database="scrape_demo"
)

cur = con.cursor()

r = requests.get('https://news.ycombinator.com')
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.findAll('tr', class_='athing')

for link in links:
    cur.execute("""
        INSERT INTO hn_links (id, title, url, rank)
        VALUES (%s, %s, %s, %s)
        """,
        (
            link['id'],
            link.find_all('td')[2].a.text,
            link.find_all('td')[2].a['href'],
            int(link.find_all('td')[0].span.text.replace('.', ''))
        )
    )

# Commit the data
con.commit()

# Close our database connections
cur.close()
con.close()
