import random
from locust import task, TaskSet


class BaseBackendTaskSet(TaskSet):

    def on_start(self):
        self.client.login(self.locust.db_name,
                          self.locust.login,
                          self.locust.password)


def search_browse(client, model, domain, random_pick=False):
    Model = client.env[model]
    record_ids = Model.search_read(domain, ['id'])
    if random_pick:
        record_ids = random.choice(record_ids)['id']
    browse_records = Model.browse(record_ids)
    return browse_records


def find_random_customer(client):
    model = 'res.partner'
    domain = [('customer', '=', True)]
    return search_browse(client, model, domain, random_pick=True)


def find_random_site(client):
    model = 'res.partner'
    domain = [('is_site', '=', True)]
    return search_browse(client, model, domain, random_pick=True)


def find_random_sellable_product(client, index=1):
    model = 'product.product'
    domain = [('sale_ok', '=', True)]
    return search_browse(client, model, domain, random_pick=True)
