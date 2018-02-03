import os
from lxml import etree


UNICODE_INDEX = 0o001

SVG_TMPL = r'''<?xml version="1.0" standalone="no"?> 
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >
<svg xmlns="http://www.w3.org/2000/svg">
<defs>
  <font id="Material Design Icons Lite" horiz-adv-x="24">
    <font-face font-family="Material Design Icons Lite"
      units-per-em="512" ascent="448"
      descent="64" />
    <missing-glyph horiz-adv-x="0" />
{icons_info}  </font>
</defs>
</svg>
'''


SVG_ICON_TMPL = r'''    <glyph glyph-name="{name}"
      unicode="&#xF{index};"
      horiz-adv-x="24" d="{dinfo}" />
'''

def findd(fn):
    txt = open(fn, encoding='utf-8').read()
    i = txt.find(' d="')
    if i != -1:
        i += 4
        j = txt.find('"', i)
        return txt[i:j]
    else:
        raise BaseException("bad svg")


def get_index():
    global UNICODE_INDEX
    ret = '%03o' % UNICODE_INDEX
    UNICODE_INDEX += 1
    return ret


def main():
    lst = filter(lambda x: x, map(str.strip, open('icon-lst.txt', encoding='utf-8').readlines()))
    svgs = []
    for i in lst:
        fn = './MaterialDesign/icons/svg/%s.svg' % i
        if os.path.exists(fn):
            print(fn)
            d = findd(fn)
            svgs.append(SVG_ICON_TMPL.format(name=i, dinfo=d, index=get_index()))
        else:
            print(fn, 'not found!')
    svg = SVG_TMPL.format(icons_info=''.join(svgs))
    open('out.svg', 'w', encoding='utf-8').write(svg)


if __name__ == '__main__':
    main()

