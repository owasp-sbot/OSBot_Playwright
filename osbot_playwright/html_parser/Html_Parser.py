from bs4 import BeautifulSoup


class Html_Parser:

    def __init__(self, data):
        self.soup = BeautifulSoup(data, 'html.parser')

    def __enter__(self): return self
    def __exit__ (self, type, value, traceback): pass

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

    def extract_elements(self, tag_type, attribute_name, key_name):
        elements = self.soup.find_all(tag_type)
        matches  = []
        for element in elements:
            if element.get(attribute_name):
                element_dict = { key_name: element[attribute_name],
                                'text'   : element.get_text()     }
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
        return [tag.text for tag in self.find_all(tag)]

    # content helpers

    def img_src(self, image_id): return self.id__attr(image_id, 'src')

    def options(self):
        return self.extract_elements('option', 'value', 'value')

    def hrefs(self):
        return self.extract_elements('a', 'href', 'href')

    def hrefs__values(self):
        return [link['href'] for link in self.hrefs()]

    def p(self): return self.paragraphs()

    def paragraphs(self):
        return [paragraph.text.strip() for paragraph in self.find_all("p")]

    def title(self):
        return self.soup.title.string if self.soup.title else None

    def __repr__(self):
        return self.soup.prettify()