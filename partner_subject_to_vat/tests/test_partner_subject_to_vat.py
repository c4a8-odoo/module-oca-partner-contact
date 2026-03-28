# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerSubjectToVat(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]

    def test_partner_subject_to_vat_true(self):
        """A partner can be marked as subject to VAT."""
        partner = self.partner_model.create(
            {"name": "VAT Company", "is_subject_to_vat": True}
        )
        self.assertTrue(partner.is_subject_to_vat)

    def test_partner_subject_to_vat_false(self):
        """A partner can be marked as not subject to VAT."""
        partner = self.partner_model.create(
            {"name": "No VAT Company", "is_subject_to_vat": False}
        )
        self.assertFalse(partner.is_subject_to_vat)

    def test_partner_subject_to_vat_default(self):
        """The is_subject_to_vat field defaults to False when not provided."""
        partner = self.partner_model.create({"name": "Default VAT Partner"})
        self.assertFalse(partner.is_subject_to_vat)

    def test_update_subject_to_vat(self):
        """The is_subject_to_vat field can be toggled on an existing partner."""
        partner = self.partner_model.create(
            {"name": "Toggle VAT", "is_subject_to_vat": False}
        )
        self.assertFalse(partner.is_subject_to_vat)
        partner.write({"is_subject_to_vat": True})
        self.assertTrue(partner.is_subject_to_vat)
        partner.write({"is_subject_to_vat": False})
        self.assertFalse(partner.is_subject_to_vat)

    def test_search_subject_to_vat(self):
        """Partners can be filtered by is_subject_to_vat."""
        vat_partner = self.partner_model.create(
            {"name": "VAT Search Partner", "is_subject_to_vat": True}
        )
        no_vat_partner = self.partner_model.create(
            {"name": "No VAT Search Partner", "is_subject_to_vat": False}
        )
        vat_results = self.partner_model.search([("is_subject_to_vat", "=", True)])
        self.assertIn(vat_partner, vat_results)
        self.assertNotIn(no_vat_partner, vat_results)
