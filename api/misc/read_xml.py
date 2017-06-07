import xml.etree.ElementTree as etree

with open('all_styles.xml', 'r') as sf:
    styles_xml = sf.read()

all_styles = []
styleguide = etree.fromstring(styles_xml)
for _class in styleguide.findall('class'):
    if _class.get('type') != 'beer':
        continue

    categories = _class.findall('category')
    for category in categories:
        subcategories = category.findall('subcategory')
        for subcategory in subcategories:
            _id = subcategory.get('id')
            name = subcategory.find('name').text
            all_styles.append({
                'key': _id, 'value': _id, 'text': '{0}. {1}'.format(_id, name)
            })

import ipdb; ipdb.set_trace()
