import shelve
from selenium import webdriver

def extract_data():
    rows = browser.find_elements_by_xpath("//*[@id='print_0']/table//tr")
    header = []
    head_row = rows[0]
    for column in head_row.find_elements_by_xpath("td"):
        header.append(column.text)

    round_data = []
    for row in rows[1:]:
        print("===")
        team_data = {}
        for index,column in enumerate(row.find_elements_by_xpath("td")):
            curr_header = header[index]
            curr_text =column.text
            if len(curr_header)==0 and len(curr_text)==0 : continue
            print("{} = {}".format(curr_header, curr_text))
            team_data[curr_header]=curr_text
        print("===")
        round_data.append(team_data)
    return round_data




db = shelve.open("league_shelve.txt")

browser = webdriver.Firefox()
browser.get('http://football.org.il/Leagues/Pages/LeagueDetails.aspx')

data = {}

while True:
    round_name = browser.find_element_by_xpath('//*[@id="tdLeagueRound0"]').text
    print("=== EXTRACTING DATA round {} ===".format(round_name))
    round_data = extract_data()
    data[round_name]=round_data
    if round_name == "מחזור 1":
        break
    prev = browser.find_element_by_xpath('//*[@id="tdPrevLeagueRound0"]')
    prev.click()

db["DATA"] = data
db.close()