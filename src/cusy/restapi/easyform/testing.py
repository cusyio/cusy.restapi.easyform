# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import cusy.restapi.easyform


class CusyRestapiEasyformLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=cusy.restapi.easyform)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cusy.restapi.easyform:default')


CUSY_RESTAPI_EASYFORM_FIXTURE = CusyRestapiEasyformLayer()


CUSY_RESTAPI_EASYFORM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CUSY_RESTAPI_EASYFORM_FIXTURE,),
    name='CusyRestapiEasyformLayer:IntegrationTesting',
)


CUSY_RESTAPI_EASYFORM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CUSY_RESTAPI_EASYFORM_FIXTURE,),
    name='CusyRestapiEasyformLayer:FunctionalTesting',
)


CUSY_RESTAPI_EASYFORM_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CUSY_RESTAPI_EASYFORM_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CusyRestapiEasyformLayer:AcceptanceTesting',
)
