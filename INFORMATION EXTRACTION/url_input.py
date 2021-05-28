import requests
from bs4 import BeautifulSoup

def get_url(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup

def get_information(soup):
    information = []

    title = soup.h1.text
    information.append(title)

    try:
        detail = soup.find("div", {"class": "detail text-content"}).text
    except:
        detail = soup.find("div", {"class": "detail"}).text
    information.append(detail)

    moreinfor = soup.find("div", {"class": "moreinfor"})
    moreinfor = [ele.text.replace("²", "2") for ele in moreinfor if ele.text != '']
    moreinfor = '\n'.join(moreinfor)
    information.append(moreinfor)
    
    address = soup.find("div", {"class": "address"}).text
    information.append(address)
    
    moreinfor1 = soup.find('table').find_all('td')
    data = [ele.text for ele in moreinfor1]
    data = [' '.join(i) for i in zip(data[::2], data[1::2])]
    information.append('\n'.join(data))

    return '\n'.join(information)

def main(url):
    soup = get_url(url)
    return get_information(soup)

# if __name__ == "__main__":
#     url = input()
#     soup = get_url(url)
#     output = get_information(soup)
#     print(output)
