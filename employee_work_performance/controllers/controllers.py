# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeWorkPerformance(http.Controller):
#     @http.route('/employee_work_performance/employee_work_performance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_work_performance/employee_work_performance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_work_performance.listing', {
#             'root': '/employee_work_performance/employee_work_performance',
#             'objects': http.request.env['employee_work_performance.employee_work_performance'].search([]),
#         })

#     @http.route('/employee_work_performance/employee_work_performance/objects/<model("employee_work_performance.employee_work_performance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_work_performance.object', {
#             'object': obj
#         })

