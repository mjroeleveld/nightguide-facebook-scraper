# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
from facebook_scraper.lib.parse_dates import parse_date
from scrapy.utils.markup import remove_tags


class FacebookEvent(scrapy.Item):
    venue_id = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    dates = scrapy.Field()
    description = scrapy.Field()
    organiser_name = scrapy.Field()
    location_name = scrapy.Field()
    image = scrapy.Field()
    interested_count = scrapy.Field()
    going_count = scrapy.Field()
    pass


def format_dates(self, dates):
    def formatter(d):
        return d.isoformat()

    def iterator(date):
        val = {'from': formatter(date[0])}
        if len(date) == 2:
            val['to'] = formatter(date[1])
        return val

    return list(map(iterator, [x for x in dates if x is not None]))


def dates_in(self, dates, loader_context):
    def filter_non_dates(item):
        lower = item.lower()
        # Every Thursday, until 28 Jun
        if "every" in lower:
            return False
        # 3 more dates
        if "dates" in lower:
            return False
        # +7 more times
        if "times" in lower:
            return False
        return True

    timezone = loader_context.get('timezone')
    sanitized = map(remove_tags, dates)
    filtered = filter(filter_non_dates, sanitized)
    parsed = map(lambda item: parse_date(item, timezone), filtered)
    return list(parsed)


class FacebookEventLoader(ItemLoader):
    default_output_processor = TakeFirst()

    description_in = Join('/n')

    dates_in = dates_in
    dates_out = format_dates