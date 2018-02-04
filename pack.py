import os
import json
import subprocess

FONTFORGE_PATH = r'D:\Program Files (x86)\FontForgeBuilds\bin'
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

CSS_TMPL = r'''@font-face {
  font-family: "Material Design Icons Lite";
  src: url("mdi-lite.svg?v=2.1.19#materialdesigniconsregular") format("svg");
  font-weight: normal;
  font-style: normal;
}
.mdi:before,
.mdi-set {
  display: inline-block;
  font: normal normal normal 24px/1 "Material Design Icons Lite";
  font-size: inherit;
  text-rendering: auto;
  line-height: inherit;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
{FLAG}
.mdi-18px.mdi-set, .mdi-18px.mdi:before {
  font-size: 18px;
}

.mdi-24px.mdi-set, .mdi-24px.mdi:before {
  font-size: 24px;
}

.mdi-36px.mdi-set, .mdi-36px.mdi:before {
  font-size: 36px;
}

.mdi-48px.mdi-set, .mdi-48px.mdi:before {
  font-size: 48px;
}

.mdi-dark:before {
  color: rgba(0, 0, 0, 0.54);
}
.mdi-dark.mdi-inactive:before {
  color: rgba(0, 0, 0, 0.26);
}

.mdi-light:before {
  color: white;
}
.mdi-light.mdi-inactive:before {
  color: rgba(255, 255, 255, 0.3);
}

.mdi-rotate-45 {
  /*
  // Not included in production
  &.mdi-flip-h:before {
      -webkit-transform: scaleX(-1) rotate(45deg);
      transform: scaleX(-1) rotate(45deg);
      filter: FlipH;
      -ms-filter: "FlipH";
  }
  &.mdi-flip-v:before {
      -webkit-transform: scaleY(-1) rotate(45deg);
      -ms-transform: rotate(45deg);
      transform: scaleY(-1) rotate(45deg);
      filter: FlipV;
      -ms-filter: "FlipV";
  }
  */
}
.mdi-rotate-45:before {
  -webkit-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
}

.mdi-rotate-90 {
  /*
  // Not included in production
  &.mdi-flip-h:before {
      -webkit-transform: scaleX(-1) rotate(90deg);
      transform: scaleX(-1) rotate(90deg);
      filter: FlipH;
      -ms-filter: "FlipH";
  }
  &.mdi-flip-v:before {
      -webkit-transform: scaleY(-1) rotate(90deg);
      -ms-transform: rotate(90deg);
      transform: scaleY(-1) rotate(90deg);
      filter: FlipV;
      -ms-filter: "FlipV";
  }
  */
}
.mdi-rotate-90:before {
  -webkit-transform: rotate(90deg);
  -ms-transform: rotate(90deg);
  transform: rotate(90deg);
}

.mdi-rotate-135 {
  /*
  // Not included in production
  &.mdi-flip-h:before {
      -webkit-transform: scaleX(-1) rotate(135deg);
      transform: scaleX(-1) rotate(135deg);
      filter: FlipH;
      -ms-filter: "FlipH";
  }
  &.mdi-flip-v:before {
      -webkit-transform: scaleY(-1) rotate(135deg);
      -ms-transform: rotate(135deg);
      transform: scaleY(-1) rotate(135deg);
      filter: FlipV;
      -ms-filter: "FlipV";
  }
  */
}
.mdi-rotate-135:before {
  -webkit-transform: rotate(135deg);
  -ms-transform: rotate(135deg);
  transform: rotate(135deg);
}

.mdi-rotate-180 {
  /*
  // Not included in production
  &.mdi-flip-h:before {
      -webkit-transform: scaleX(-1) rotate(180deg);
      transform: scaleX(-1) rotate(180deg);
      filter: FlipH;
      -ms-filter: "FlipH";
  }
  &.mdi-flip-v:before {
      -webkit-transform: scaleY(-1) rotate(180deg);
      -ms-transform: rotate(180deg);
      transform: scaleY(-1) rotate(180deg);
      filter: FlipV;
      -ms-filter: "FlipV";
  }
  */
}
.mdi-rotate-180:before {
  -webkit-transform: rotate(180deg);
  -ms-transform: rotate(180deg);
  transform: rotate(180deg);
}

.mdi-rotate-225 {
  /*
  // Not included in production
  &.mdi-flip-h:before {
      -webkit-transform: scaleX(-1) rotate(225deg);
      transform: scaleX(-1) rotate(225deg);
      filter: FlipH;
      -ms-filter: "FlipH";
  }
  &.mdi-flip-v:before {
      -webkit-transform: scaleY(-1) rotate(225deg);
      -ms-transform: rotate(225deg);
      transform: scaleY(-1) rotate(225deg);
      filter: FlipV;
      -ms-filter: "FlipV";
  }
  */
}
.mdi-rotate-225:before {
  -webkit-transform: rotate(225deg);
  -ms-transform: rotate(225deg);
  transform: rotate(225deg);
}

.mdi-rotate-270 {
  /*
  // Not included in production
  &.mdi-flip-h:before {
      -webkit-transform: scaleX(-1) rotate(270deg);
      transform: scaleX(-1) rotate(270deg);
      filter: FlipH;
      -ms-filter: "FlipH";
  }
  &.mdi-flip-v:before {
      -webkit-transform: scaleY(-1) rotate(270deg);
      -ms-transform: rotate(270deg);
      transform: scaleY(-1) rotate(270deg);
      filter: FlipV;
      -ms-filter: "FlipV";
  }
  */
}
.mdi-rotate-270:before {
  -webkit-transform: rotate(270deg);
  -ms-transform: rotate(270deg);
  transform: rotate(270deg);
}

.mdi-rotate-315 {
  /*
  // Not included in production
  &.mdi-flip-h:before {
      -webkit-transform: scaleX(-1) rotate(315deg);
      transform: scaleX(-1) rotate(315deg);
      filter: FlipH;
      -ms-filter: "FlipH";
  }
  &.mdi-flip-v:before {
      -webkit-transform: scaleY(-1) rotate(315deg);
      -ms-transform: rotate(315deg);
      transform: scaleY(-1) rotate(315deg);
      filter: FlipV;
      -ms-filter: "FlipV";
  }
  */
}
.mdi-rotate-315:before {
  -webkit-transform: rotate(315deg);
  -ms-transform: rotate(315deg);
  transform: rotate(315deg);
}

.mdi-flip-h:before {
  -webkit-transform: scaleX(-1);
  transform: scaleX(-1);
  filter: FlipH;
  -ms-filter: "FlipH";
}

.mdi-flip-v:before {
  -webkit-transform: scaleY(-1);
  transform: scaleY(-1);
  filter: FlipV;
  -ms-filter: "FlipV";
}

.mdi-spin:before {
  -webkit-animation: mdi-spin 2s infinite linear;
  animation: mdi-spin 2s infinite linear;
}

@-webkit-keyframes mdi-spin {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(359deg);
    transform: rotate(359deg);
  }
}
@keyframes mdi-spin {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(359deg);
    transform: rotate(359deg);
  }
}
'''

