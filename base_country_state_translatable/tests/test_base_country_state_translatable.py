# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestBaseCountryStateTranslatable(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.state_model = cls.env["res.country.state"]
        cls.country_us = cls.env.ref("base.us")

    def test_state_name_field_is_translatable(self):
        """The name field on res.country.state has translate=True."""
        name_field = self.state_model._fields.get("name")
        self.assertIsNotNone(name_field)
        self.assertTrue(
            name_field.translate,
            "The 'name' field on res.country.state should be translatable.",
        )

    def test_create_state_with_name(self):
        """A country state can be created and its name can be read back."""
        state = self.state_model.create(
            {"name": "Test State", "code": "TS", "country_id": self.country_us.id}
        )
        self.assertEqual(state.name, "Test State")

    def test_update_state_name(self):
        """A country state name can be updated."""
        state = self.state_model.create(
            {
                "name": "Original Name",
                "code": "ON",
                "country_id": self.country_us.id,
            }
        )
        state.write({"name": "Updated Name"})
        self.assertEqual(state.name, "Updated Name")
