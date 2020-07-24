import re
import scrapy


class ZiseaspiderSpider(scrapy.Spider):
    name = 'zisea'

    def start_requests(self):
        unicode_ranges = \
            ( (0x4e00, 0x9ffc)
            , (0x3400, 0x4dbf)
            , (0x20000, 0x2a6dd)
            , (0x2a700, 0x2b734)
            , (0x2b740, 0x2b81d)
            , (0x2b820, 0x2cea1)
            , (0x2ceb0, 0x2ebe0)
            , (0x30000, 0x3134a)
            )

        for lower, upper in unicode_ranges:
            for code_point in range(lower, upper + 1):
                url = 'http://zisea.com/zscontent.asp?uni=%X' % code_point
                yield scrapy.Request(url=url, callback=self.parse, meta={'code_point': code_point})

    def parse(self, response):
        text = response.css('td[style="FONT-SIZE: 10em;"] + td').get()
        regex = r'两分字元：(?P<lfzy>[^\n]+)\n.+?字形描述：(?P<zxms>[^<]+)<br>.+?提交来源：(?P<tjly>[^<]+)'
        match = re.search(regex, text, re.DOTALL)
        yield \
            { 'cp': '%X' % response.meta['code_point']
            , 'lfzy': match['lfzy']
            , 'zxms': match['zxms']
            , 'tjly': match['tjly']
            }
