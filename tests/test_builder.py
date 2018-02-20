import os.path
from xml.etree.ElementTree import Element

from django import setup
from jinja2 import Template

from invoice_generator import builder
from tests.ModelsAssets import ModelsAssets
from tests.TestUtils import TestUtils

HERE = os.path.dirname(__file__)


class TestBuilder(TestUtils, ModelsAssets):
    def setUp(self):
        setup()

    def generate_wrapper(self, currency='€', invoice=None, **kwargs):

        invoice = invoice or self.invoice()
        pdf = builder.generate_pdf(currency, invoice, **kwargs)

        return pdf

    def test_custom_template(self):
        tpl_path = os.path.join(HERE, 'templates', 'index.html')

        with open(tpl_path) as fp:
            tpl = Template(fp.read())

        pdf = self.generate_wrapper(template=tpl)
        title = pdf.wrapper_element.query('title')
        paragraph = pdf.wrapper_element.query('body p')

        self.assertIsNotNone(paragraph)

        element = paragraph.etree_element  # type: Element
        self.assertEqual(element.text, 'Test template')

        self.assertEqual(title.etree_element.text, 'It\'s a test.')

    def test_no_given_template(self):
        wrapper = self.generate_wrapper()
        title = wrapper.wrapper_element.query('head title')

        self.assertIsNotNone(title)

        element = title.etree_element  # type: Element
        self.assertStrippedEqual('Invoice INV0001', element.text)

    def test_localization(self):
        pass

    def test_render_css(self):
        wrapper = self.generate_wrapper()
        doc = wrapper.wrapper_element
        css = doc.query('html head style').etree_element.text

        # test if information about vendor are here
        self.assertStrippedMultiIn(
            (
                'content: "Henry H. Rice" "\\a"',
                '"159 Hornor Avenue" "\\a"',
                '"74119 Tulsa, OK" "\\a"',
                '"VAT Number: VT000112" "\\a"',
                '"\\a" "\\a"',
                '}'
            ), css)

        # test if additional information are here
        self.assertStrippedMultiIn(
            (
                'content:  "Additional Information" "\\a" '
                '"test + email" "\\a" "HenryHRice@example.org" "\\a"',

                '"\\a" "\\a" "\\a"'
            ), css)

        # test if information about the executive are here
        self.assertStrippedMultiIn(
            (
                'content: "Management Board" "\\a"',
                '"Ruth W. Blatt" "\\a"',
                '"RuthWBlatt@example.org" "\\a"',
                '"\\a\\a\\a"',
                '}',
            ), css)

    def test_render_invoice_info(self):
        wrapper = self.generate_wrapper()
        doc = wrapper.wrapper_element
        data = doc.query_all('table.infoTable tr td')

        expected_data = (
            'Order ID: INV0001',
            'Customer ID: ORD0002',
            'Date of Invoice: Feb. 20, 2018',
        )

        found = 0

        for node in data:
            text = node.etree_element.text
            if text:
                if text.strip() in expected_data:
                    found += 1

        self.assertEqual(len(expected_data), found)

    def test_render_order_info(self):
        cells = (
            ('reference', str),
            ('text', str),
            ('quantity', str),
            ('net_price', lambda x: '%.2f €' % x),
            ('tax_rate', lambda x: '%d %%' % x),
            ('total_net', lambda x: '%.2f €' % x),
        )
        
        items, order = self.random_items()
        invoice = self.invoice(*items, order_data=order)
        wrapper = self.generate_wrapper(invoice=invoice)

        doc = wrapper.wrapper_element
        rows = doc.query_all('table.invoiceTable tbody tr:not(.tfoot)')

        for i, row in enumerate(rows):
            self.assertLess(i, len(items), 'Got more items than expected.')

            item = items[i]
            for cell_pos, cell in enumerate(row.query_all('td')):
                cell = cell.etree_element.text
                self.assertLess(
                    cell_pos, len(cells),
                    'Got an unexpected cell in product %d.' % i
                )

                attr, transformer = cells[cell_pos]
                self.assertEqual(
                    transformer(getattr(item, attr)), cell.strip())
