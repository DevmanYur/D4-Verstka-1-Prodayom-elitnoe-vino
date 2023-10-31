from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import pandas
import collections
import datetime
from environs import Env


def get_delta_year():
    foundation_date = datetime.datetime(year=1920, month=1, day=1)
    now_date = datetime.datetime.now()
    delta = now_date - foundation_date
    seconds = delta.total_seconds()
    years = seconds / 60 / 60 / 24 / 365
    return int(years)


def get_ending_year(year):
    remains_100 = year % 100
    remains_10 = remains_100 % 10
    if (remains_100 == 11) or (remains_100 == 12) or (remains_100 == 13) or (remains_100 == 14):
        return "лет"
    elif remains_10 == 1:
        return "год"
    elif (remains_10 == 2) or (remains_10 == 3) or (remains_10 == 4):
        return "года"
    else:
        return "лет"


def main():
    glogal_env = Env()
    glogal_env.read_env()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    try:
        products_from_file = pandas.read_excel(io=glogal_env.str('FILE'),
                                               keep_default_na=False
                                               )
    except FileNotFoundError:
        products_from_file = pandas.read_excel(io='wine3.xlsx',
                                               keep_default_na=False
                                               )
        print("Путь к файлу не найден")

    all_products = products_from_file.to_dict(orient='records')
    products = collections.defaultdict(list)
    for product in all_products:
        products[product["Категория"]].append(product)

    rendered_page = template.render(
        products=products,
        delta_year=get_delta_year(),
        ending_year=get_ending_year(get_delta_year())
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()

