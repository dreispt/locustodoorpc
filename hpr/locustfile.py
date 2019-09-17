from locustodoorpc import OdooRPCLocust
import crm_lead


class BackendCRMUser(OdooRPCLocust):
    min_wait = 1000
    max_wait = 5000
    weight = 10
    task_set = crm_lead.BackendCRMBehavior
