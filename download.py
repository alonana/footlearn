import io
import urllib.request
import lxml.html as lh

url = 'http://football.org.il/Leagues/Pages/LeagueDetails.aspx'
response = urllib.request.urlopen(url)
root = lh.parse(response)
rows =  root.xpath("//*[@id='print_0']/table//tr")
header = rows[0].xpath("td/text()")
for row in rows[1:]:
	for idx,col in enumerate(row.xpath("td/text()")):
		print(header[idx] + "=" +col + ", ")
	print()
