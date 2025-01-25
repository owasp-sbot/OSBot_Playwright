from bs4                                    import BeautifulSoup
from osbot_utils.decorators.lists.index_by  import index_by
from osbot_utils.utils.Json                 import json_parse
from osbot_utils.utils.Str                  import trim


class Html_Parser:

    def __init__(self, data):
        self.raw_data = data
        self.soup     = BeautifulSoup(self.raw_data, 'html.parser')

    def __enter__(self): return self
    def __exit__ (self, type, value, traceback): pass

    def body(self):
        return self.soup.body

    def id__attr(self, id_to_find, attr_name):
        return self.id__attrs(id_to_find).get(attr_name)

    def id__attrs(self, id_to_find):
        match = self.soup.find(id=id_to_find)
        if match:
            return match.attrs
        return {}

    def class__contents(self, class_to_find):
        match = self.soup.find(class_=class_to_find)
        if match:
            return match.decode_contents()

    def class__text(self, class_to_find):
        match = self.soup.find(class_=class_to_find)
        if match:
            return match.text

    def class__texts(self, class_to_find):
        elements = self.soup.find_all(class_=class_to_find)
        matches = []
        for element in elements:
            matches.append(element.text)
        return matches

    def extract_elements(self, tag_type, attribute_name, key_name):
        elements = self.soup.find_all(tag_type)
        matches  = []
        for element in elements:
            if element.get(attribute_name):
                element_dict = { key_name: element[attribute_name],
                                'text'   : element.get_text()     }
                if element.get('id'):
                    element_dict['id'] = element.get('id')
                matches.append(element_dict)
        return matches

    def id__content(self, id_to_find):
        return self.soup.find(id=id_to_find).contents

    def id__content_decoded(self, id_to_find):
        match = self.soup.find(id=id_to_find)
        if match:
            return match.decode_contents()

    def id__html(self, id_to_find):
        return self.soup.find(id=id_to_find).decode_contents()

    def id__text(self, id_to_find):
        match = self.soup.find(id=id_to_find)
        if match:
            return match.text

    def ids__text(self, id_to_find):
        return [tag.text for tag in self.find_all(id=id_to_find)]

    def info(self):                                         # todo: see what error handling we need to add here
        info = dict(size      = len(self.raw_data),
                    text_size = len(self.text())  ,
                    title     = self.title()      )
        return info

    def json(self):
        return json_parse(self.text())

    def find(self, *args, **kwargs):
        return self.soup.find(*args, **kwargs)

    def find_all(self, *args, **kwargs):
        return self.soup.find_all(*args, **kwargs)

    def footer(self):
        return self.soup.footer.string if self.soup.footer else None

    def html(self):
        return self.soup.prettify()

    def select(self, query):
        result = self.soup.select(query)
        return [item.text for item in result]

    def tag__attrs(self, tag):
        match = self.soup.find(tag)
        if match:
            return match.attrs

    def tag__content(self, tag):
        return self.soup.find(tag).contents

    def tag__content_decoded(self, tag):
        match = self.soup.find(tag)
        if match:
            return match.decode_contents()

    def tag__html(self, tag):
        return self.soup.find(tag).decode_contents()

    def tag__text(self, tag):
        match = self.soup.find(tag)
        if match:
            return match.text

    @index_by
    def tags__attrs(self, tag):
        elements = self.soup.find_all(tag)
        result = []
        for element in elements:
            result.append(element.attrs)
        return result

    def tags__content(self, tag):
        elements = self.soup.find_all(tag)
        result = []
        for element in elements:
            result.extend(element.contents)
        return result

    def tags__text(self, tag):
        return [tag.text.strip() for tag in self.find_all(tag)] # todo: refactor to handle case when tag.text is None

    def tags__stats(self):
        stats = {}
        for tag in self.soup.find_all(True):
            tag_name = tag.name
            if tag_name in stats:
                stats[tag_name] += 1
            else:
                stats[tag_name] = 1
        return stats


    def text(self):
        return self.body().text

    # content helpers

    def img_src(self, image_id): return self.id__attr(image_id, 'src')

    def options(self):
        return self.extract_elements('option', 'value', 'value')

    @index_by
    def hrefs(self):
        return self.extract_elements('a', 'href', 'href')

    def hrefs__texts(self):
        return [link['text'] for link in self.hrefs()]

    def hrefs__values(self):
        return [link['href'] for link in self.hrefs()]

    def p(self): return self.paragraphs()

    def paragraphs(self):
        return [paragraph.text.strip() for paragraph in self.find_all("p")]

    def title(self):
        return str(self.soup.title.string) if self.soup.title else None

    def title_trimmed(self):
        return trim(self.title())

    def __repr__(self):
        return self.soup.prettify()