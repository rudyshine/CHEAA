import requests

url='http://news.cheaa.com/hangye_2.shtml'
r=requests.get(url)
print(r.text)