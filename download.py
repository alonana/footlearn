import io
import urllib.request
import lxml.html as lxml_html
import sys

reload = False
if len(sys.argv)>1:
	if sys.argv[1]=="reload":
		reload = True

print ("running with reload={}".format(reload))

if reload :
	url = 'http://football.org.il/Leagues/Pages/LeagueDetails.aspx'
	response = urllib.request.urlopen(url)
	data = response.read()
	cache = open("cache.html","wb")
	cache.write(data)
	cache.close()

cache = open("cache.html","r")
data = cache.read()
root = lxml_html.fromstring(data)

rows = root.xpath("//*[@id='print_0']/table//tr")
header = rows[0].xpath("td/text()")
for row in rows[1:]:
	for idx,col in enumerate(row.xpath("td/text()")):
		print(header[idx] + "=" +col + ", ")
	print()
