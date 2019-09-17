import random
from locust import task
import helper


class BackendCRMBehavior(helper.BaseBackendTaskSet):

    def on_start(self, *args, **kwargs):
        super(BackendCRMBehavior, self).on_start(*args, **kwargs)
        self.Lead = self.client.env['crm.lead']
        self.Sale = self.client.env['sale.order']

    @task(10)
    def create_lead(self):
        partner_rec = helper.find_random_customer(self.client)
        # site_rec = helper.find_random_site(self.client)
        # contract_type_rec = helper.search_browse(
        #    'contract.type',
        #    [('name', '=', 'Buyer/Sold Home')],
        #    )
        vals = {
            # 'name': site_rec.name,
            'name': partner_rec.name,
            'partner_id': partner_rec.id,
            # 'site_id': site_rec.id,
            # 'contract_type_id': contract_type_rec.id,
            }
        lead_id = self.Lead.create(vals)
        return lead_id

    @task(2)
    def mark_lead_won(self):
        domain = [('stage_id.name', 'not in', ['Won'])]
        lead_rec = helper.search_browse(
            self.client, 'crm.lead', domain, random_pick=True)
        return lead_rec.action_set_won_rainbowman()

    @task(2)
    def create_quotation(self):
        domain = [
            ('stage_id.name', '=', 'Won'),
            ('partner_id', '!=', False),
            ('order_ids', '=', False),
            ]
        lead_rec = helper.search_browse(
            self.client, 'crm.lead', domain, random_pick=True)
        vals = {
            'opportunity_id': lead_rec.id,
            'partner_id': lead_rec.partner_id.id,
            'partner_shipping_id': lead_rec.partner_id.id,
            }
        print('create_quotation %s %s' % (lead_rec.name, vals))
        sale_id = self.Sale.create(vals)
        return sale_id
