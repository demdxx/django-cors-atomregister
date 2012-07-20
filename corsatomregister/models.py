# -*- coding: utf-8 -*-

__author__ = "Ponomarev Dmitriy <demdxx@gmail.com>"

import os, logging
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

from django.db import models, transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

__all__ = ['Item']

class Item(models.Model):
    user_from           = models.ForeignKey(User, verbose_name=_('User'), related_name='atomregister_items', db_index=True)
    user_target         = models.ForeignKey(User, verbose_name=_('User'), related_name='atomregister_target_items', db_index=True)

    code                = models.PositiveIntegerField(_('Operation code'),default=0)

    content_type        = models.ForeignKey(ContentType, db_index=True)
    object_id           = models.PositiveIntegerField(_('object ID'), db_index=True)
    content_object      = generic.GenericForeignKey('content_type','object_id')

    unique_mark         = models.IntegerField(default=None, blank=True, null=True, editable=False)

    date_create         = models.DateTimeField(_('Creation date'), auto_now_add=True, editable=False)
    date_modify         = models.DateTimeField(_('Modify date'), auto_now=True, editable=False)
    
    is_positive         = models.BooleanField(_('Is positive'), default=True)

    class Meta:
        unique_together = (('user_from', 'code', 'content_type', 'object_id', 'unique_mark'),)

