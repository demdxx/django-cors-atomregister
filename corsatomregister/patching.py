import sys

from django.db import models
from django.core.signals import request_started
from django.db.models import signals
from django.utils.importlib import import_module

from .utils import register, unregister, isregister, countregister, get_users


def import_class(module, class_name):
    return getattr(import_module(module),class_name)


def monkey(model, info):
    # Init base params
    code = info.get('code', 1)
    unique = info.get('unique', True)
    methods = info.get('names')
    positive_only = info.get('positive_only', False)
    counter_field = info.get('counter_field', None)

    if isinstance(methods,basestring):
        methods = dict((k, '%s_%s' % (k, methods)) for k in ['set', 'uset', 'is', 'count', 'users'])

    # Patch methods
    for k in methods:
        if k == 'set':
            if positive_only:
                setattr(model,methods[k],lambda self, user, **kwargs: register(code,user,self,unique,positive=True,counter_field=counter_field))
            else:
                setattr(model,methods[k],lambda self, user, positive=True: register(code,user,self,unique,positive=positive,counter_field=counter_field))
        elif k == 'uset':
            setattr(model,methods[k],lambda self, user: unregister(code,user,self,unique,counter_field=counter_field))
        elif k == 'is':
            setattr(model,methods[k],lambda self, user: isregister(code,user,self,unique))
        elif k == 'count':
            if positive_only:
                setattr(model,methods[k],lambda self, **kwargs: countregister(code,self,positive=True))
            else:
                setattr(model,methods[k],lambda self, positive=True: countregister(code,self,positive=positive))
        elif k == 'users':
            setattr(model, methods[k], lambda self, positive=True: get_users(code, self, positive=positive))
        else:
            raise Exception, 'Undefined method: %s' % methods[k]
    
    if counter_field:
        fields = model._meta.get_all_field_names()
        if not isinstance(counter_field,(list,tuple)):
            counter_field = [counter_field]
        
        # Patch model fields
        for f in counter_field:
            if f not in fields:
                # Add counter field as usigned int
                model.add_to_class(f, models.PositiveIntegerField(default=0,editable=True,blank=True))


def __init_patch__(**kwargs):
    if not getattr(__init_patch__,'inited',False):
        from .settings import ATOMREGISTER
        for k in ATOMREGISTER:
            app, mod = k.split('.')
            model = import_class('%s.models' % app, mod)
            monkey(model,ATOMREGISTER[k])
        
        setattr(__init_patch__,'inited',True)


if len(sys.argv)>1 and ('run' in sys.argv[1] or 'server' in sys.argv[1] or sys.argv[1] in ['supervisor']):
    request_started.connect(__init_patch__)
else:
    __init_patch__()


