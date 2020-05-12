# pip install requests BeautifulSoup4 matplotlib

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


html = BeautifulSoup(simple_get("http://www.inumeraveis.com.br"), 'html.parser')

idades = {}

for item in html.select('h4 span'):
    ano = int(item.text.replace(' anos', ''))
    if ano not in idades.keys():
        idades[ano] = 1
        continue
    idades[ano] = idades.get(ano) + 1

idades = sorted(idades.items(), key=lambda x: x[0])
print(idades)
xIdade = []
yQtd = []
for key, value in idades:
    print(f'Idade: {key} Ocorrências: {value}')
    xIdade.append(int(key))
    yQtd.append(int(value))


def createGraphic(xIdade, yQtd, idades):
    plt.plot(xIdade, yQtd, 'bo--', label='mortes por idade', linewidth=1)
    plt.xlabel('x - idade')
    plt.ylabel('y - quantidade')
    plt.title('Quantidade de mortes por idade - COVID-19')
    plt.legend()
    plt.show()


createGraphic(xIdade, yQtd, idades)