CSS_ITEM_TMPL = r'''
.mdi-{name}:before {{
  content: "\F{index}";
}}
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
    ret = '%03x' % UNICODE_INDEX
    UNICODE_INDEX += 1
    return ret


def main():
    os.path.insert(0, FONTFORGE_PATH)
    lst = filter(lambda x: x, map(str.strip, open('icon-lst.txt', encoding='utf-8').readlines()))
    svg_lst = []
    css_lst = []
    item_lst = []
    
    for i in lst:
        fn = './MaterialDesign/icons/svg/%s.svg' % i
        if os.path.exists(fn):
            print(fn)
            d = findd(fn)
            index = get_index()
            svg_lst.append(SVG_ICON_TMPL.format(name=i, dinfo=d, index=index))
            css_lst.append(CSS_ITEM_TMPL.format(name=i, index=index))
            item_lst.append({'name': i, 'hex': 'f' + index})
        else:
            print(fn, 'not found!')

    svg = SVG_TMPL.format(icons_info=''.join(svg_lst))
    css = CSS_TMPL.replace('{FLAG}', ''.join(css_lst))

    HTML_TMPL = open('preview.tmpl', 'r', encoding='utf-8').read()
    html = HTML_TMPL.replace('{FLAG}', json.dumps(item_lst))
    
    p = subprocess.Popen(['fontforge'],

    open('dist/mdi-lite.svg', 'w', encoding='utf-8').write(svg)
    open('dist/mdi-lite.css', 'w', encoding='utf-8').write(css)
    open('dist/preview.html', 'w', encoding='utf-8').write(html)


if __name__ == '__main__':
    main()

