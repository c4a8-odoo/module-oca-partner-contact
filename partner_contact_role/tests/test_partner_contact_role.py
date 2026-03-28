# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerContactRole(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.role_model = cls.env["res.partner.role"]
        cls.partner_model = cls.env["res.partner"]
        cls.partner = cls.partner_model.create({"name": "Role Partner"})

    def test_create_role(self):
        """A partner role can be created with name and active fields."""
        role = self.role_model.create({"name": "Supplier"})
        self.assertEqual(role.name, "Supplier")
        self.assertTrue(role.active)

    def test_role_default_active(self):
        """Roles are active by default."""
        role = self.role_model.create({"name": "Customer"})
        self.assertTrue(role.active)

    def test_archive_role(self):
        """A role can be archived by setting active to False."""
        role = self.role_model.create({"name": "Archived Role"})
        role.write({"active": False})
        self.assertFalse(role.active)
        result = self.role_model.search([("name", "=", "Archived Role")])
        self.assertNotIn(role, result)

    def test_assign_role_to_partner(self):
        """A role can be assigned to a partner via the M2M field."""
        role = self.role_model.create({"name": "Distributor"})
        self.partner.write({"role_ids": [(4, role.id)]})
        self.assertIn(role, self.partner.role_ids)

    def test_assign_multiple_roles(self):
        """A partner can have multiple roles."""
        role1 = self.role_model.create({"name": "Buyer"})
        role2 = self.role_model.create({"name": "Seller"})
        self.partner.write({"role_ids": [(6, 0, [role1.id, role2.id])]})
        self.assertIn(role1, self.partner.role_ids)
        self.assertIn(role2, self.partner.role_ids)

    def test_remove_role_from_partner(self):
        """A role can be removed from a partner."""
        role = self.role_model.create({"name": "Removable Role"})
        self.partner.write({"role_ids": [(4, role.id)]})
        self.assertIn(role, self.partner.role_ids)
        self.partner.write({"role_ids": [(3, role.id)]})
        self.assertNotIn(role, self.partner.role_ids)

    def test_partner_without_roles(self):
        """A partner can be created without any roles."""
        partner = self.partner_model.create({"name": "No Role Partner"})
        self.assertFalse(partner.role_ids)
