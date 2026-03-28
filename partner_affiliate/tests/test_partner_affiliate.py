# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerAffiliate(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.company = cls.partner_model.create(
            {"name": "Parent Company", "is_company": True}
        )
        cls.contact = cls.partner_model.create(
            {
                "name": "Contact Person",
                "is_company": False,
                "parent_id": cls.company.id,
            }
        )
        cls.affiliate = cls.partner_model.create(
            {
                "name": "Affiliate Company",
                "is_company": True,
                "parent_id": cls.company.id,
            }
        )

    def test_child_ids_excludes_companies(self):
        """child_ids should only include non-company children."""
        self.assertIn(self.contact, self.company.child_ids)
        self.assertNotIn(self.affiliate, self.company.child_ids)

    def test_affiliate_ids_includes_only_companies(self):
        """affiliate_ids should only include company children."""
        self.assertIn(self.affiliate, self.company.affiliate_ids)
        self.assertNotIn(self.contact, self.company.affiliate_ids)

    def test_child_ids_excludes_inactive(self):
        """child_ids should exclude inactive (archived) records."""
        self.contact.active = False
        # Re-read field to pick up domain filter
        self.company.invalidate_recordset()
        self.assertNotIn(self.contact, self.company.child_ids)

    def test_affiliate_ids_excludes_inactive(self):
        """affiliate_ids should exclude inactive (archived) affiliate companies."""
        self.affiliate.active = False
        self.company.invalidate_recordset()
        self.assertNotIn(self.affiliate, self.company.affiliate_ids)

    def test_multiple_affiliates(self):
        """A company can have multiple affiliate companies."""
        affiliate2 = self.partner_model.create(
            {
                "name": "Second Affiliate",
                "is_company": True,
                "parent_id": self.company.id,
            }
        )
        self.assertIn(self.affiliate, self.company.affiliate_ids)
        self.assertIn(affiliate2, self.company.affiliate_ids)
