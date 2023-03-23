import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re

def get_parents(celebname):
    celebname = celebname.title()
    if " " in celebname:
        name = "_".join(celebname.split(" "))
    else:
        name = celebname

    # URL of the Wikipedia page to scrape
    url = f'https://en.wikipedia.org/wiki/{name}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    redirected_url = driver.current_url

    driver.close()

    # Make a request to the webpage and store the HTML in a variable
    html = requests.get(redirected_url).text
    

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    answer = ''
    # Find the table with the class "infobox biography vcard"
    table = soup.find('table', {'class': 'infobox biography vcard'})
    if table is None:
        table = soup.find('table', {'class': 'infobox vcard'})

    options = ['Parents', 'Parent', 'Parent(s)']
    parent_row = None
    for option in options:
        try:
            parent_row = table.find('th', text=option)
            if parent_row is not None:
                break
        except:
            continue

    parent_string = ''
    if parent_row is not None:
        # Find the cell in the row that contains the links
        parent_cell = parent_row.find_next_sibling('td', class_='infobox-data')
        # Find all the links in the cell
        parent_links = parent_cell.find_all('a', href=re.compile('^/wiki'))
        # Add the number of links to the overall link count
        link_count = len(parent_links)

    
        # Print the number of links
        answer += f'{celebname} has {link_count} blue-linker parent(s):'

        # Print the names of the linked parents
        
        if parent_links is not None:
            parent_names = [link.text for link in parent_links]
            if parent_names:
                if link_count == 1:
                    parent_string = parent_names[0]
                elif link_count == 2:
                    parent_string = " and ".join(parent_names)
                else:
                    parent_string = ", ".join(parent_names[:-1])
                    parent_string += " and " + parent_names[-1]

            
        answer += '\n' + parent_string

        if parent_row is not None:
            if link_count >= 1:
                babystatus = '--confirmed nepo baby--'
            else: 
                babystatus = '--not a nepo baby--'
        answer += '\n' + babystatus
    return answer



def get_momdad(celebname):
    celebname = celebname.title()
    if " " in celebname:
        name = "_".join(celebname.split(" "))
    else:
        name = celebname
    # URL of the Wikipedia page to scrape
    url = f'https://en.wikipedia.org/wiki/{name}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    redirected_url = driver.current_url
    driver.close()
    

    # Make a request to the webpage and store the HTML in a variable
    html = requests.get(redirected_url).text

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    answer = ''
    options = ['infobox biography vcard', 'infobox vcard']
    
    # Find the table with the class "infobox biography vcard"
    for option in options:
        try:
            table = soup.find('table', {'class': option})       
        except:
            continue  

    options = ['Father','Dad']
    # Find the row with the label "Parent(s)"
    father_row = None
    father_count = 0
    for option in options:
        try:
            father_row = table.find('th', text=option)
            if father_row is not None:
                break
        except:
            continue 

    if father_row is not None:
        # Find the cell in the row that contains the links
        father_cell = father_row.find_next_sibling('td', class_='infobox-data')
        # Find all the links in the cell
        father_links = father_cell.find_all('a', href=re.compile('^/wiki'))
        # Add the number of links to the overall link count
        father_count = len(father_links)


    options = ['Mother','Mom']
    mother_row = None
    # Find the row with the label "Parent(s)"
    for option in options:
        try:
            mother_row = table.find('th', text = option)
            if mother_row is not None:
                break
        except:
            continue 

    if mother_row is not None:
        # Find the cell in the row that contains the links
        mother_cell = mother_row.find_next_sibling('td', class_='infobox-data')
        # Find all the links in the cell
        mother_links = mother_cell.find_all('a', href=re.compile('^/wiki'))
        # Add the number of links to the overall link count
        mother_count = len(mother_links)
    

    if mother_row is not None and father_row is not None:
        answer += f'{celebname} has {father_count + mother_count} blue-linker parent(s):'

    if mother_row is not None and father_row is not None:
        mother_names = [link.text for link in mother_links]
        father_names = [link.text for link in father_links]
        mother_string = ", ".join(mother_names[:-1])
        mother_string += " and " + mother_names[-1]
        father_string = ", ".join(father_names[:-1])
        father_string += " and " + father_names[-1]

        if mother_count == 1 and father_count == 1:
            doublestring = f"{mother_names[0]} and {father_names[0]}"
        elif mother_count == 2 and father_count == 2:
            doublestring = f"{' and '.join(mother_names)} and {' and '.join(father_names)}"
        elif mother_count == 1 and father_count > 1:
            doublestring = f" {mother_names[0]} and {father_string}"
        elif father_count == 1 and mother_count > 1:
            doublestring = f"{father_names[0]} and {mother_string}"
        else:
            doublestring = f"{mother_string} and {father_string}"
        answer += '\n' + doublestring
    if mother_row is not None and father_row is not None:
        if father_count + mother_count >= 1:
            babystatus = '--confirmed nepo baby--'
        else: 
            babystatus = '--not a nepo baby--'
        answer += '\n' + babystatus
    return answer



def get_relatives(celebname: str):
    celebname = celebname.title()
    if " " in celebname:
        name = "_".join(celebname.split(" "))
    else:
        name = celebname
    # URL of the Wikipedia page to scrape
    
    
    url = f'https://en.wikipedia.org/wiki/{name}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    redirected_url = driver.current_url

    driver.close()

    # Make a request to the webpage and store the HTML in a variable
    html = requests.get(redirected_url).text

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table with the class "infobox biography vcard"
    table = soup.find('table', {'class': 'infobox biography vcard'})
    
    answer = ''

    options = ['Relatives', 'Relative(s)','Family']
    # Find the row with the label "Parent(s)"
    
    for option in options:
        try:
            relatives_row = table.find('th', text=option)
        except:
            continue
        
        if relatives_row is not None:
            relatives_row = relatives_row.find_parent('tr')
            # Find the cell in the row that contains the links
            relatives_cell = relatives_row.find('td')
            # Find all the links in the cell
            
            relatives_links = relatives_cell.find_all('a', href=re.compile('^/wiki'))
            # Count the number of links
            link_count = len(relatives_links)

            
            # Print the number of links
            answer += f'\n\nand {link_count} blue-linker relative(s):'

            # Print the names of the linked parents
            for link in relatives_links:
                relatives_names = [link.text for link in relatives_links]
            if link_count == 1:
                relnames = relatives_names[0]
            elif link_count == 2:
                relnames = " and ".join(relatives_names)
            else:
                relatives_string = ", ".join(relatives_names[:-1])
                relatives_string += " and " + relatives_names[-1]
                relnames = relatives_string
            answer += '\n' + relnames
    return answer
    

    



        
        
