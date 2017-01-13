import shelve
import time
import re
from selenium import webdriver
import requestor_model


def extract_sessions():
    sessions_amount = len(browser.find_elements_by_xpath("//*[@id='ddlSeason']/option"))
    print("{} total sessions to scan".format(sessions_amount))
    sessions_data = requestor_model.SessionsData()
    sessions_limit = 100
    for session_index in range(1, sessions_amount + 1):
        session = browser.find_element_by_xpath('//*[@id="ddlSeason"]/option[{}]'.format(session_index))
        session_name = session.text
        print("scanning session {}".format(session_name))
        session.click()
        browser.find_element_by_xpath('//input[@class="BtnChoose"]').click()
        time.sleep(30)
        sessions_data.add(session_name, extract_session())
        sessions_limit -= 1
        if sessions_limit == 0:
            break
    return sessions_data


def extract_session():
    print("session extract starting")
    session_data = requestor_model.SessionData()
    for round_element in browser.find_elements_by_xpath('//*[starts-with(@id,"tdLeagueRound")]'):
        name = round_element.text
        match = re.match("(\\S+)\\s+(\\S+)", name)
        if not match:
            continue
        section_id = round_element.get_attribute("id")[-1:]
        extract_all_rounds(session_data, section_id)
    print("session extract done {}".format(session_data))
    return session_data


def extract_all_rounds(session_data, section_id):
    print("handling section ID {}".format(section_id))
    rounds_limit = 100
    while True:
        round_element = browser.find_element_by_xpath('//*[@id="tdLeagueRound{}"]'.format(section_id))
        round_name = round_element.text
        print("extracting data for round {}".format(round_name))
        position_table = extract_data(section_id, "תיקו")
        if position_table is not None:
            print("adding position table")
            session_data.add_position(round_name, position_table)
        games_table = extract_data(section_id, "מגרש")
        if games_table is not None:
            print("adding game table")
            session_data.add_game(round_name, games_table)
        rounds_limit -= 1
        if rounds_limit == 0:
            break
        if round_name == "מחזור 1":
            break
        prev = browser.find_element_by_xpath('//*[@id="tdPrevLeagueRound{}"]'.format(section_id))
        print("click on prev round")
        prev.click()
        time.sleep(3)


def extract_data(section_id, required_header):
    # print("looking for header {}".format(required_header))
    elements = browser.find_elements_by_xpath("//*[@id='print_{}']/table".format(section_id))
    if len(elements) == 0:
        print("WARNING: skipping table - bad site data, we might have another round")
        return None
    if len(elements) > 1:
        raise Exception("too many elements")
    table_element = elements[0]
    rows = table_element.find_elements_by_xpath(".//tr")
    if len(rows) == 0:
        print("empty table, skipping")
        return None
    head_row = rows[0]
    for header in head_row.find_elements_by_xpath("td[@class!='BDCHorizonSeparator']"):
        if header.text == required_header:
            # print("header located")
            return extract_table(table_element)
    # print("header not located")
    return None


def extract_table(table_element):
    table_data = []
    rows = table_element.find_elements_by_xpath(".//tr")
    header = []
    head_row = rows[0]
    for column in head_row.find_elements_by_xpath("td[@class!='BDCHorizonSeparator']"):
        header.append(column.text)

    rows = table_element.find_elements_by_xpath(".//tr[starts-with(@class,'BDC')]")
    for row in rows:
        row_data = {}
        for index, column in enumerate(row.find_elements_by_xpath("td[@class!='BDCHorizonSeparator']")):
            curr_header = header[index]
            curr_text = column.text
            if len(curr_header) == 0 and len(curr_text) == 0: continue
            row_data[curr_header] = curr_text
        table_data.append(row_data)
    print(table_data)
    return table_data


print("starting")
browser = webdriver.Firefox()
browser.get('http://football.org.il/Leagues/Pages/LeagueDetails.aspx')
print("page loaded")
data = extract_sessions()
db = shelve.open("league_shelve.txt")
db["DATA"] = data
db.close()
