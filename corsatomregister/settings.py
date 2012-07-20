
from django.conf import settings

ATOMREGISTER = getattr(settings,'ATOMREGISTER',{})

# Accept models
#
# ATOMREGISTER = {
#   'news.article': {'names':('set_like','unset_like','is_like'),'code':1}
#
#

