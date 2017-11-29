# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime

from django.http import JsonResponse, FileResponse
from django.template.loader import render_to_string

from utils.django_base import BaseView
from utils import common


# Create your views here.
class GenerateContract(BaseView):

    def post(self, request, *args, **kwargs):
        signature = request.POST.get('signature', None)
        d = {'error': 1}
        if signature:
            html = render_to_string('turnover/signature-test.html', {'signature': signature})
            filename = "Signature_%s.pdf" % datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            out_file = os.path.join(r"D:\FTP", filename)
            common.generate_pdf_from_string(html, out_file)
            d.update({'error': 0, 'path': out_file})
        return JsonResponse(d)


class ViewContract(BaseView):

    def get(self, request, *args, **kwargs):
        path = kwargs.get('path')
        return FileResponse(open(path, 'rb'), content_type='application/pdf')
