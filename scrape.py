import os
import requests
from datetime import date
from bs4 import BeautifulSoup

URL = 'https://www.moh.gov.sg/covid-19'
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'covid-sg-stats.csv')


def save_covid_stats_to_csv(stats):
    file_exists = os.path.isfile(OUTPUT_FILE)
    today_date = date.today().isoformat()
    with open(OUTPUT_FILE, 'a') as f:
        if not file_exists:
            f.write('Date,Total number of imported cases,Active cases,' +
                    'Discharged,Vaccine at least first dose,' +
                    'Vaccine completed,Vaccine total doses,' +
                    'Total swabs tested\n')
        f.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (
            today_date,
            stats['cases_imported'],
            stats['cases_active'],
            stats['cases_discharged'],
            stats['vaccine_first_dose'],
            stats['vaccine_completed'],
            stats['vaccine_total_doses'],
            stats['swab_tests_total']
        ))


def get_content():
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    content = (soup
               .find('section', class_='body-content')
               .find_all('div', class_='sfContentBlock'))
    return content


def get_stats(content):
    def parse_content(soup, split=None):
        text = soup.find_all('td')[1].text
        if split:
            text = text.split(split)[0]
        text = text.replace(',', '')
        return int(text)

    cases_imported = parse_content(content[1], '\xa0')
    cases_active = parse_content(content[3])
    cases_discharged = parse_content(content[4])
    vaccine_first_dose = parse_content(content[11])
    vaccine_completed = parse_content(content[12])
    vaccine_total_doses = parse_content(content[13])
    swab_tests_total = parse_content(content[15])

    return {
        'cases_imported': cases_imported,
        'cases_active': cases_active,
        'cases_discharged': cases_discharged,
        'vaccine_first_dose': vaccine_first_dose,
        'vaccine_completed': vaccine_completed,
        'vaccine_total_doses': vaccine_total_doses,
        'swab_tests_total': swab_tests_total
    }


if __name__ == '__main__':
    content = get_content()
    stats = get_stats(content)
    save_covid_stats_to_csv(stats)
