# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerFax(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]

    def test_create_partner_with_fax(self):
        """A partner can be created with a fax number."""
        partner = self.partner_model.create(
            {"name": "Test Partner", "fax": "+1 555 123 4567"}
        )
        self.assertEqual(partner.fax, "+1 555 123 4567")

    def test_partner_without_fax(self):
        """A partner can be created without a fax number."""
        partner = self.partner_model.create({"name": "No Fax Partner"})
        self.assertFalse(partner.fax)

    def test_update_fax(self):
        """A partner's fax number can be updated."""
        partner = self.partner_model.create({"name": "Fax Partner", "fax": "111"})
        partner.write({"fax": "222"})
        self.assertEqual(partner.fax, "222")

    def test_clear_fax(self):
        """A partner's fax number can be cleared."""
        partner = self.partner_model.create(
            {"name": "Clear Fax Partner", "fax": "333"}
        )
        partner.write({"fax": False})
        self.assertFalse(partner.fax)
