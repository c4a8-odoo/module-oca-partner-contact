# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerAccreditation(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.accreditation_model = cls.env["res.partner.accreditation"]
        cls.partner_model = cls.env["res.partner"]
        cls.partner = cls.partner_model.create({"name": "Test Partner"})

    def test_create_accreditation(self):
        """An accreditation record can be created with name and active fields."""
        accreditation = self.accreditation_model.create(
            {"name": "ISO 9001", "active": True}
        )
        self.assertEqual(accreditation.name, "ISO 9001")
        self.assertTrue(accreditation.active)

    def test_accreditation_default_active(self):
        """Accreditation is active by default."""
        accreditation = self.accreditation_model.create({"name": "ISO 14001"})
        self.assertTrue(accreditation.active)

    def test_archive_accreditation(self):
        """An accreditation can be archived by setting active to False."""
        accreditation = self.accreditation_model.create(
            {"name": "ISO 27001", "active": True}
        )
        accreditation.write({"active": False})
        self.assertFalse(accreditation.active)
        # Archived records are excluded from default searches
        result = self.accreditation_model.search([("name", "=", "ISO 27001")])
        self.assertNotIn(accreditation, result)

    def test_assign_accreditation_to_partner(self):
        """An accreditation can be assigned to a partner via the M2M field."""
        accreditation = self.accreditation_model.create({"name": "CE Mark"})
        self.partner.write({"accreditation_ids": [(4, accreditation.id)]})
        self.assertIn(accreditation, self.partner.accreditation_ids)

    def test_accreditation_partner_ids_backref(self):
        """The partner_ids back-reference on accreditation reflects assigned partners."""
        accreditation = self.accreditation_model.create({"name": "FDA Approved"})
        self.partner.write({"accreditation_ids": [(4, accreditation.id)]})
        self.assertIn(self.partner, accreditation.partner_ids)

    def test_assign_multiple_accreditations(self):
        """A partner can have multiple accreditations assigned at once."""
        acc1 = self.accreditation_model.create({"name": "Acc A"})
        acc2 = self.accreditation_model.create({"name": "Acc B"})
        self.partner.write(
            {"accreditation_ids": [(6, 0, [acc1.id, acc2.id])]}
        )
        self.assertIn(acc1, self.partner.accreditation_ids)
        self.assertIn(acc2, self.partner.accreditation_ids)

    def test_remove_accreditation_from_partner(self):
        """An accreditation can be removed from a partner."""
        accreditation = self.accreditation_model.create({"name": "Removable Acc"})
        self.partner.write({"accreditation_ids": [(4, accreditation.id)]})
        self.assertIn(accreditation, self.partner.accreditation_ids)
        self.partner.write({"accreditation_ids": [(3, accreditation.id)]})
        self.assertNotIn(accreditation, self.partner.accreditation_ids)
