
import utils


def export(doc):
    lines = ['url', doc.url, ''] + ['title', doc.title, ''] + ['content'] + doc.paragraphs + ['']
    for k, v in doc.classified_paragraphs.items():
        lines.append(k)
        lines += v
        lines.append('')
    utils.write_all_lines('./generate/{}.txt'.format(doc.title), lines)