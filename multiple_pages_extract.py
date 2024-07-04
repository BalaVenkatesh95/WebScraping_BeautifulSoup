from bs4 import BeautifulSoup
import requests

# Extracting links from pagination bar

# To Get The HTML
root = 'https://subslikescript.com'
website = f'{root}/movies_letter-X'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')

# Locate the box that contains the pagination bar
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

# Extracting the links of multiple movie transcripts inside each page listed

# Loop through all tbe pages and sending a request to each link
for page in range(1, int(last_page)+1):
    result = requests.get(f'{website}?page={page}')
    # structure --> https://subslikescript.com/movies_letter-X?page=2
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    # Locate the box that contains a list of movies
    box = soup.find('article', class_='main-article')

    with open('links_multiple_pages.txt', 'w') as file:
        # Store each link in "links" list (href doesn't consider root aka "homepage", so we have to concatenate it later)
        links = []
        for link in box.find_all('a', href=True):  # find_all returns a list
            links.append(link['href'])
            file.write(str(link))

    # Extracting the movie transcript

    for link in links:
        try:
            result = requests.get(f'{root}/{link}')
            # structure --> https://subslikescript.com/movie/X-Men_2-290334
            content = result.text
            soup = BeautifulSoup(content, 'lxml')

            # Locate the box that contains title and transcript
            box = soup.find('article', class_='main-article')
            # Locate title and transcript
            title = box.find('h1').get_text()
            transcript_element = box.find('div', class_='full-script')
            if transcript_element:
                transcript = transcript_element.get_text(strip=True, separator=' ')
            else:
                transcript = ""  # or handle the case where the element is not found

            # Exporting data in a text file
            with open(f'{title}.txt', 'w') as file:
                file.write(transcript)
        except:
            print('------ Link not working -------')
            print(link)
