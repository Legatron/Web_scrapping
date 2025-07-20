"""
<span class="table-ip4-home">
                           178.76.204.16                           </span>
"""
import requests
import bs4
respose = requests.get("https://www.iplocation.net/")
html = respose.text
soup = bs4.BeautifulSoup(html, features="lxml" )
tag = soup.find( name = 'span', class_ = 'table-ip4-home')
ip_address = tag.text
ip_addr = ip_address.strip()
print(ip_addr)