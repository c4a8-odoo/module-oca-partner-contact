# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerPriority(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.priority_model = cls.env["partner.priority"]
        cls.partner_model = cls.env["res.partner"]

    def test_create_priority(self):
        """A priority record can be created with name, description and sequence."""
        priority = self.priority_model.create(
            {"name": "High", "description": "High priority partner", "sequence": 10}
        )
        self.assertEqual(priority.name, "High")
        self.assertEqual(priority.description, "High priority partner")
        self.assertEqual(priority.sequence, 10)

    def test_default_sequence(self):
        """Sequence defaults to 0 when not specified."""
        priority = self.priority_model.create(
            {"name": "Normal", "description": "Normal priority"}
        )
        self.assertEqual(priority.sequence, 0)

    def test_assign_priority_to_partner(self):
        """A priority can be assigned to a partner via priority_id."""
        priority = self.priority_model.create(
            {"name": "VIP", "description": "VIP partner", "sequence": 1}
        )
        partner = self.partner_model.create(
            {"name": "VIP Partner", "priority_id": priority.id}
        )
        self.assertEqual(partner.priority_id, priority)

    def test_partner_without_priority(self):
        """A partner can be created without a priority."""
        partner = self.partner_model.create({"name": "No Priority Partner"})
        self.assertFalse(partner.priority_id)

    def test_priority_ordering_by_sequence(self):
        """Priorities are ordered by sequence."""
        low = self.priority_model.create(
            {"name": "Low", "description": "Low priority", "sequence": 30}
        )
        high = self.priority_model.create(
            {"name": "High2", "description": "High priority", "sequence": 5}
        )
        priorities = self.priority_model.search(
            [("id", "in", [low.id, high.id])], order="sequence"
        )
        self.assertEqual(priorities[0], high)
        self.assertEqual(priorities[1], low)

    def test_update_priority_on_partner(self):
        """A partner's priority can be updated."""
        priority1 = self.priority_model.create(
            {"name": "P1", "description": "P1 desc", "sequence": 1}
        )
        priority2 = self.priority_model.create(
            {"name": "P2", "description": "P2 desc", "sequence": 2}
        )
        partner = self.partner_model.create(
            {"name": "Partner", "priority_id": priority1.id}
        )
        self.assertEqual(partner.priority_id, priority1)
        partner.write({"priority_id": priority2.id})
        self.assertEqual(partner.priority_id, priority2)
