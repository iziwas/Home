# coding: utf-8
# encoding: utf-8
import requests
import dateparser
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import base64

URL_LIBRAIRIE_DE_PARIS = 'https://www.librairie-de-paris.fr/listeliv.php?' \
                         'base=paper&mots_recherche='


class LibrairieDeParis:
    _soup = False
    _url = False
    _headers = {}
    _book = {}

    def __init__(self):
        self._soup = False
        self._url = False
        self._headers = {}
        self._book = {}

    def search_book(self, isbn):
        self._url = URL_LIBRAIRIE_DE_PARIS + isbn

        self._get_source_page()

        # if we haven't data, return empty information
        if not self._soup:
            return self._book

        # if we don't have result return empty book
        if self._check_if_no_result():
            return self._book

        # Get Title information of book
        self._book['barcode'] = isbn
        self._book['name'] = self._get_title()

        # Get Summary
        self._book['summary'] = self._get_summary()

        # Get Auhtor
        self._book['author_name'] = self._get_author()

        # Get Editor
        self._book['editor_name'] = self._get_editor()

        # Get Collection
        self._book['collection_name'] = self._get_collection()

        # Get Release date
        self._book['release_date'] = self._get_release_date()

        # Get image
        self._book['image'] = self._get_image()

        return self._book

    def _get_source_page(self):
        # private method to create fake user agent
        self._create_fake_useragent()

        # request to get html page
        req = requests.get(self._url, headers=self._headers)

        # convert html page to XML
        self._soup = BeautifulSoup(req.text, "lxml")

    def _create_fake_useragent(self):
        ua = UserAgent()
        self._headers = {'user-agent': ua.random}

    def _check_if_no_result(self):
        return bool(self._soup.find('p', {'class': 'msg_no_result'}))

    def _get_title(self):
        title = self._soup.find("h2", {'class': 'livre_titre'})
        if title:
            title = title.get_text().strip()
        return title

    def _get_summary(self):
        split_resume = self._soup.find("p", {'class': 'livre_resume'})
        summary = ''
        if split_resume:
            split_resume = split_resume.get_text().split('\n')
            for i in range(0, len(split_resume) - 2):
                summary += split_resume[i].strip() if split_resume[i] else ''
        return summary

    def _get_author(self):
        book_author = self._soup.find("h2", {'class': 'livre_auteur'})
        if book_author:
            book_author = book_author.get_text().strip()
        return book_author

    def _get_editor(self):
        book_editor = self._soup.find("li", {'class': 'editeur'})
        if book_editor:
            book_editor = book_editor.get_text().strip()
        return book_editor

    def _get_collection(self):
        book_collection = self._soup.find("li", {'class': 'collection'})
        if book_collection:
            book_collection = book_collection.get_text().strip()
        return book_collection

    def _get_release_date(self):
        livre_release_date = self._soup.find("li", {'class': 'MiseEnLigne'})
        release_date = False
        if livre_release_date:
            livre_release_date = livre_release_date.get_text().strip()
            release_date = dateparser.parse(livre_release_date).date()
        return release_date

    def _get_image(self):
        self._create_fake_useragent()
        image_url = self._soup.find("img", {'class': 'lazy'})['data-original']
        return base64.b64encode(requests.get(image_url, headers=self._headers).content)
