import json
import requests
import xml.etree.cElementTree as ET
import os
from domain.reference_data import ReferenceData

class MimeDataService:
    '''
    Service for getting mime type reference data for elasticsearch index. The data is in iana.org,
    so it is first fetched and parsed.
    '''

    IANA_NS = '{http://www.iana.org/assignments}'
    MIME_TYPE_REFERENCE_DATA_SOURCE_URL = 'https://www.iana.org/assignments/media-types/media-types.xml'
    MIME_TYPE_REGISTRY_IDS = [  'application',
                                'audio',
                                'font',
                                'image',
                                'message',
                                'model',
                                'multipart',
                                'text',
                                'video']

    TEMP_XML_FILENAME = '/tmp/data.xml'

    def get_data(self):
        self._fetch_mime_data()
        index_data_models = self._parse_mime_data()
        os.remove(self.TEMP_XML_FILENAME)

        # i=0
        # while i < 10:
        #     print(index_data_models[i], sep='\n\n')
        #     i = i+1

        return index_data_models

    def _parse_mime_data(self):
        data_type = ReferenceData.DATA_TYPE_MIME_TYPE
        index_data_models = []
        print("Extracting relevant data from the fetched data")

        is_parsing_model_elem = False
        found_valid_file_elem = False
        found_valid_name_elem = False
        for event, elem in ET.iterparse(self.TEMP_XML_FILENAME, events=("start", "end")):
            if event == 'start':
                if elem.tag == (self.IANA_NS + 'registry') and elem.get('id') in self.MIME_TYPE_REGISTRY_IDS:
                    is_parsing_model_elem = True
                    registry_name = elem.get('id')
                if is_parsing_model_elem and elem.tag == (self.IANA_NS + 'name'):
                    if elem.text:
                        label = dict()
                        found_valid_name_elem = True
                        uri = 'https://www.iana.org/assignments/media-types/' + registry_name + "/" + elem.text
                        label['fi'] = registry_name + "/" + elem.text
                        label['en'] = registry_name + "/" + elem.text
                        data_id = registry_name + "/" + elem.text
                if is_parsing_model_elem and elem.tag == (self.IANA_NS + 'file') and elem.get('type') == 'template':
                    if elem.text:
                        label = dict()
                        found_valid_file_elem = True
                        uri = 'https://www.iana.org/assignments/media-types/' + elem.text
                        label['fi'] = elem.text
                        label['en'] = elem.text
                        data_id = elem.text
            elif event == 'end':
                if elem.tag == self.IANA_NS + 'registry':
                    is_parsing_model_elem = False
                if is_parsing_model_elem and elem.tag == (self.IANA_NS + 'record'):
                    if found_valid_file_elem or found_valid_name_elem:
                        index_data_models.append(ReferenceData(data_id, data_type, label, uri))
                    found_valid_file_elem = False
                    found_valid_name_elem = False

        return index_data_models

    def _fetch_mime_data(self):
        url = self.MIME_TYPE_REFERENCE_DATA_SOURCE_URL
        print("Fetching data from url " + url)
        response = requests.get(url, stream=True)
        with open(self.TEMP_XML_FILENAME, 'wb') as handle:
            for block in response.iter_content(1024):
                handle.write(block)