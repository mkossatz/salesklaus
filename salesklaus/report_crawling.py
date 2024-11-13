
from dataclasses import dataclass
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time





def deserialize_report_from_url(report_url: str, sf_sid: str) -> list[dict]:
    table_soup = _table_soup_from_report(report_url, sf_sid)
    report_entries = _deserialize_table_soup(table_soup)
    return report_entries

def deserialize_report_from_html_file(file_name: str):
    table_soup = _table_soup_from_html_file(file_name)
    report_entries = _deserialize_table_soup(table_soup)
    return report_entries

def is_logged_in(sf_sid: str) -> bool:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(500, 500)
    driver.get("https://redhatcrm.lightning.force.com/lightning")
    driver.add_cookie({'name': 'sid', 'value': sf_sid,
                       'domain': '.salesforce.com', 'path': '/'})
    SF_HOME_URL = "https://redhatcrm.lightning.force.com/lightning/page/home"
    driver.get(SF_HOME_URL)
    time.sleep(4)
    if driver.current_url == SF_HOME_URL:
        return True
    else:
        return False

def _table_soup_from_report(report_url: str, sf_sid: str) -> BeautifulSoup:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--start-maximized")  # Start maximized
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(4000, 30000)

    driver.get("https://redhatcrm.lightning.force.com/lightning")  # Initial dummy get request to set the cookie
    driver.add_cookie({'name': 'sid', 'value': sf_sid,
                       'domain': '.salesforce.com', 'path': '/'})

    driver.get(report_url)

    time.sleep(4)

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


def _table_soup_from_html_file(file_name: str) -> BeautifulSoup:
    with open(file_name, "r") as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        table_soup = soup.find(
            'table', class_='data-grid-table data-grid-full-table')
        # actually find out why this might happen (as it does randomly) and print a better error
        if not table_soup:
            raise Exception(
                "Something went wrong with reading the file, interpreting it as html, or finding a table")
        return table_soup


def _clean_text(text: str) -> str:
    stripped_text = text.strip()
    if stripped_text in ["", "-"]:
        return None
    # Replace line-breaks and tabs with a space
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # Reduce multiple spaces to a single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading and trailing spaces
    return text.strip()


def _extract_sf_id_from_link(link):
    # Regex to extract ID, flexible for content before and after
    match = re.search(r'/lightning/r/([a-zA-Z0-9]+)/view', link)
    if match:
        return match.group(1)  # Return the captured ID
    return None

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
            # Text
            header = headers[cell_index]
            cell_item_text = _clean_text(cell.get_text(strip=True))
            row_data[header] = cell_item_text
            # ID
            cell_item_a = cell.find('a')
            if cell_item_a:
                item_link = cell_item_a.get('href', None)
                cell_item_sf_id = _extract_sf_id_from_link(item_link)
                if cell_item_sf_id:
                    row_data[header+" ID"] = cell_item_sf_id
            
            
            
            

        opportunities.append(row_data)
    return opportunities

