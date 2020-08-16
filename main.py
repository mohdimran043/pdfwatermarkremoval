from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import ContentStream
from PyPDF2.generic import TextStringObject, NameObject
from PyPDF2.utils import b_
import numpy as np

file = open('tmp/source.pdf', "rb")

output = PdfFileWriter()
source = PdfFileReader(file)

print(source.getDocumentInfo())


def guess_codes(s):
    avaiable_c = []

    codes = 'ascii,big5,big5hkscs,cp037,cp273,cp424,cp437,cp500,cp720,cp737,cp775,cp850,cp852,cp855,cp856,cp857,cp858,cp860,cp861,cp862,cp863,cp864,cp865,cp866,cp869,cp874,cp875,cp932,cp949,cp950,cp1006,cp1026,cp1125,cp1140,cp1250,cp1251,cp1252,cp1253,cp1254,cp1255,cp1256,cp1257,cp1258,cp65001,euc_jp,euc_jis_2004,euc_jisx0213,euc_kr,gb2312,gbk,gb18030,hz,iso2022_jp,iso2022_jp_1,iso2022_jp_2,iso2022_jp_2004,iso2022_jp_3,iso2022_jp_ext,iso2022_kr,latin_1,iso8859_2,iso8859_3,iso8859_4,iso8859_5,iso8859_6,iso8859_7,iso8859_8,iso8859_9,iso8859_10,iso8859_11,iso8859_13,iso8859_14,iso8859_15,iso8859_16,johab,koi8_r,koi8_t,koi8_u,kz1048,mac_cyrillic,mac_greek,mac_iceland,mac_latin2,mac_roman,mac_turkish,ptcp154,shift_jis,shift_jis_2004,shift_jisx0213,utf_32,utf_32_be,utf_32_le,utf_16,utf_16_be,utf_16_le,utf_7,utf_8,utf_8_sig'.split(
        ',')
    if not isinstance(s, bytes):
        for c in codes:
            try:
                s.decode(c)
                print(c)
                avaiable_c.append(c)
            except Exception:
                pass

    return avaiable_c



target_locations = np.array([
    [0.70711, 0.70711, -0.70711, 0.70711, -308.753, -165.279],
    [1, 0, 0, 1, -44.831, 54.605]])


def match_location(location, target, epsilon=1e-5):
    # targe must be n*6 numpy matrix
    return np.any(np.abs(np.array([i.as_numeric() for i in location]) - target).max(axis=1) < epsilon)


for p in range(source.getNumPages()):
    page = source.getPage(p)
    # print(page.extractText())
    #content_object, = page["/Contents"][0].getObject()
    content_object = page["/Contents"][1]

    content = ContentStream(content_object, source)
    for operands, operator in content.operations:
        # print(operator, operands) # pdf元素的类型和值
	
	# 主要的代码在这里，使用各种方式找到水印可识别的特征
        # if operator == b_("TJ"): # `b_`只是python2/3中bytes类型转换的冗余代码
        #     text = operands[0][0]
        #     # if isinstance(text, bytes):
        #     #     print('====  ', text, '  ====')
        #     #     for c in guess_codes(text):
        #     #         print(c, text.decode(c))
        #     if isinstance(text, TextStringObject) and text in target_str:
        #         operands[0] = TextStringObject('')

        if operator == b_("cm") and match_location(operands, target_locations):
            operands[:] = []

    page.__setitem__(NameObject('/Contents'), content)
    output.addPage(page)


outputStream = open("tmp/output.pdf", "wb")
output.write(outputStream)
outputStream.close()

file.close()