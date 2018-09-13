import re
import json
import requests
from lxml import html

document = {'document_type': 'aws_service_status', 'aws_region': 'eu-west-1', 'aws_services': []}

pageContent=requests.get(
    'https://status.aws.amazon.com'
)
tree = html.fromstring(pageContent.content)
table_rows = tree.xpath('.//div[@id="EU_block"]/table[2]/tbody/tr')

for p in table_rows:
    service = str(p.xpath('td[2]/text()')[0])
    status = str(p.xpath('td[3]/text()')[0])

    if re.match(r'.*Ireland.*', service) is not None:
        match = re.match(r'(^.*[^\s])\s*\(([\w]+)\)', service)
        service_name = match.group(1)
        service_location = match.group(2)

        if re.match(r'Service is operating normally', status) is not None:
            status_condition = 'green'
        else:
            status_condition = 'red'

        document['aws_services'].append({'service_location': service_location, 'service_name': service_name,
                                         'status_text': status, 'status_condition': status_condition})
        # print(service, status)
        print(json.dumps(document, indent=2))
        with open('aws_service_status.json', 'w') as o:
            o.write(json.dumps(document, indent=4))















