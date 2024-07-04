from bs4 import BeautifulSoup
import requests

# Extracting the links of multiple movie transcripts


# To Get The HTML
root = 'https://subslikescript.com'  # this is the homepage of the website
website = f'{root}/movies'  # concatenating the homepage with the movies section
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())  # prints the HTML of the website

# Locate the box that contains a list of movies
box = soup.find('article', class_='main-article')

with open('links_multiple_emovies.txt', 'w') as file:
    # Store each link in "links" list
    links = []
    for link in box.find_all('a', href=True):  # find_all returns a list
        links.append(link['href'])
        file.write(str(link))


# Extracting the movie transcript

# Loop through the "links" list and sending a request to each link
for link in links:
    result = requests.get(f'{root}/{link}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    # Locate the box that contains title and transcript
    box = soup.find('article', class_='main-article')
    # Locate title and transcript
    title = box.find('h1').get_text()
    title = ''.join(title.split('/'))
    transcript_element = box.find('div', class_='full-script')
    if transcript_element:
        transcript = transcript_element.get_text(strip=True, separator=' ')
    else:
        transcript = ""

    # Exporting data in a text file
    with open(f'{title}.txt', 'w') as file:
        file.write(transcript)
