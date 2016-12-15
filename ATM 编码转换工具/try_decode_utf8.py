# encoding=utf8
import re
import codecs
from binascii import hexlify, unhexlify


def display_unicode():
    unicode_dic = {}

    regex = "u\{\w{4}\}"

    with codecs.open("test.txt", "r", encoding="utf8") as f:
        unicode_content = f.read().replace("\\", "")

    regex_res = re.findall(regex, unicode_content)

    for each in regex_res:
        test = r"\u" + each.replace("u{", "").replace("}", "")
        unicode_dic[each] = test.encode("utf8").decode("unicode_escape")

    output = unicode_content
    for eachkey in unicode_dic:
        output = output.replace(eachkey, unicode_dic[eachkey])

    with codecs.open("ok.txt", "w", encoding="utf8") as f:
        f.write(output)


if __name__ == "__main__":
    display_unicode()
