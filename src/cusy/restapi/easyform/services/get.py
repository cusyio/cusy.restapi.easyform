# -*- coding: utf-8 -*-

from cusy.restapi.easyform.serializer.utils import get_json_schema_for_form_contents
from plone.restapi.services import Service

import json


_no_content_marker = object()


class EasyFormSchemaGet(Service):

    def render(self):
        """Customized render method which does not sort keys.

        The order of the keys is important here.
        """
        self.check_permission()
        content = self.reply()
        if content is not _no_content_marker:
            self.request.response.setHeader("Content-Type", self.content_type)
            return json.dumps(
                content, indent=2, sort_keys=False, separators=(", ", ": ")
            )

    def reply(self):
        """Get the json schema representation of the form."""
        result = get_json_schema_for_form_contents(self.context, self.request)
        self.content_type = "application/json+schema"
        return result
