# pip install requests BeautifulSoup4 matplotlib

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


# --- STEP 01: Get the html ---
def simple_get(url):
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
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


html = BeautifulSoup(simple_get("https://inumeraveis.com.br/"), 'html.parser')

# --- STEP 02: Collect and sort the data ---
ages = {}

for item in html.select('h4 span'):
    ano = int(item.text.replace(' anos', ''))
    if ano not in ages.keys():
        ages[ano] = 1
        continue
    ages[ano] = ages.get(ano) + 1

ages = sorted(ages.items(), key=lambda x: x[0])
print(ages)
xAge = []
yCount = []
for key, value in ages:
    print(f'Idade: {key} Ocorrências: {value}')
    xAge.append(int(key))
    yCount.append(int(value))


# --- STEP 03: Plot the graphic ---
def createGraphic(xAge, yCount):
    fig, ax = plt.subplots()
    plt.bar
    ax.bar(xAge, yCount, align='center', alpha=0.5)
    ax.set_xlabel('x - idade')
    ax.set_ylabel('y - quantidade')
    plt.title('Quantidade de mortes por idade - COVID-19')
    ax.xaxis.set_ticks(xAge)
    ax.yaxis.set_ticks(yCount)
    ax.legend()
    plt.gca().margins(x=0)
    plt.gcf().canvas.draw()
    tl = plt.gca().get_xticklabels()
    maxsize = max([t.get_window_extent().width for t in tl])
    m = 0.4
    s = maxsize / plt.gcf().dpi * len(xAge) + 15 * m
    margin = m / plt.gcf().get_size_inches()[0]
    plt.gcf().subplots_adjust(left=margin, right=1. - margin)
    plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
    plt.show()


createGraphic(xAge, yCount)
