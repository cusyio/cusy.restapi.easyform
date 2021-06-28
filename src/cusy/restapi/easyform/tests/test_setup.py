# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from cusy.restapi.easyform.testing import CUSY_RESTAPI_EASYFORM_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that cusy.restapi.easyform is properly installed."""

    layer = CUSY_RESTAPI_EASYFORM_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cusy.restapi.easyform is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'cusy.restapi.easyform'))

    def test_browserlayer(self):
        """Test that ICusyRestapiEasyformLayer is registered."""
        from cusy.restapi.easyform.interfaces import (
            ICusyRestapiEasyformLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICusyRestapiEasyformLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CUSY_RESTAPI_EASYFORM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['cusy.restapi.easyform'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if cusy.restapi.easyform is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'cusy.restapi.easyform'))

    def test_browserlayer_removed(self):
        """Test that ICusyRestapiEasyformLayer is removed."""
        from cusy.restapi.easyform.interfaces import \
            ICusyRestapiEasyformLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICusyRestapiEasyformLayer,
            utils.registered_layers())
