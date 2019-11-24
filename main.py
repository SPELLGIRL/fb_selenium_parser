from crawlers import FBCrawler


def debug_print(data):
    """ Функция для отображения результата в консоли """

    for post in data:
        date = post.date.strftime("%Y-%m-%d") if post.date else "Unknown"
        print(f'{date}\n{post.url}\n{post.text}\n')


if __name__ == '__main__':
    crawler = FBCrawler()
    try:
        find = input('Поисковый запрос: ')
        post_urls = crawler.get_post_urls(find)
        parsed_data = crawler.get_parsed_data(post_urls)
        debug_print(parsed_data)
    finally:
        crawler.close()
