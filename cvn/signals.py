# -*- encoding: UTF-8 -*-

from django.dispatch import Signal

pre_cvn_status_changed = Signal(providing_args=["cvn"])