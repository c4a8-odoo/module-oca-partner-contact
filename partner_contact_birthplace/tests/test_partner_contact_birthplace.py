# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerContactBirthplace(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.country_be = cls.env.ref("base.be")
        cls.state_be = cls.env["res.country.state"].search(
            [("country_id", "=", cls.country_be.id)], limit=1
        )

    def test_create_partner_with_birthplace(self):
        """A partner can be created with birth city and zip."""
        partner = self.partner_model.create(
            {
                "name": "Test Person",
                "birth_city": "Brussels",
                "birth_zip": "1000",
            }
        )
        self.assertEqual(partner.birth_city, "Brussels")
        self.assertEqual(partner.birth_zip, "1000")

    def test_create_partner_with_birth_country(self):
        """A partner can have a birth country set."""
        partner = self.partner_model.create(
            {
                "name": "Test Person",
                "birth_country_id": self.country_be.id,
            }
        )
        self.assertEqual(partner.birth_country_id, self.country_be)

    def test_create_partner_with_birth_state(self):
        """A partner can have a birth state set."""
        if not self.state_be:
            self.skipTest("No states available for Belgium in test database")
        partner = self.partner_model.create(
            {
                "name": "Test Person",
                "birth_country_id": self.country_be.id,
                "birth_state_id": self.state_be.id,
            }
        )
        self.assertEqual(partner.birth_state_id, self.state_be)

    def test_partner_without_birthplace(self):
        """A partner can be created without birth fields."""
        partner = self.partner_model.create({"name": "Anonymous"})
        self.assertFalse(partner.birth_city)
        self.assertFalse(partner.birth_zip)
        self.assertFalse(partner.birth_country_id)
        self.assertFalse(partner.birth_state_id)

    def test_update_birth_city(self):
        """The birth city can be updated on a partner."""
        partner = self.partner_model.create(
            {"name": "Update Person", "birth_city": "Liège"}
        )
        partner.write({"birth_city": "Ghent"})
        self.assertEqual(partner.birth_city, "Ghent")
