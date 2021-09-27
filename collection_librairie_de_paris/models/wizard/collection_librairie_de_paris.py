# coding: utf-8
# encoding: utf-8
import requests
import dateparser
from odoo import models, fields, tools
from odoo.exceptions import ValidationError
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
import locale
import base64
from odoo.modules.module import get_module_resource


URL_LIBRAIRIE_DE_PARIS = 'https://www.librairie-de-paris.fr/listeliv.php?' \
                         'base=paper&mots_recherche='


class CollectionWizardLibrairieDeParis(models.TransientModel):
    _name = 'collection.wizard.librairie.de.paris'
    _description = "Wizard to add books with 'Librairie de Paris' information"
    _soup = False

    isbn = fields.Char(string=u"ISBN", size=13, required=True)
    is_ebook = fields.Boolean(string="Est un Ebook ?", default=False, required=True)

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
        book['barcode'] = self.isbn
        book['name'] = self._get_title()

        # Get Summary
        book['summary'] = self._get_summary()

        # Get Auhtor
        author_name = self._get_author()
        author = self.env['res.partner'].search([('name', 'ilike', author_name)])
        if not author:
            image_name = 'author.png'
            image_path = get_module_resource('collection', 'static/src/img', image_name)
            image = tools.image_resize_image_big(base64.b64encode(
                open(image_path, 'rb').read()))

            author = self.env['res.partner'].create({
                'name': author_name,
                'partner_category_id': 
                    self.env.ref('collection.partner_category_author').id,
                'image': image,
            })
        book['author_id'] = author.id

        # Get Editor
        editor_name = self._get_editor()
        if editor_name:
            editor = self.env['res.partner'].search([('name', 'ilike', editor_name)])
            if not editor:
                image_name = 'publisher.png'
                image_path = get_module_resource('collection', 'static/src/img',
                                                 image_name)
                image = tools.image_resize_image_big(base64.b64encode(
                    open(image_path, 'rb').read()))

                editor = self.env['res.partner'].create({
                    'name': editor_name,
                    'partner_category_id':
                        self.env.ref('collection.partner_category_editor').id,
                    'image': image,
                })
            book['editor_id'] = editor.id

        # Get Collection
        collection_name = self._get_collection()
        collection = self.env['collection.collection'].search(
            [('name', 'ilike', editor_name)])
        if not collection:
            collection = self.env['collection.collection'].create({
                'name': collection_name,
            })
        book['collection_id'] = collection.id

        # Get Release date
        book['release_date'] = self._get_release_date()

        # Get image
        book['image'] = self._get_image()

        # Create book
        book['categ_id'] = self.env.ref('collection.product_category_ebook').id if self.is_ebook else \
            self.env.ref('collection.product_category_ebook').id

        self.env['product.product'].create(book)

        return {'type': 'ir.actions.client', 'tag': 'reload'}


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
        image_url = self._soup.find("img", {'class': 'lazy'})['data-original']
        headers = {'user-agent': self._get_fake_useragent()}
        return base64.b64encode(requests.get(image_url, headers=headers).content)
