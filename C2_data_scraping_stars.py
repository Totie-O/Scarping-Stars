import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def main():
    response = requests.get('https://hk.space.museum/sc/web/spm/resources/teachers-corner/constellations-and-myths/glossary-of-bright-stars.html')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        div_main = soup.find('div', id='main')
        data_rows = []
        for table in div_main.find_all('table'):
            for tbody in table.find_all('tbody'):
                for tr in tbody.find_all('tr'):
                    row = [td.text for td in tr.find_all('td')]
                    data_rows.append(row)

        column_names = ['name_with_suffix', 'in_cos_index', 'cons_abbr', 'name_cn', 'magnitude', 'note']
        df = pd.DataFrame(data_rows, columns=column_names)

        df['top20'] = np.where(df['name_with_suffix'].str.endswith('**'), 'yes', 'no')
        df['commonly_used'] = np.where(df['name_with_suffix'].str.endswith(' *'), 'yes', 'no')
        df['name'] = [s.split(r' *', 1)[0].strip() for s in df['name_with_suffix']]
        df['name_cn'] = [s.replace(' ', '') for s in df['name_cn']] 

        df.to_csv('assets/stars.csv')


if __name__ == '__main__': main()