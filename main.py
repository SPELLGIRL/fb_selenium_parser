from crawlers import FBCrawler


def debug_print(data):
    for i in data:
        print(i)


if __name__ == '__main__':
    crawler = FBCrawler()
    try:
        find = input('Поисковый запрос: ')
        post_urls = crawler.get_post_urls(find)
        parsed_data = crawler.get_parsed_data(post_urls)
        debug_print(parsed_data)
    finally:
        crawler.close()
