import random
from locust import task
import helper


class BackendCRMBehavior(helper.BaseBackendTaskSet):

    def on_start(self, *args, **kwargs):
        super(BackendCRMBehavior, self).on_start(*args, **kwargs)
        self.Lead = self.client.env['crm.lead']

    @task
    def create_lead(self):
        partner_rec = helper.find_random_customer(self.client)
        # site_rec = helper.find_random_site(self.client)
        # contract_type_rec = helper.search_browse(
        #    'contract.type',
        #    [('name', '=', 'Buyer/Sold Home')],
        #    )
        values = {
            # 'name': site_rec.name,
            'name': partner_rec.name,
            'partner_id': partner_rec.id,
            # 'site_id': site_rec.id,
            # 'contract_type_id': contract_type_rec.id,
            }
        lead_id = self.Lead.create(values)
        return lead_id
