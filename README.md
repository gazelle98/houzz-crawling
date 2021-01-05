# Houzz Scraping
By using *scrapy* library, I crawled some products. The result saved in *results.csv*. You can put categories that you want to crawl the relevant products in a text file called *selected_categories.txt*


In order to set a limit to crawling different pages of a category, you can set *to_page* parameter. To crawl the Houzz, run this command: 

```
scrapy crawl houzz -a to_page=5
```
