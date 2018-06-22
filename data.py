import utils
import config
import re

def replace_span(pattern, index, repl, string):
    m = re.search(pattern, string)
    if m is None:
        return string
    s = m.span(index)
    return string[:s[0]] + repl + string[s[1]:]


class PolicyDoc(object):
    def __init__(self, url, title, content):
        self.url = url
        self.title = title
        self.content = self.process_chars(content)


    def process_chars(self, content):
        r = content
        r = r.replace(',', '，')
        r = re.sub('[\xa0|\ue003|\ue004|\u3000]+', '\n', r)
        r = replace_span(r'(\s+)第.+[章|条]', 1, '\n', r)
        r = re.sub('总[ ]+则', '总则', r)
        return r


def load_documents():
    samples = utils.load_json(config.data_file)
    docs = []
    for sample in samples:
        doc = PolicyDoc(sample['url'], sample['title'], sample['content'])
        docs.append(doc)
    return docs
