import base64
import datetime
import json
import os
import logging
import re
import requests
import werkzeug.urls
import werkzeug.utils
import werkzeug.wrappers

from itertools import islice
from lxml import etree
from textwrap import shorten
from werkzeug.exceptions import NotFound
from xml.etree import ElementTree as ET
import odoo

from odoo import http, models, fields, _
from odoo.exceptions import AccessError
from odoo.http import request, SessionExpiredException
from odoo.osv import expression
from odoo.tools import OrderedSet, escape_psql, html_escape as escape
from odoo.addons.http_routing.models.ir_http import slug, slugify, _guess_mimetype
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.web import Home
from odoo.addons.web.controllers.binary import Binary
from odoo.addons.website.tools import get_base_domain

logger = logging.getLogger(__name__)


class Website(Home):

    @http.route('/akghardware/<int:website_id>', type='http', auth="none", sitemap=False)
    def website_force_akghardware(self, website_id, path='/', isredir=False, **kw):
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        website = request.env['website'].browse(website_id)

        if not isredir and website.domain:
            domain_from = request.httprequest.environ.get('HTTP_HOST', '')
            domain_to = get_base_domain(website.domain)
            if domain_from != domain_to:
                url_to = werkzeug.urls.url_join(website.domain, '/%s?isredir=1&path=%s' % (website.id, path))
                return request.redirect(url_to)
        website._force()
        return request.redirect(path)