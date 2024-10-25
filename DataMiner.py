import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Function to extract Service Titles
def get_service_title(soup):
    try:
        # Find all <h2> tags 
        first = soup.find_all("div", attrs = {'class' : 'text-box layout-element__component layout-element__component--GridTextBox'})
        temp = []
        titles_list = []
        for div in first:
        # Find the <h2> tag inside each div
            h5_tag = div.find("h5")
            if h5_tag :
                temp.append(h5_tag)
        for h5 in temp:
            strong = h5.find("strong")
            if strong:
                titles_list.append(strong.string.strip())
        print(titles_list)
        
    except AttributeError:
        titles_list = []
    return titles_list

# Function to extract Service Descriptions
def get_service_description(soup, lent):
    try:
        # Find all <p> tags under the service section
        descriptions = soup.find_all("p", attrs={'class':'body'}, limit=lent)
        descriptions_list = [desc.text.strip() for desc in descriptions if desc.text]
    except AttributeError:
        descriptions_list = []
    return descriptions_list

if __name__ == '__main__':

    HEADERS = ({
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36', 'Accept-Language':'en-US, en;q=0.5'
        })

    URL = "https://www.cipherbytetechnologies.com/services"

    webpage = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "html.parser")

    services = get_service_title(soup)
    descriptions = get_service_description(soup, len(services))

    data = {"Service": services[:len(services)-1], "Description": descriptions[1:len(descriptions)]}

    # Save the data to a CSV file
    cipherbyte_df = pd.DataFrame.from_dict(data)
    cipherbyte_df.to_csv("cipherbyte_services.csv", header=True, index=False)

    print("Data scraped and saved to cipherbyte_services.csv")
    print(cipherbyte_df)