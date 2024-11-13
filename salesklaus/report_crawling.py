
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time


@dataclass
class SFSessionIDs:
    sid: str
    sid_Client: str


def deserialize_report(report_url: str, sf_session_ids: SFSessionIDs) -> list[dict]:
    table_soup = _table_soup_from_report(report_url, sf_session_ids)
    report_entries = _deserialize_table_soup(table_soup)
    return report_entries


def _table_soup_from_report(report_url: str, sf_session_ids: SFSessionIDs) -> BeautifulSoup:

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--start-maximized")  # Start maximized

    driver = webdriver.Chrome(options=options)
    # Arbitrary large height for long content
    driver.set_window_size(2500, 50000)

    driver.get(report_url)  # Initial dummy get request to set the cookie
    driver.add_cookie({'name': 'sid', 'value': sf_session_ids.sid,
                       'domain': '.salesforce.com', 'path': '/'})
    driver.add_cookie({'name': 'sid_Client', 'value': sf_session_ids.sid_Client,
                       'domain': '.salesforce.com', 'path': '/'})

    driver.get(report_url)

    time.sleep(2)

    iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(iframe)

    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')
    table_soup = soup.find(
        'table', class_='data-grid-table data-grid-full-table')
    # actually find out why this might happen (as it does randomly) and print a better error
    if not table_soup:
        raise Exception(
            "Something went wrong with requesting the report or extracting the report. Is the URL correct? Is it pointing to a SF report? Please try again.")
    return table_soup


def _deserialize_table_soup(table_soup: BeautifulSoup) -> list[dict]:
    opportunities = []
    # headers
    header_row = table_soup.find("tr", class_="data-grid-header-row")
    headers = []
    if header_row:
        header_cells = header_row.find_all(
            "span", class_="lightning-table-cell-measure-header-value")[1:]
        headers = [header.get_text(strip=True) for header in header_cells]
    # data rows
    data_rows = table_soup.find_all("tr", class_="data-grid-table-row")[1:]
    for row_index, row in enumerate(data_rows):
        row_data = dict()
        cells = row.find_all(["th", "td"])[1:]
        for cell_index, cell in enumerate(cells):
            cell_data = cell.get_text(strip=True)
            row_data[headers[cell_index]] = cell_data
        opportunities.append(row_data)
    return opportunities
