# -*- coding: utf-8 -*-
# from odoo import http


# class AfricabCore(http.Controller):
#     @http.route('/africab_core/africab_core', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/africab_core/africab_core/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('africab_core.listing', {
#             'root': '/africab_core/africab_core',
#             'objects': http.request.env['africab_core.africab_core'].search([]),
#         })

#     @http.route('/africab_core/africab_core/objects/<model("africab_core.africab_core"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('africab_core.object', {
#             'object': obj
#         })

