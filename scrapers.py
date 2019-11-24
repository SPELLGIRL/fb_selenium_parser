from datetime import datetime

from bs4 import BeautifulSoup


class FBPostScraper(object):
    def __init__(self, html, url=None):
        self._soup = BeautifulSoup(html, "html.parser")
        self._data = {
            'url': url,
            'date': '',
            'content': {
                'text': '',
                'html': html,
            },
        }
        self.parse()

    def __str__(self):
        return self.url

    @property
    def data(self):
        return self._data

    @property
    def date(self):
        return self.data.get('date')

    @property
    def text(self):
        return self.data.get('content').get('text')

    @property
    def url(self):
        return self.data.get('url')

    def parse(self):
        """ Метод для запуска цепочки обработчиков """

        self._data['date'] = self._parse_date()
        self._data['content']['text'] = self._parse_text()

    def _parse_text(self):
        """ Метод получения текста публикации """

        elem = self._soup.select_one('div[data-testid="post_message"]')
        return elem.text if elem else ''

    def _parse_date(self):
        """ Метод получения даты публикации """

        elem = self._soup.select_one('abbr')
        return datetime.fromtimestamp(int(elem['data-utime'])) if elem else ''
