# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import attr

@attr.s
class Sorting(object):
    field = attr.ib(validator=attr.validators.instance_of((str)))
    desc = attr.ib(validator=attr.validators.instance_of(bool))
