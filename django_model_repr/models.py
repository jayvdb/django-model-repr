# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class Model(models.Model):
    class Meta:
        abstract = True

    def _repr_format_field(self, field):
        """Get a "bar='bar_value'" str.

        field is a Django Field object.
        """

        if isinstance(field, models.ForeignKey):
            field_name = field.name + '_id'
        else:
            field_name = field.name
        return self._repr_format_field_raw(field, field_name)

    def _repr_format_field_raw(self, field, field_name=None):
        """Get a "bar='bar_value'" str.

        field is a Django Field object.
        """
        if not isinstance(field_name, str):
            field_name = field.name

        field_value = getattr(self, field_name)

        default = field.default
        if field_value == default:
            return ''
        elif default is models.NOT_PROVIDED:
            if isinstance(field, models.CharField) and field_value == '':
                return ''
            if field_value is None:
                return ''
        return "{}={!r}".format(field_name, field_value)

    def __repr__(self):
        cls = type(self)
        fields = cls._meta.fields
        if hasattr(cls._meta, 'repr_fields'):
            fields = [f for f in fields if f.name in cls._meta.repr_fields]
            parts = filter(None, map(self._repr_format_field_raw, fields))
        else:
            parts = filter(None, map(self._repr_format_field, fields))
        attrs = ', '.join(parts)
        return '{}({})'.format(cls.__name__, attrs)

    __str__ = __repr__


import django.db.models.options as options
if 'repr_fields' not in options.DEFAULT_NAMES:
    options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('repr_fields',)

import django.contrib.auth.base_user


class AbstractBaseUser(Model, django.contrib.auth.base_user.AbstractBaseUser):
    pass
    class Meta:
        abstract = True


if getattr(settings, "MODEL_REPR_MONKEY_PATCHING", True):
    print('brutallling')
    setattr(models, "Model", Model)
    import django.db.models.base
    setattr(django.db.models.base, "Model", Model)
    setattr(django.contrib.auth.base_user, "AbstractBaseUser", AbstractBaseUser)
