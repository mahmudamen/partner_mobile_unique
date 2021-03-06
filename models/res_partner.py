# Copyright 2016 Antonio Espinosa
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains("mobile", "is_company", "company_id")
    def _check_mobile(self):
        for partner in self.filtered("mobile"):
            # If the company is not defined in the partner, take current user company
            company = partner.company_id or self.env.company
            mode = company.partner_mobile_unique
            if mode == "all" or (mode == "companies" and partner.is_company):
                domain = [
                    ("id", "!=", partner.id),
                    ("mobile", "=", partner.mobile),
                ]
                if mode == "companies":
                    domain.append(("is_company", "=", True))
                other = self.search(domain)
                # Don't raise when coming from contact merge wizard or no duplicates
                if other and not self.env.context.get("partner_mobile_unique_merging"):
                    raise ValidationError(
                        _("This Mobile number is equal to partner '%s'")
                        % other[0].display_name
                    )
