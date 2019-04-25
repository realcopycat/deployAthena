#coding=utf-8
#test pyltp

import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from pyltp import NamedEntityRecognizer
from pyltp import SementicRoleLabeller

LTP_DIR = "/home/demo1/support_ltp"

segmentor = Segmentor()
segmentor.load(os.path.join(LTP_DIR, "cws.model"))
postagger = Postagger()
postagger.load(os.path.join(LTP_DIR, "pos.model"))
parser = Parser()
parser.load(os.path.join(LTP_DIR, "parser.model"))
recognizer = NamedEntityRecognizer()
recognizer.load(os.path.join(LTP_DIR, "ner.model"))
labeller = SementicRoleLabeller()
labeller.load(os.path.join(LTP_DIR, 'pisrl.model'))

while True:

    testsen=input('请输入句子：')

    words = segmentor.segment(testsen)
    print('\t'.join(words))

    postags = postagger.postag(words)
    print('\t'.join(postags))

    netags = recognizer.recognize(words, postags)
    print('\t'.join(netags))

    arcs = parser.parse(words, postags)
    print('\t'.join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

    roles = labeller.label(words, postags, arcs)
    for role in roles:
        print(role.index, " ".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]
        ))

input()

labeller.release()
parser.release()
recognizer.release()
postagger.release()
segmentor.release()

