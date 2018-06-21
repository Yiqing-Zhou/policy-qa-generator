from collections import defaultdict
import re

def parse_paragraphs(doc):
    lines = doc.content.split('\n')
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    doc.paragraphs = lines


def classify_paragraph(paragraph):
    if '是指' in paragraph:
        return 'definition'
    elif re.match('.+按照.+分为.+', paragraph) is not None:
        return 'classification'
    else:
        return 'unknown'


def classify_paragraphs(doc):
    doc.classified_paragraphs = defaultdict(lambda: [])
    unknown = 0
    for paragraph in doc.paragraphs:
        type = classify_paragraph(paragraph)
        if type != 'unknown':
            doc.classified_paragraphs[type].append(paragraph)
        else:
            unknown += 1
    doc.classified_paragraphs['unknown'].append(str(unknown))


if __name__ == '__main__':
    assert classify_paragraph('本办法所称税前扣除凭证,是指企业在计算企业所得税应纳税所得额时，证明与取得收入有关的、合理的支出实际发生，并据以税前扣除的各类凭证。') == 'definition'
    assert classify_paragraph('本办法所称企业是指企业所得税法及其实施条例规定的居民企业和非居民企业') == 'definition'
    assert classify_paragraph('税前扣除凭证按照来源分为内部凭证和外部凭证。') == 'classification'
