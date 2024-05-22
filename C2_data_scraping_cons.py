import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def scraper_cn():
    response = requests.get('https://zh.wikipedia.org/zh-hans/%E6%98%9F%E5%BA%A7%E5%88%97%E8%A1%A8')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('div', class_='mw-content-ltr mw-parser-output').find('table')

        column_names = ['name_cn', 'abbr_upper', 'name', 'area', 'ra', 'dec', 'quadrant', 'family', 'bs', 'sg']
        data_rows = []
        for tr in table.tbody.find_all('tr')[1:]:
            row = [td.text for td in tr.find_all('td')]
            data_rows.append(row)
        df = pd.DataFrame(data_rows, columns=column_names)

        return df.join(df.bs.str.extract(r'(?P<bs_name_bayer_cn>.*)\((?P<bs_name_cn>.*)\)'))
    else:
        return pd.DataFrame()
    

def clean_en(str):
    return re.split(r'/|\[|\n', str, maxsplit=1)[0].strip()

def scraper_en():
    response = requests.get('https://en.wikipedia.org/wiki/IAU_designated_constellations')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('div', class_='mw-content-ltr mw-parser-output').find('table')

        column_names = ['name', 'abbr_iau', 'abbr_nasa', 'genitive', 'origin', 'meaning', 'bs_name']
        data_rows = []
        for tr in table.tbody.find_all('tr')[2:]:
            row = [td.text.strip() for td in tr.find_all('td')]
            data_rows.append(row)
        df = pd.DataFrame(data_rows, columns=column_names)

        df['name'] = df['name'].apply(clean_en)
        df['genitive'] = df['genitive'].apply(clean_en)
        df['bs_name'] = df['bs_name'].apply(clean_en)
        return df
    else:
        return pd.DataFrame()
    

def main():
    df_cn = scraper_cn()
    df_en = scraper_en()

    if not df_cn.empty and not df_en.empty:
        df_en['abbr_upper'] = df_en['abbr_iau'].str.upper()
        df = pd.merge(df_en[['name', 'abbr_iau', 'abbr_nasa', 'abbr_upper', 'meaning', 'bs_name']], 
                      df_cn[['abbr_upper', 'name_cn', 'area', 'ra', 'dec', 'quadrant', 'family', 'bs_name_bayer_cn', 'bs_name_cn']],
                      on='abbr_upper')
        
        df.to_csv('assets/cons.csv')

if __name__ == '__main__': main()