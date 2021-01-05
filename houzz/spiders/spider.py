import scrapy
import datetime
from houzz.items import HouzzItem


class HouzzSpider(scrapy.Spider):
    name = 'houzz'

    def start_requests(self):
        urls = []
        with open('selected_categories.txt', 'r') as file:
            for category in file:
                category = category.rstrip()
                urls.append((
                    category,
                    f'https://www.houzz.com/products/{category}'
                ))
        self.to_page = None

        for url in urls:
            yield scrapy.Request(
                url=url[1], callback=self.parse, meta={'category': url[0]}
            )

    def parse(self, response):
        product_urls = response.css(".hz-product-card a::attr(href)").extract()
        page = response.css(
            ".hz-pagination-link--selected ::text"
            ).extract_first()

        category = response.meta['category']

        for url in product_urls:
            yield scrapy.Request(
                url=response.urljoin(url),
                callback=self.parse_product,
                meta={'page': page, 'category': category}
                )

        next_page = response.css(
            ".hz-pagination-bottom .hz-pagination-link--next ::attr(href)"
            ).extract_first()

        count_per_page = int(response.css(
                '.hz-dropdown__custom--label::text'
            ).extract()[-1].split()[0])

        if self.to_page is None:
            all_results_count = int(response.css(
                '.hz-br-resultset__total-results ::text'
            ).extract_first().replace(',', ''))

            # Set default to_page according to the whole pages exist
            self.to_page = all_results_count // count_per_page + 1

        nextp = int(next_page.split('/')[-1]) // count_per_page + 1

        if int(page) < self.to_page and nextp <= self.to_page:
            yield scrapy.Request(
                url=response.urljoin(next_page), callback=self.parse
                )

    def parse_product(self, response):
        item = HouzzItem()
        item['url'] = response.request.url
        item['page'] = response.meta['page']
        item['name'] = response.css(
            ".hz-view-product-title .view-product-title ::text"
            ).extract_first()
        item['tag'] = response.css(
            ".product-keywords .product-keywords__word::text"
            ).extract()
        images = response.css(
            ".alt-images__thumb img::attr(src)"
        ).extract()[0:2]
        item['datetime'] = str(datetime.datetime.now())
        item['category'] = response.meta['category']

        try:
            item['image_1'] = images[0]
            item['image_2'] = images[1]

        except:
            item['image_1'] = response.css(
                ".view-product-image img::attr(style)"
                ).re_first(r'url\(([^\)]+)')

        yield item
