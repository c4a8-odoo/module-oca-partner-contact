# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerContactNationality(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.country_de = cls.env.ref("base.de")
        cls.country_fr = cls.env.ref("base.fr")

    def test_assign_nationality(self):
        """A nationality (country) can be assigned to a partner."""
        partner = self.partner_model.create(
            {"name": "German Contact", "nationality_id": self.country_de.id}
        )
        self.assertEqual(partner.nationality_id, self.country_de)

    def test_partner_without_nationality(self):
        """A partner can be created without a nationality."""
        partner = self.partner_model.create({"name": "Unknown Nationality"})
        self.assertFalse(partner.nationality_id)

    def test_update_nationality(self):
        """A partner's nationality can be changed."""
        partner = self.partner_model.create(
            {"name": "Changing Nationality", "nationality_id": self.country_de.id}
        )
        self.assertEqual(partner.nationality_id, self.country_de)
        partner.write({"nationality_id": self.country_fr.id})
        self.assertEqual(partner.nationality_id, self.country_fr)

    def test_clear_nationality(self):
        """A partner's nationality can be cleared."""
        partner = self.partner_model.create(
            {"name": "Clear Nationality", "nationality_id": self.country_de.id}
        )
        partner.write({"nationality_id": False})
        self.assertFalse(partner.nationality_id)
