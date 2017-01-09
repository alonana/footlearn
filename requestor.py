from selenium import webdriver
browser = webdriver.Firefox()
browser.get('http://football.org.il/Leagues/Pages/LeagueDetails.aspx')

def extractData():
	rows = browser.find_elements_by_xpath("//*[@id='print_0']/table//tr")
	header = []
	headRow = rows[0]
	for column in headRow.find_elements_by_xpath("td"):
		header.append(column.text)

	for row in rows[1:]:
		print("===")
		for index,column in enumerate(row.find_elements_by_xpath("td")):
			print("{} = {}".format(header[index],column.text))
		print("===")

while True:
	round = browser.find_element_by_xpath('//*[@id="tdLeagueRound0"]').text
	print("=== EXTRACTING DATA round {} ===".format(round))
	extractData()
	if round == "מחזור 1":
		break
	prev = browser.find_element_by_xpath('//*[@id="tdPrevLeagueRound0"]')
	prev.click()

