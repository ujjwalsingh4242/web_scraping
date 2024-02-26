import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

main = {
    'ANDAMAN & NICOBAR ISLANDS': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/113/35/{}',
    'ANDHRA PRADESH': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/3914/28/{}',
    'ARUNACHAL PRADESH': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/389/12/{}',
    
}

def scrape_ngos(url, start_page, end_page):
    """Scrape NGO data."""
    session = requests.Session()
    ngo_data = []
    
    for page_num in range(start_page, end_page + 1):
        response = session.get(url.format(page_num))
        print(response)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            table = soup.find('table', class_='table table-striped table-bordered table-hover Tax')
            rows = table.select('tbody tr')
            
            for row in rows:
                columns = row.find_all('td')
                ngo_info = {
            'Sr No.': columns[0].text.strip(),
            'Name of VO/NGO': columns[1].text.strip(),
            'Registration No.,City & State': columns[2].text.strip(),
            'Address': columns[3].text.strip(),
            'Sectors working in': columns[4].text.strip(),
        }
            ngo_data.append(ngo_info)
        else:
            print(f"Failed to fetch page {page_num}. Status code: {response.status_code}")
    return ngo_data

def save_to_csv(data, state, start_page, end_page):
    """Save data to CSV file."""
    df = pd.DataFrame(data)
    df['Instagram Page link'] = ""
    df['Facebook Page link'] = ""
    df['Linked Profile link'] = ""
    df['Remarks/additional information'] = ""
    df.to_csv(f'NGO_Data_of_{state}_from_page_{start_page}_to_{end_page}.csv', index=False)

if __name__ == "__main__":
    state = input('Enter state: ').upper()
    url = main.get(state)
    if not url:
        print("State not found in the database.")
    else:
        start_page = int(input('Enter starting page: '))
        end_page = int(input('Enter ending page: '))
        ngo_data = scrape_ngos(url, start_page, end_page)
        print(ngo_data)
        
        if ngo_data:
            save_to_csv(ngo_data, state, start_page, end_page)
            print("Data saved successfully!")
