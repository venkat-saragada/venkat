# -*- coding: utf-8 -*-
from odoo import http

# class EmpBackgroundVerification(http.Controller):
#     @http.route('/emp_background_verification/emp_background_verification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emp_background_verification/emp_background_verification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('emp_background_verification.listing', {
#             'root': '/emp_background_verification/emp_background_verification',
#             'objects': http.request.env['emp_background_verification.emp_background_verification'].search([]),
#         })

#     @http.route('/emp_background_verification/emp_background_verification/objects/<model("emp_background_verification.emp_background_verification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emp_background_verification.object', {
#             'object': obj
#         })