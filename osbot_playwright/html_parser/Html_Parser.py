from bs4 import BeautifulSoup
from osbot_utils.utils.Misc import unique


class Html_Parser:

    def __init__(self, data):
        self.soup = BeautifulSoup(data, 'html.parser')

    def __enter__(self): return self
    def __exit__ (self, type, value, traceback): pass

    def id__attrs(self, id_to_find):
        match = self.soup.find(id=id_to_find)
        if match:
            return match.attrs

    def class__contents(self, class_to_find):
        match = self.soup.find(class_=class_to_find)
        if match:
            return match.decode_contents()

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

    def tag__attrs(self, tag):
        match = self.soup.find(tag)
        if match:
            return match.attrs

    def find(self, *args, **kwargs):
        return self.soup.find(*args, **kwargs)

    def find_all(self, *args, **kwargs):
        return self.soup.find_all(*args, **kwargs)

    def footer(self):
        return self.soup.footer.string if self.soup.footer else None

    def html(self):
        return self.soup.prettify()

    def paragraphs(self):
        return [paragraph.text.strip() for paragraph in self.find_all("p")]

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

    def tags__content(self, tag):
        elements = self.soup.find_all(tag)
        result = []
        for element in elements:
            result.extend(element.contents)
        return unique(result)


    def tags__text(self, tag):
        return [tag.text for tag in self.find_all(tag)]



    def title(self):
        return self.soup.title.string if self.soup.title else None



    def p(self): return self.paragraphs()

    def select(self, query):
        result = self.soup.select(query)
        return [item.text for item in result]

    def __repr__(self):
        return self.soup.prettify()