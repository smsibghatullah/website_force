import logging
from odoo import http
from odoo.http import request
from odoo.addons.website.tools import get_base_domain
import werkzeug.urls

_logger = logging.getLogger(__name__)

class Website(http.Controller):
    @http.route('/akghardware/<int:website_id>', type='http', auth="none", sitemap=False , website=True)
    def website_force_akghardware(self, website_id, path='/', isredir=False, **kw):
        _logger.info("Route accessed with website_id: %s", website_id)
        website = request.env['website'].sudo().browse(website_id)

        if not website.exists():
            _logger.error("Website with ID %s not found", website_id)
            return request.not_found()

        if not isredir and website.domain:
            domain_from = request.httprequest.environ.get('HTTP_HOST', '')
            domain_to = get_base_domain(website.domain)
            _logger.info("Domain from request: %s, Domain to redirect: %s", domain_from, domain_to)
            
            if domain_from != domain_to:
                url_to = werkzeug.urls.url_join(website.domain, '/akghardware/%d?isredir=1&path=%s' % (website.id, path))
                _logger.info("Redirecting to: %s", url_to)
                return request.redirect(url_to)

        _logger.info("Forcing the website and redirecting to path: %s", path)
        website.sudo()._force()
        return request.redirect(path)
