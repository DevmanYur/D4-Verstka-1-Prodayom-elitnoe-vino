from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import pandas
import collections
import datetime

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


file_pandas = pandas.read_excel(io = 'wine3.xlsx', 
                                sheet_name='Лист1',
                                na_values='znachenie_nan',
                                keep_default_na=False
                               )

list_all_products = file_pandas.to_dict(orient='records')


dict_with_products = collections.defaultdict(list)
for dict in list_all_products:
    dict_with_products[dict["Категория"]].append(dict)


def get_delta_year():
    date_foundation = datetime.datetime(year=1920,month=1, day=1)
    date_now = datetime.datetime.now()
    delta = date_now - date_foundation
    seconds = delta.total_seconds()
    years = seconds / 60 / 60 / 24 / 365
    return int(years)


def get_ending_year(year):
    remains_100 = year%100
    remains_10 = remains_100%10
    if ((remains_100 == 11) or (remains_100 == 12) or (remains_100 == 13) or (remains_100 == 14)):
        return "лет"
    elif (remains_10 == 1):
        return "год"
    elif ((remains_10 == 2) or (remains_10 == 3) or (remains_10 == 4)):
        return "года"
    else:
        return "лет"


rendered_page = template.render(
    dict_with_products = dict_with_products,
    delta_year = get_delta_year(),
    ending_year = get_ending_year(get_delta_year())
)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()