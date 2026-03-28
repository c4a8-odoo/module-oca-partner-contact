# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerContactJobPosition(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.job_position_model = cls.env["res.partner.job_position"]
        cls.partner_model = cls.env["res.partner"]

    def test_create_job_position(self):
        """A job position can be created with a name."""
        position = self.job_position_model.create({"name": "Developer"})
        self.assertEqual(position.name, "Developer")

    def test_assign_job_position_to_partner(self):
        """A job position can be assigned to a partner."""
        position = self.job_position_model.create({"name": "Manager"})
        partner = self.partner_model.create(
            {"name": "Test Contact", "job_position_id": position.id}
        )
        self.assertEqual(partner.job_position_id, position)

    def test_partner_without_job_position(self):
        """A partner can be created without a job position."""
        partner = self.partner_model.create({"name": "No Position Partner"})
        self.assertFalse(partner.job_position_id)

    def test_update_job_position(self):
        """A partner's job position can be updated."""
        pos1 = self.job_position_model.create({"name": "Junior Developer"})
        pos2 = self.job_position_model.create({"name": "Senior Developer"})
        partner = self.partner_model.create(
            {"name": "Dev Partner", "job_position_id": pos1.id}
        )
        self.assertEqual(partner.job_position_id, pos1)
        partner.write({"job_position_id": pos2.id})
        self.assertEqual(partner.job_position_id, pos2)

    def test_multiple_partners_same_job_position(self):
        """Multiple partners can share the same job position."""
        position = self.job_position_model.create({"name": "Accountant"})
        partner1 = self.partner_model.create(
            {"name": "Accountant 1", "job_position_id": position.id}
        )
        partner2 = self.partner_model.create(
            {"name": "Accountant 2", "job_position_id": position.id}
        )
        self.assertEqual(partner1.job_position_id, position)
        self.assertEqual(partner2.job_position_id, position)
