# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.base_partner_company_group.tests.test_base_partner_company_group import (  # noqa: E501
    TestBasePartnerCompanyGroup,
)


class TestCrmPartnerCompanyGroup(TestBasePartnerCompanyGroup):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_group = cls.env["res.partner"].create(
            {"name": "CRM Company Group", "is_company": True}
        )
        cls.member_company = cls.env["res.partner"].create(
            {
                "name": "CRM Member Company",
                "is_company": True,
                "company_group_id": cls.company_group.id,
            }
        )

    def _create_lead(self, partner):
        return self.env["crm.lead"].create(
            {
                "name": "Test Opportunity",
                "partner_id": partner.id,
            }
        )

    def test_company_group_id_stored_on_lead(self):
        """company_group_id is stored on crm.lead via related field."""
        lead = self._create_lead(self.member_company)
        self.assertEqual(lead.company_group_id, self.company_group)

    def test_lead_without_company_group(self):
        """A lead for a partner without a company group has no company_group_id."""
        partner = self.env["res.partner"].create(
            {"name": "No Group CRM Partner", "is_company": True}
        )
        lead = self._create_lead(partner)
        self.assertFalse(lead.company_group_id)

    def test_company_group_id_updates_with_partner(self):
        """Updating the partner's company_group_id is reflected on the lead."""
        partner = self.env["res.partner"].create(
            {"name": "Changing CRM Partner", "is_company": True}
        )
        lead = self._create_lead(partner)
        self.assertFalse(lead.company_group_id)
        partner.write({"company_group_id": self.company_group.id})
        lead.invalidate_recordset()
        self.assertEqual(lead.company_group_id, self.company_group)
