# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.base_partner_company_group.tests.test_base_partner_company_group import (  # noqa: E501
    TestBasePartnerCompanyGroup,
)


class TestAccountPartnerCompanyGroup(TestBasePartnerCompanyGroup):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_group = cls.env["res.partner"].create(
            {"name": "Test Company Group", "is_company": True}
        )
        cls.member_company = cls.env["res.partner"].create(
            {
                "name": "Member Company",
                "is_company": True,
                "company_group_id": cls.company_group.id,
            }
        )

    def _create_invoice(self, partner):
        return self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": partner.id,
            }
        )

    def test_company_group_id_stored_on_invoice(self):
        """company_group_id is stored on account.move via related field."""
        invoice = self._create_invoice(self.member_company)
        self.assertEqual(invoice.company_group_id, self.company_group)

    def test_invoice_without_company_group(self):
        """An invoice for a partner without a company group has no company_group_id."""
        partner = self.env["res.partner"].create(
            {"name": "No Group Partner", "is_company": True}
        )
        invoice = self._create_invoice(partner)
        self.assertFalse(invoice.company_group_id)

    def test_company_group_id_updates_with_partner(self):
        """Updating the partner's company_group_id is reflected on the invoice."""
        partner = self.env["res.partner"].create(
            {"name": "Changing Partner", "is_company": True}
        )
        invoice = self._create_invoice(partner)
        self.assertFalse(invoice.company_group_id)
        partner.write({"company_group_id": self.company_group.id})
        invoice.invalidate_recordset()
        self.assertEqual(invoice.company_group_id, self.company_group)
