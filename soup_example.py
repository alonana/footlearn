from bs4 import BeautifulSoup
import io
import urllib.request

url = 'http://football.org.il/Leagues/Pages/LeagueDetails.aspx'
response = urllib.request.urlopen(url)
data = response.read()      
html = data.decode('utf-8') 
soup = BeautifulSoup(html,"html.parser")
table = soup.find('table', id='LeaguesTable')
out = io.open("output.txt",mode='w',encoding="utf8")
data = []
for row in table.find_all('tr'):
	cols = row.find_all('td',{'class':'BDCItemText'})
	cols = [e.text.strip() for e in cols]
	data.append(cols)
for cols in data:
	for col in cols:
		print (col + "\n", end="", file=out)
	print ("next\n\n", end="", file=out)
		
out.close()
