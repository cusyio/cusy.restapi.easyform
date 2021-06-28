# -*- coding: utf-8 -*-

from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from plone.restapi.types.utils import get_form_fieldsets
from zExceptions import BadRequest
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

import datetime
import plone.api
import plone.protect


class EasyFormPost(Service):
    def reply(self):  # noqa: C901
        data = json_body(self.request)

        # Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)

        easyform_view = getMultiAdapter((self.context, self.request), name="view")
        formview = easyform_view.form(self.context, self.request)
        formview.update()
        fieldsets = get_form_fieldsets(formview)

        # normalize data
        # get grouped (fieldset) data and add to plain dict
        form_data = {}
        if len(fieldsets) > 1:
            for fieldset in fieldsets:
                id_ = fieldset["id"]
                if id_ in data:
                    form_data.update(data[id_])
        else:
            form_data.update(data)

        form = easyform_view.form_instance
        errors = []
        for fname in form.schema:
            field = form.schema[fname]
            field_data = form_data.get(fname, None)

            if field_data and field._type == set:
                try:
                    field_data = form_data[fname] = set(field_data)
                except AttributeError:
                    field_data = form_data[fname] = None
            elif field_data and field._type == datetime.date:
                try:
                    field_data = form_data[fname] = datetime.date.fromisoformat(
                        field_data
                    )
                except AttributeError:
                    field_data = form_data[fname] = None
            elif field_data and field._type == datetime.datetime:
                try:
                    field_data = form_data[fname] = datetime.datetime.fromisoformat(
                        field_data
                    )
                except AttributeError:
                    field_data = form_data[fname] = None

            try:
                field.validate(field_data)
            except Exception as error:  # noqa: B902
                errors.append({"error": error, "message": str(error)})

        if errors:
            # Drop Python specific error classes in order to be able to better handle
            # errors on front-end
            for error in errors:
                error["error"] = "ValidationError"
            raise BadRequest(errors)

        data = form.updateServerSideData(form_data)
        errors = form.processActions(form_data)
        if errors:
            return BadRequest("Wrong form data.")

        return self.reply_no_content()
