# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from deform.widget import Select2Widget


class TrelloBoardSelectWidget(Select2Widget):
    multiple = True
    values = (('abc', 'Test 1'), ('abd', 'Test 2'))
