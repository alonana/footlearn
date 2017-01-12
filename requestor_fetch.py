import shelve
import time
from selenium import webdriver


def extract_session():
    print("session extract starting")
    data_rounds = {}
    data_games = {}

    rounds_limit = 50
    while True:
        round_name = browser.find_element_by_xpath('//*[@id="tdLeagueRound0"]').text
        print("=== EXTRACTING DATA round {} ===".format(round_name))
        data_rounds[round_name] = extract_data("תיקו")
        data_games[round_name] = extract_data("מגרש")
        rounds_limit -= 1
        if rounds_limit == 0:
            break

        if round_name == "מחזור 1":
            break
        prev = browser.find_element_by_xpath('//*[@id="tdPrevLeagueRound0"]')
        prev.click()

    return {"rounds": data_rounds, "games": data_games}


def extract_data(required_header):
    print("looking for header {}".format(required_header))
    table_data = []
    for table in browser.find_elements_by_xpath("//*[starts-with(@id,'print_')]/table"):
        rows = table.find_elements_by_xpath(".//tr")
        if len(rows) == 0:
            print("empty table, skipping")
            continue
        head_row = rows[0]
        header_located = False
        for header in head_row.find_elements_by_xpath("td[@class!='BDCHorizonSeparator']"):
            print("header is {}".format(header.text))
            if header.text == required_header:
                header_located = True
                break
        if header_located:
            print("header located")
            extract_table(table_data, table)
    return table_data


def extract_table(table_data, table):
    rows = table.find_elements_by_xpath(".//tr")
    header = []
    head_row = rows[0]
    for column in head_row.find_elements_by_xpath("td[@class!='BDCHorizonSeparator']"):
        header.append(column.text)

    rows = table.find_elements_by_xpath(".//tr[starts-with(@class,'BDC')]")
    for row in rows:
        print("===")
        team_data = {}
        for index, column in enumerate(row.find_elements_by_xpath("td[@class!='BDCHorizonSeparator']")):
            curr_header = header[index]
            curr_text = column.text
            if len(curr_header) == 0 and len(curr_text) == 0: continue
            print("{} = {}".format(curr_header, curr_text))
            team_data[curr_header] = curr_text
        print("===")
        table_data.append(team_data)


print("starting")
browser = webdriver.Firefox()
browser.get('http://football.org.il/Leagues/Pages/LeagueDetails.aspx')
print("page loaded")
sessions_amount = len(browser.find_elements_by_xpath("//*[@id='ddlSeason']/option"))
print("{} total sessions to scan".format(sessions_amount))
data = {}
for session_index in range(1, sessions_amount + 1):
    session = browser.find_element_by_xpath('//*[@id="ddlSeason"]/option[{}]'.format(session_index))
    session_name = session.text
    print("scanning session {}".format(session_name))
    session.click()
    browser.find_element_by_xpath('//input[@class="BtnChoose"]').click()
    time.sleep(10)
    data[session_name] = extract_session()

db = shelve.open("league_shelve.txt")
db["DATA"] = data
db.close()
