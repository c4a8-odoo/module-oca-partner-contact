# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerPurchaseManager(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        # Use system users that are always present (not demo data)
        cls.user = cls.env.ref("base.user_admin")
        cls.user2 = cls.env.ref("base.user_root")

    def test_assign_purchase_manager(self):
        """A purchase manager (res.users) can be assigned to a partner."""
        partner = self.partner_model.create(
            {"name": "Supplier", "purchase_manager_id": self.user.id}
        )
        self.assertEqual(partner.purchase_manager_id, self.user)

    def test_partner_without_purchase_manager(self):
        """A partner can be created without a purchase manager."""
        partner = self.partner_model.create({"name": "No Manager Supplier"})
        self.assertFalse(partner.purchase_manager_id)

    def test_update_purchase_manager(self):
        """A partner's purchase manager can be changed."""
        partner = self.partner_model.create(
            {"name": "Managed Supplier", "purchase_manager_id": self.user.id}
        )
        self.assertEqual(partner.purchase_manager_id, self.user)
        partner.write({"purchase_manager_id": self.user2.id})
        self.assertEqual(partner.purchase_manager_id, self.user2)

    def test_clear_purchase_manager(self):
        """A partner's purchase manager can be cleared."""
        partner = self.partner_model.create(
            {"name": "Clear Manager Partner", "purchase_manager_id": self.user.id}
        )
        partner.write({"purchase_manager_id": False})
        self.assertFalse(partner.purchase_manager_id)
