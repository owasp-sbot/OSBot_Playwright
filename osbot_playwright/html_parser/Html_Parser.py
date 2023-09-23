from bs4 import BeautifulSoup
from osbot_utils.utils.Misc import unique


class Html_Parser:

    def __init__(self, data):
        self.soup = BeautifulSoup(data, 'html.parser')

    def __enter__(self): return self
    def __exit__ (self, type, value, traceback): pass

    def content__with_id(self, id_to_find):
        return self.soup.find(id=id_to_find).contents

    def content__with_tag(self, tag):
        return self.soup.find(tag).contents

    def content_all__with_tag(self, tag):
        elements = self.soup.find_all(tag)
        result = []
        for element in elements:
            result.extend(element.contents)
        return unique(result)

    def find(self, *args, **kwargs):
        return self.soup.find(*args, **kwargs)

    def find_all(self, *args, **kwargs):
        return self.soup.find_all(*args, **kwargs)

    def footer(self):
        return self.soup.footer.string if self.soup.footer else None

    def html(self):
        return self.soup.prettify()

    def html__with_id(self, id_to_find):
        return self.soup.find(id=id_to_find).decode_contents()

    def html__with_tag(self, tag):
        return self.soup.find(tag).decode_contents()

    def paragraphs(self):
        return [paragraph.text.strip() for paragraph in self.find_all("p")]

    def text_in_all__id(self, id_to_find):
        return [tag.text for tag in self.find_all(id=id_to_find)]

    def text_in_all__tag(self, tag):
        return [tag.text for tag in self.find_all(tag)]

    def text_in_tag(self, tag):
        match = self.soup.find(tag)
        if match:
            return match.text

    def title(self):
        return self.soup.title.string if self.soup.title else None

    def with_class(self, class_to_find):
        match = self.soup.find(class_=class_to_find)
        if match:
            return match.decode_contents()

    def with_id(self, id_to_find):
        match = self.soup.find(id=id_to_find)
        if match:
            return match.decode_contents()

    def with_tag(self, tag):                                    # todo refactor to use self.decode_contents (which can handle the None scenario)
        match = self.soup.find(tag)
        if match:
            return match.decode_contents()

    def p(self): return self.paragraphs()

    def select(self, query):
        result = self.soup.select(query)
        return [item.text for item in result]

    def __repr__(self):
        return self.soup.prettify()