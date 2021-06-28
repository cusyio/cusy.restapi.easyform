# -*- coding: utf-8 -*-

from collections import OrderedDict
from cusy.restapi.easyform.interfaces import ICusyRestapiEasyformLayer
from plone.restapi.serializer.converters import IJsonCompatible
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.types.interfaces import IJsonSchemaProvider
from plone.restapi.types.utils import get_form_fieldsets
from plone.restapi.types.utils import get_info_for_fieldset
from plone.restapi.types.utils import get_jsonschema_properties
from plone.restapi.types.utils import iter_fields
from six.moves import map
from six.moves import zip
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import implementer


def get_field_value(field, excluded_fields, form, request, prefix):
    fieldname = field.__name__
    if fieldname not in excluded_fields:

        adapter = queryMultiAdapter(
            (field, form, request),
            interface=IJsonSchemaProvider,
            name=field.__name__,
        )

        if adapter is None:
            adapter = queryMultiAdapter(
                (field, form, request), interface=IJsonSchemaProvider
            )

        adapter.prefix = prefix
        if prefix:
            fieldname = ".".join([prefix, fieldname])

        return adapter.get_schema()


def get_json_schema_for_form_contents(
    context, request, prefix="", excluded_fields=None
):
    view = getMultiAdapter((context, request), name="view")
    formview = view.form(context, request)
    formview.update()
    fieldsets = get_form_fieldsets(formview)
    # Build JSON schema properties

    properties = OrderedDict()
    base_required = []

    for fieldset in fieldsets:
        id_ = fieldset["id"]
        info = get_info_for_fieldset(formview, request, id_)
        fieldset_properties = get_jsonschema_properties(
            formview, request, [fieldset], excluded_fields=excluded_fields
        )

        if len(fieldsets) > 1 and id_ == "default" and not info:
            info = {
                "title": "Standard",
                "description": "",
            }

        # Determine required fields
        required = []
        for field in iter_fields([fieldset]):
            if field.field.required:
                required.append(field.field.getName())

        if info:
            properties[id_] = {
                "title": info["title"],
                "description": info["description"],
                "type": "object",
                "properties": fieldset_properties,
                "required": required,
            }
        else:
            # Default fieldset
            properties.update(fieldset_properties)
            base_required.extend(required)

    return {
        "type": "object",
        "title": context.Title(),
        "properties": IJsonCompatible(properties),
        "required": base_required,
    }


@implementer(IJsonCompatible)
@adapter(OrderedDict, ICusyRestapiEasyformLayer)
def ordereddict_converter(value):
    if value == {}:
        return {}

    keys, values = list(zip(*list(value.items())))
    keys = list(map(json_compatible, keys))
    values = list(map(json_compatible, values))
    return OrderedDict(list(zip(keys, values)))
