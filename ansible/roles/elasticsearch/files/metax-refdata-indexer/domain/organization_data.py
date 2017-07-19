from domain.indexable_data import IndexableData

class OrganizationData(IndexableData):
    '''
    Model class for organization data that can be indexed into Metax Elasticsearch
    '''

    DATA_TYPE_ORGANIZATION = 'organization'

    def __init__(
        self,
        org_id,
        label,
        broader_id='',
        broader_label=''):

        super(OrganizationData, self).__init__(org_id, OrganizationData.DATA_TYPE_ORGANIZATION)

        self.label = label # { 'fi': 'value1', 'en': 'value2',..., 'default': 'default_value' }
        self.broader_id = broader_id
        self.broader_label = broader_label

    def __str__(self):
        return (
            "{" +
                "\"org_id\":\"" + self.doc_id + "\","
                "\"label\":\"" + str(self.label) + "\","
                "\"broader_id\":\"" + self.broader_id + "\","
                "\"broader_label\":\"" + self.broader_label + "\""
            "}")