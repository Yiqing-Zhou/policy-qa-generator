
#http://www.chinatax.gov.cn/n810341/n810755/index.html
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


'''
本公告自发布后30日起施行。此前尚未处理的涉税事项按本公告执行。
q:关于个人投资者收购企业股权后将原盈余积累转增股本个人所得税问题的公告自何时起施行
a:自发布（2013-05-14）后30日起施行。此前尚未处理的涉税事项按本公告执行。
'''
def transform_schedule(paragraph):
    m = re.search('(本.+)自(.*)起(.*?)[，|。|；]', paragraph)
    subj = m.span(1)
    verb = m.span(3)
    question = paragraph[subj[0]:subj[1]] + '自何时起' + paragraph[verb[0]:verb[1]]
    answer = paragraph[subj[1]:]
    return question, answer

'''
二、境内机构和个人（以下称备案人）在办理对外支付税务备案时，应向主管国税机关提交加盖公章的合同（协议）或相关交易凭证复印件（外文文本应同时附送中文译本），并填报《服务贸易等项目对外支付税务备案表》（一式三份，以下简称《备案表》，见附件1）。
q:境内机构和个人（以下称备案人）怎样办理对外支付税务备案
a:向主管国税机关提交加盖公章的合同（协议）或相关交易凭证复印件（外文文本应同时附送中文译本）并填报服务贸易等项目对外支付税务备案表（一式三份以下简称备案表见附件1）。
'''
def transform_instruction(paragraph):
    m = re.search('(.*)在(.*)时，应(.*)', paragraph)
    subj = m.span(1)
    acti = m.span(2)
    inst = m.span(3)
    question = paragraph[subj[0]:subj[1]] + '怎样' + paragraph[acti[0]:acti[1]]
    answer = paragraph[inst[0]:]
    return question, answer

def transform_doc(doc):
    doc.qas = []
    transformers = {
        'definition': transform_definition,
        'classification': transform_classification,
        'schedule': transform_schedule,
        'instruction': transform_instruction
    }
    for type, paragraphs in doc.classified_paragraphs.items():
        if type != 'unknown':
            for paragraph in paragraphs:
                question, answer = transformers[type](paragraph)
                question = normalize(doc, question)
                answer = normalize(doc, answer)
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
    prefix = ['本规定', '本通知', '本公告', '本条', '本补充公告']
    for p in prefix:
        if text.startswith(p):
            return title + text[len(p):]
    return text


def substitute_publishDate(text, publishDate):
    refer = ['公告之日', '发布之日', '公告后', '发布后']
    for r in refer:
        if r in text:
            m = re.search('(公告|发布).*', text)
            publ = m.span(1)
            text = text[:publ[1]] + '（{0}）' + text[publ[1]:]
            return text.format(publishDate)
    return text


def normalize(doc, text):
    text = remove_bullet(text)
    text = remove_punction(text)
    text = substitute_pronoun(text, doc.title)
    text = substitute_publishDate(text, doc.publishDate)
    return text
