from __future__ import unicode_literals, absolute_import

import django
from django.db import models

from django_hstore.query import HStoreQuerySet
from django_hstore.apps import GEODJANGO_INSTALLED


class HStoreManager(models.Manager):
    """
    Object manager which enables hstore features.
    """
    use_for_related_fields = True

    def get_queryset(self):
        return HStoreQuerySet(self.model, using=self._db)

    get_query_set = get_queryset

    def hkeys(self, attr, **params):
        return self.filter(**params).hkeys(attr)

    def hpeek(self, attr, key, **params):
        return self.filter(**params).hpeek(attr, key)

    def hslice(self, attr, keys, **params):
        return self.filter(**params).hslice(attr, keys)


if GEODJANGO_INSTALLED:
    if django.VERSION[0] == 1:
        from django.contrib.gis.db.models import GeoManager
        class HStoreGeoManagerBase(GeoManager, HStoreManager):
            pass
    else:
        class HStoreGeoManagerBase(HStoreManager):
            pass

    from django_hstore.query import HStoreGeoQuerySet

    class HStoreGeoManager(HStoreGeoManagerBase):
        """
        Object manager combining Geodjango and hstore.
        """
        def get_queryset(self):
            return HStoreGeoQuerySet(self.model, using=self._db)

        get_query_set = get_queryset
