import os
import xml.etree.ElementTree as etree
from pony import orm

import time
time.sleep(10)

db = orm.Database()

db.bind(
    'postgres',
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_PASSWORD'),
    host='db',
    database=os.environ.get('POSTGRES_DATABASE')
)


class BeerStyle(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str, 255)
    key = orm.Required(str, 5)
    beer_style_statistics = orm.Set('BeerStyleStatistic')


class BeerStyleStatistic(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    beer_style = orm.Required(BeerStyle)
    stat = orm.Required(str, 5)
    low = orm.Optional(float)
    high = orm.Optional(float)
    flexible = orm.Required(bool, sql_default='False')

db.generate_mapping(create_tables=True)


def load_data(beer_styles_xml):
    with open(beer_styles_xml, 'r') as sf:
        styles_xml = sf.read()
    with orm.db_session:
        styleguide = etree.fromstring(styles_xml)
        for _class in styleguide.findall('class'):
            if _class.get('type') != 'beer':
                continue
            categories = _class.findall('category')
            for category in categories:
                subcategories = category.findall('subcategory')
                for subcategory in subcategories:
                    bs = BeerStyle(
                        name=subcategory.find('name').text,
                        key=subcategory.get('id'))

                    stats = subcategory.find('stats')

                    ibu = stats.find('ibu')
                    if ibu is not None:
                        flexible = ibu.get('flexible') == 'true'
                        low = ibu.find('low')
                        high = ibu.find('high')
                        BeerStyleStatistic(
                            beer_style=bs,
                            stat='IBU',
                            low=low.text if low is not None else None,
                            high=high.text if high is not None else None,
                            flexible=flexible)

                    og = stats.find('og')
                    if og is not None:
                        flexible = og.get('flexible') == 'true'
                        low = og.find('low')
                        high = og.find('high')
                        BeerStyleStatistic(
                            beer_style=bs,
                            stat='OG',
                            low=low.text if low is not None else None,
                            high=high.text if high is not None else None,
                            flexible=flexible)

                    fg = stats.find('fg')
                    if fg is not None:
                        flexible = fg.get('flexible') == 'true'
                        low = fg.find('low')
                        high = fg.find('high')
                        BeerStyleStatistic(
                            beer_style=bs,
                            stat='FG',
                            low=low.text if low is not None else None,
                            high=high.text if high is not None else None,
                            flexible=flexible)

                    srm = stats.find('srm')
                    if srm is not None:
                        flexible = srm.get('flexible') == 'true'
                        low = srm.find('low')
                        high = srm.find('high')
                        BeerStyleStatistic(
                            beer_style=bs,
                            stat='SRM',
                            low=low.text if low is not None else None,
                            high=high.text if high is not None else None,
                            flexible=flexible)

                    abv = stats.find('abv')
                    if abv is not None:
                        flexible = abv.get('flexible') == 'true'
                        low = abv.find('low')
                        high = abv.find('high')
                        BeerStyleStatistic(
                            beer_style=bs,
                            stat='ABV',
                            low=low.text if low is not None else None,
                            high=high.text if high is not None else None,
                            flexible=flexible)
