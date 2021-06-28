# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from collective.easyform.interfaces import ILabel
from collective.easyform.interfaces import IRichLabel
from cusy.restapi.easyform.interfaces import ICusyRestapiEasyformLayer
from plone.app.content.browser.vocabulary import DEFAULT_PERMISSION
from plone.app.content.browser.vocabulary import PERMISSIONS
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.z3cform.interfaces import IFieldPermissionChecker
from plone.restapi.types.adapters import ChoiceJsonSchemaProvider
from plone.restapi.types.adapters import DateJsonSchemaProvider
from plone.restapi.types.adapters import DatetimeJsonSchemaProvider
from plone.restapi.types.adapters import DefaultJsonSchemaProvider
from plone.restapi.types.adapters import EmailJsonSchemaProvider
from plone.restapi.types.adapters import URIJsonSchemaProvider
from plone.restapi.types.interfaces import IJsonSchemaProvider
from plone.restapi.types.utils import get_querysource_url
from plone.restapi.types.utils import get_source_url
from plone.restapi.types.utils import get_vocabulary_url
from plone.schema import IEmail
from z3c.formwidget.query.interfaces import IQuerySource
from zope.component import adapter
from zope.component import queryAdapter
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IDate
from zope.schema.interfaces import IDatetime
from zope.schema.interfaces import IURI


@adapter(IEmail, Interface, ICusyRestapiEasyformLayer)
@implementer(IJsonSchemaProvider)
class CusyEmailJsonSchemaProvider(EmailJsonSchemaProvider):
    def additional(self):
        info = super(CusyEmailJsonSchemaProvider, self).additional()
        info["format"] = "email"
        return info


@adapter(IURI, Interface, ICusyRestapiEasyformLayer)
@implementer(IJsonSchemaProvider)
class CusyURIJsonSchemaProvider(URIJsonSchemaProvider):
    def additional(self):
        info = super(CusyURIJsonSchemaProvider, self).additional()
        info["format"] = "uri"
        return info


@adapter(IDate, Interface, ICusyRestapiEasyformLayer)
@implementer(IJsonSchemaProvider)
class CusyDateJsonSchemaProvider(DateJsonSchemaProvider):
    def additional(self):
        info = super(CusyDateJsonSchemaProvider, self).additional()
        info["format"] = "date"
        return info


@adapter(IDatetime, Interface, ICusyRestapiEasyformLayer)
@implementer(IJsonSchemaProvider)
class CusyDatetimeJsonSchemaProvider(DatetimeJsonSchemaProvider):
    def additional(self):
        info = super(CusyDatetimeJsonSchemaProvider, self).additional()
        info["format"] = "date-time"
        return info


@adapter(IChoice, Interface, ICusyRestapiEasyformLayer)
@implementer(IJsonSchemaProvider)
class CusyChoiceJsonSchemaProvider(ChoiceJsonSchemaProvider):
    def additional(self):
        result = {}
        # Named global vocabulary
        vocab_name = getattr(self.field, "vocabularyName", None)
        if vocab_name:
            if not self.checkPermission(vocab_name):
                return {"enum": []}
            result.update(
                {
                    "vocabulary": {
                        "@id": get_vocabulary_url(
                            vocab_name, self.context, self.request
                        )
                    }
                }
            )

        # Maybe an unnamed vocabulary or source.
        vocabulary = getattr(self.field, "vocabulary", None)
        if IContextSourceBinder.providedBy(vocabulary):
            vocabulary = vocabulary(self.context)

        # Query source
        if IQuerySource.providedBy(vocabulary):
            result.update(
                {
                    "querysource": {
                        "@id": get_querysource_url(
                            self.field, self.context, self.request
                        )
                    }
                }
            )

        # Unamed ISource or vocabulary - render link addressing it via field
        #
        # Even though the URL will point to the @sources endpoint, we also
        # list it under the 'vocabulary' key, because the semantics for an
        # API consumer are exactly the same: A GET to that URL will enumerate
        # terms, and will support batching and filtering by title/token.
        if not result.get("vocabulary"):
            result.update(
                {
                    "vocabulary": {
                        "@id": get_source_url(self.field, self.context, self.request)
                    }
                }
            )

        # Optionally inline choices for unnamed sources
        # (this is for BBB, and may eventually be deprecated)
        if hasattr(vocabulary, "__iter__") and self.should_render_choices:
            choices = []

            for term in vocabulary:
                if term.title:
                    title = translate(term.title, context=self.request)
                else:
                    title = None
                if vocab_name:
                    token = term.token
                else:
                    token = title
                if token is None:
                    continue
                choices.append({"const": token, "title": title})

            result.update({"oneOf": choices})

        return result

    def checkPermission(self, vocabulary_name):
        authorized = None
        sm = getSecurityManager()
        if vocabulary_name not in PERMISSIONS or not INavigationRoot.providedBy(
            self.context
        ):
            field_name = self.field.getName()
            # Check field specific permission
            if field_name:
                permission_checker = queryAdapter(self.context, IFieldPermissionChecker)
                if permission_checker is not None:
                    authorized = permission_checker.validate(
                        field_name, vocabulary_name
                    )
                elif sm.checkPermission(
                    PERMISSIONS.get(vocabulary_name, DEFAULT_PERMISSION), self.context
                ):
                    # If no checker, fall back to checking the global registry
                    authorized = True
            else:
                authorized = sm.checkPermission(
                    PERMISSIONS.get(vocabulary_name, DEFAULT_PERMISSION), self.context
                )
        # Short circuit if we are on the site root and permission is
        # in global registry
        elif not sm.checkPermission(
            PERMISSIONS.get(vocabulary_name, DEFAULT_PERMISSION), self.context
        ):
            authorized = False

        return authorized


@adapter(ILabel, Interface, Interface)
@implementer(IJsonSchemaProvider)
class LabelJsonSchemaProvider(DefaultJsonSchemaProvider):
    prefix = ""

    def get_type(self):
        return "string"

    def get_widget(self):
        return "label"

    def get_factory(self):
        return "Label"


@adapter(IRichLabel, Interface, Interface)
@implementer(IJsonSchemaProvider)
class RichLabelJsonSchemaProvider(LabelJsonSchemaProvider):
    prefix = ""

    def get_type(self):
        return "string"

    def get_widget(self):
        return "richlabel"

    def get_factory(self):
        return "Rich Label"

    def additional(self):
        return {
            "content": self.field.rich_label and self.field.rich_label.output or "",
        }
