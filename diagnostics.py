
import utils


def export(doc):
    lines = ['url', doc.url, ''] + ['title', doc.title, ''] + ['content'] + doc.paragraphs + ['']
    for k, v in doc.classified_paragraphs.items():
        lines.append(k)
        lines += v
        lines.append('')
    lines.append('qas')
    for qa in doc.qas:
        lines += ['------------------------', 'q:'+qa.question, 'a:'+qa.answer]
    utils.write_all_lines('./generate/{}.txt'.format(doc.title), lines)