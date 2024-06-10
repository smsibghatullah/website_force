# controllers/main.py
from odoo import http
from odoo.http import request

class WebsiteForce(http.Controller):
    @http.route('/website/force/akghardware/<int:website_id>', type='http', auth="public", website=True, sitemap=False, multilang=False)
    def website_force(self, website_id, path='/', isredir=False, **kw):
        if not request.env.user.has_group('website.group_multi_website'):
            return request.redirect(path)

        website = request.env['website'].browse(website_id)

        if not isredir and website.domain:
            domain_from = request.httprequest.environ.get('HTTP_HOST', '')
            domain_to = website.domain
            if domain_from != domain_to:
                url_to = website.domain + '/website/force/%d?isredir=1&path=%s' % (website.id, path)
                return request.redirect(url_to)

        website._force()
        return request.redirect(path)
