#!/usr/bin/env python3
import os.path

from django.template.loader import get_template
from weasyprint import HTML

from .models import *


BASE_PATH = os.path.join(os.path.dirname(__file__))
BASE_URL = os.path.join(BASE_PATH, 'templates')


def generate_html(currency: str, invoice: Invoice, template):
    if not template:
        template = get_template('pdf_invoice.html')

    ctx = dict(
        invoice=invoice,
        order=invoice.order,
        currency=currency,
        executive=invoice.vendor.executive,
        vendor=invoice.vendor,
        billing_address=invoice.billing_address,
    )

    html_text = template.render(ctx)
    return html_text


def generate_pdf_from(html, static_path):
    pdf = HTML(string=html, base_url=static_path)
    return pdf


def generate_pdf(currency: str, invoice: Invoice, template=None, static_path=BASE_URL):
    html = generate_html(currency, invoice, template)
    return generate_pdf_from(html, static_path)
