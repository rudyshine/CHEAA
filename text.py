import requests

url='http://news.cheaa.com/2008/0221/117484.shtml'
r=requests.get(url)
print(r.text)