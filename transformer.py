
import re

class QuestionAnswer(object):
    def __init__(self, type, question, answer):
        self.type = type
        self.question = question
        self.answer = answer


'''
第二条  本办法所称税前扣除凭证，是指企业在计算企业所得税应纳税所得额时，证明与取得收入有关的、合理的支出实际发生，并据以税前扣除的各类凭证。
q:税前扣除凭证是指什么？
a:是指企业在计算企业所得税应纳税所得额时，证明与取得收入有关的、合理的支出实际发生，并据以税前扣除的各类凭证。

本办法所称企业是指企业所得税法及其实施条例规定的居民企业和非居民企业
q:[本办法]+企业所得税税前扣除凭证管理办法|所称企业是指什么？
a:是指企业所得税法及其实施条例规定的居民企业和非居民企业
'''

def transform_definition(paragraph):
    span = re.search('是指', paragraph).span()
    question = paragraph[:span[0]] + '是指什么'
    answer = paragraph[span[0]:]
    return question, answer


'''
税前扣除凭证按照来源分为内部凭证和外部凭证。
q:税前扣除凭证有哪些来源
a:按照来源分为内部凭证和外部凭证。
'''
def transform_classification(paragraph):
    m = re.search('(.*)按照(.*)分为(.*)', paragraph)
    subj = m.span(1)
    type = m.span(2)
    question = paragraph[subj[0]:subj[1]] + '有哪些' + paragraph[type[0]:type[1]]
    answer = paragraph[subj[1]:]
    return question, answer


def transform_doc(doc):
    doc.qas = []
    transformers = {
        'definition': transform_definition,
        'classification': transform_classification
    }
    for type, paragraphs in doc.classified_paragraphs.items():
        if type != 'unknown':
            for paragraph in paragraphs:
                question, answer = transformers[type](paragraph)
                question = normalize(doc, question)
                doc.qas.append(QuestionAnswer(type, question, answer))


def remove_bullet(text):
    pattern = r'(\s*（.*?）\s*)|(\s*第.+条\s*)|([一二三四五六七八九十]+[\s、]+)'
    m = re.search(pattern, text)
    if m is not None:
        span = m.span()
        if span[0] == 0:
            return text[span[1]:]
    return text


def remove_punction(text):
    r = text
    r = re.sub('[《》，]', '', r)
    return r


def substitute_pronoun(text, title):
    prefix = ['本规定', '本通知', '本公告', '本条']
    for p in prefix:
        if text.startswith(p):
            return title + text[len(p):]
    return text


def normalize(doc, text):
    text = remove_bullet(text)
    text = remove_punction(text)
    text = substitute_pronoun(text, doc.title)
    return text
