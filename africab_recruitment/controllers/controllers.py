# -*- coding: utf-8 -*-
# from odoo import http


# class AfricabRecruitment(http.Controller):
#     @http.route('/africab_recruitment/africab_recruitment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/africab_recruitment/africab_recruitment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('africab_recruitment.listing', {
#             'root': '/africab_recruitment/africab_recruitment',
#             'objects': http.request.env['africab_recruitment.africab_recruitment'].search([]),
#         })

#     @http.route('/africab_recruitment/africab_recruitment/objects/<model("africab_recruitment.africab_recruitment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('africab_recruitment.object', {
#             'object': obj
#         })

