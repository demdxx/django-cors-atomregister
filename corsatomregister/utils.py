# Utils ...
import logging

from django.db import models
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from .models import Item

__all__ = ['register','unregister','isregister','countregister']

logger = logging.getLogger(__name__)


def get_content_type(obj):
    return ContentType.objects.get_for_model(obj)


@transaction.commit_manually
def register(code,user,obj,unique=True,positive=True,counter_field=None):
    if not isinstance(obj,models.Model):
        transaction.rollback()
        raise Exception('Object must be instanced by Model')

    print 'register',code,user,obj,unique,positive,counter_field
    res = None
    try:
        res = Item(
            user_from       = user,
            user_target     = getattr(obj,'user',None),
            content_type    = get_content_type(obj),
            object_id       = obj.id,
            code            = code,
            unique_mark     = 1 if unique else 0,
            is_positive     = positive
        )
        res.save()
        
        # Set counts
        if counter_field:
            if not isinstance(counter_field,(list,tuple)):
                counter_field = [counter_field]

            setattr(obj,counter_field[0], getattr(obj,counter_field[0])+1)
            if positive and len(counter_field)>1:
                setattr(obj,counter_field[1], getattr(obj,counter_field[1])+1)
            if not positive and len(counter_field)>2:
                setattr(obj,counter_field[2], getattr(obj,counter_field[2])+1)

            obj.save()

        elif hasattr(obj, 'touch'):
            obj.touch()

        elif hasattr(obj, 'invalidate'):
            obj.invalidate()

        elif hasattr(obj, '_invalidate'):
            obj._invalidate()

    except Exception, e:
        logger.exception(e)
        transaction.rollback()
        return False
    else:
        transaction.commit()

    return True


def unregister(code,user,obj,unique=True,counter_field=None):
    filter = Item.objects.filter(
            user_from       = user,
            content_type    = get_content_type(obj),
            object_id       = obj.id,
            code            = code,
            unique_mark     = 1 if unique else None
        )
        
    # Set counts
    if counter_field:
        if not isinstance(counter_field,(list,tuple)):
            counter_field = [counter_field]

        setattr(obj,counter_field[0], getattr(obj,counter_field[0])-filter.count())
        if len(counter_field)>1:
            setattr(obj,counter_field[1], getattr(obj,counter_field[1])-filter.filter(is_positive=True).count())
        if len(counter_field)>2:
            setattr(obj,counter_field[2], getattr(obj,counter_field[2])-filter.filter(is_positive=False).count())

        obj.save()

    elif hasattr(obj, 'touch'):
        obj.touch()

    elif hasattr(obj, 'invalidate'):
        obj.invalidate()

    elif hasattr(obj, '_invalidate'):
        obj._invalidate()

    return filter.delete()


def isregister(code,user,obj,unique=True):
    try:
        item = Item.objects.get(
            user_from       = user,
            content_type    = get_content_type(obj),
            object_id       = obj.id,
            code            = code,
            unique_mark     = 1 if unique else None
        )
        return item.is_positive
    except Item.DoesNotExist:
        return None


def countregister(code,obj,positive=True,counter_field=None):
    if counter_field:
        if not isinstance(counter_field,(list,tuple)):
            counter_field = [counter_field]

        if positive is None:
            return getattr(obj, counter_field[0])
        elif positive and len(counter_field)>1:
            return getattr(obj, counter_field[1])
        elif not positive and len(counter_field)>2:
            return getattr(obj, counter_field[2])
    
    # Get count by selector
    filter = Item.objects.filter(
            content_type    = get_content_type(obj),
            object_id       = obj.id,
            code            = code
        )
    return filter.count() if positive is None else filter.filter(is_positive=positive).count()


def get_users(code, obj, positive=None):
    items = Item.objects.filter(code=code, content_type=get_content_type(obj), object_id=obj.id)
    users = [ item.user_from for item in items ]
    return users

