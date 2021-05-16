# coding: utf-8
# encoding: utf-8
import requests
from odoo import models, fields
from odoo.exceptions import ValidationError
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from PIL import Image
from datetime import datetime
import locale

URL_LIBRAIRIE_DE_PARIS = 'https://www.librairie-de-paris.fr/listeliv.php?' \
                         'base=paper&mots_recherche='


class CollectionWizardLibrairieDeParis(models.TransientModel):
    _name = 'collection.wizard.product.librairie.de.paris'
    _description = "Wizard to add books with 'Librairie de Paris' information"
    _soup = False

    isbn = fields.Char(string=u"ISBN", size=13, required=True)

    def add_book(self):
        url = URL_LIBRAIRIE_DE_PARIS + self.isbn
        headers = {'user-agent': self._get_fake_useragent()}
        req = requests.get(url, headers=headers)
        self._soup = BeautifulSoup(req.text, "lxml")

        if not self._soup:
            raise ValidationError('No result with BeautifoulSoup')

        # Check if we have a result
        self._check_if_no_result()

        book = {}

        # Get Title information of book
        book.append({'name': self._get_title()})

        # Get Summary
        book.append({'summary': self._get_summary()})

        # Get Auhtor
        author_name = self._get_author()
        author = self.env['res.partner'].search([('name', 'ilike', author_name)])
        if not author:
            author = self.env['res.partner'].create({
                'name': author_name,
                'categ_id': self.env.ref('collection.partner_category_author')
            })
        book.append({'author_id': author.id})

        # Get Editor
        editor_name = self._get_editor()
        editor = self.env['res.partner'].search([('name', 'ilike', editor_name)])
        if not editor:
            editor = self.env['res.partner'].create({
                'name': author_name,
                'categ_id': self.env.ref('collection.partner_category_editor')
            })
        book.append({'editor_id': editor.id})

        # Get Collection
        collection_name = self._get_collection()
        collection = self.env['collection.collection'].search(
            [('name', 'ilike', editor_name)])
        if not collection:
            collection = self.env['collection.collection'].create({
                'name': collection_name,
            })
        book.append({'collection_id_id': collection.id})


    def _check_if_no_result(self):
        no_result = self._soup.find('p', {'class': 'msg_no_result'})
        if no_result:
            raise ValidationError(no_result.get_text().strip())

    def _get_fake_useragent(self):
        ua = UserAgent()
        return ua.random

    def _get_title(self):
        title = self._soup.find("h2", {'class': 'livre_titre'})
        if title:
            title = title.get_text().strip()
        return title

    def _get_summary(self):
        split_resume = self._soup.find("p", {'class': 'livre_resume'}).get_text().split('\n')
        summary = False
        for i in range(0, len(split_resume) - 2):
            summary += split_resume[i].strip()
        return summary

    def _get_author(self):
        book_author = self._soup.find("h2", {'class': 'livre_auteur'})
        if book_author:
            book_author = book_author.get_text().strip()
        return book_author

    def _get_editor(self):
        book_editor = self._soup.find("h2", {'class': 'livre_auteur'})
        if book_editor:
            book_editor = book_editor.get_text().strip()
        return book_editor

    def _get_collection(self):
        book_collection = self._soup.find("li", {'class': 'collection'})
        if book_collection:
            book_collection = book_collection.get_text().strip()
        return book_collection