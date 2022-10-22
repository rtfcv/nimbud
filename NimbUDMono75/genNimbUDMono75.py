import fontforge as ff
from concurrent import futures

scaleEm = "1000"

fontName = "NimbUDMono75"


class FINFO:
    def __init__(self, weight: str, baseFont: str, secondFont: str) -> None:
        self.weight = weight
        self.baseFont = baseFont
        self.secondFont = secondFont


todoList = [
    FINFO(
        'Regular',
        "../srcfonts/urw-core35-fonts/NimbusMonoPS-Regular.otf",
        "../srcfonts/morisawa-biz-ud-mincho/fonts/ttf/BIZUDMincho-Regular.ttf"
    ),
    FINFO(
        'Bold',
        "../srcfonts/urw-core35-fonts/NimbusMonoPS-Bold.otf",
        "../srcfonts/morisawa-biz-ud-gothic/fonts/ttf/BIZUDGothic-Bold.ttf"
    ),
    FINFO(
        'Italic',
        "../srcfonts/urw-core35-fonts/NimbusMonoPS-Italic.otf",
        "../srcfonts/morisawa-biz-ud-gothic/fonts/ttf/BIZUDGothic-Regular.ttf"
    ),
    FINFO(
        'BoldItalic',
        "../srcfonts/urw-core35-fonts/NimbusMonoPS-BoldItalic.otf",
        "../srcfonts/morisawa-biz-ud-gothic/fonts/ttf/BIZUDGothic-Bold.ttf"
    ),

]


def cpOS2(src, dest):
    dest.os2_codepages = src.os2_codepages
    # dest.os2_family_class = src.os2_family_class
    dest.os2_fstype = src.os2_fstype
    dest.os2_stylemap = src.os2_stylemap
    dest.os2_panose = src.os2_panose
    dest.os2_strikeypos = src.os2_strikeypos
    dest.os2_strikeysize = src.os2_strikeysize
    dest.os2_subxoff = src.os2_subxoff
    dest.os2_subxsize = src.os2_subxsize
    dest.os2_subyoff = src.os2_subyoff
    dest.os2_subysize = src.os2_subysize
    dest.os2_supxoff = src.os2_supxoff
    dest.os2_supxsize = src.os2_supxsize
    dest.os2_supyoff = src.os2_supyoff
    dest.os2_supysize = src.os2_supysize
    dest.os2_typoascent = src.os2_typoascent
    dest.os2_typoascent_add = src.os2_typoascent_add
    # dest.os2_typodescent = src.os2_typodescent
    # dest.os2_typodescent_add = src.os2_typodescent_add
    dest.os2_typolinegap = src.os2_typolinegap
    dest.os2_use_typo_metrics = src.os2_use_typo_metrics
    dest.os2_unicoderanges = src.os2_unicoderanges
    dest.os2_vendor = src.os2_vendor
    dest.os2_version = src.os2_version
    # dest.os2_weight = src.os2_weight
    # dest.os2_weight_width_slope_only = src.os2_weight_width_slope_only
    dest.os2_width = src.os2_width
    dest.os2_winascent = src.os2_winascent
    dest.os2_winascent_add = src.os2_winascent_add
    # dest.os2_windescent = src.os2_windescent
    # dest.os2_windescent_add = src.os2_windescent_add

    dest.head_optimized_for_cleartype = src.head_optimized_for_cleartype
    dest.hhea_ascent = src.hhea_ascent
    dest.hhea_ascent_add = src.hhea_ascent_add
    # dest.hhea_descent = src.hhea_descent
    # dest.hhea_descent_add = src.hhea_descent_add
    dest.hhea_linegap = src.hhea_linegap
    return dest


def font_merger(i: FINFO):
    alt: ff.font = ff.open(i.secondFont)
    print(f'alt font is: {alt["A"].width}x{alt["A"].vwidth}')
    print(f'em for alt font is: {alt.em}')
    altwid = alt['A'].width

    base: ff.font = ff.open(i.baseFont)
    print(f'base font is: {base["A"].width}x{base["A"].vwidth}')
    print(f'em for base font is: {base.em}')
    print(f'{i.baseFont} is {base.weight}-----------------------------------------------------------------')

    base.em = alt.em
    base.design_size = alt.design_size

    print(f'base font changed to: {base["A"].width}x{base["A"].vwidth}')
    print(f'em for base changed to: {base.em}')

    basewid = base['A'].width

    base.selection.all()
    base.nltransform(f'x*{altwid}/{basewid}', 'y')

    for g in base:
        if base[g].isWorthOutputting():
            __origwid = base[g].width
            base[g].width = int(__origwid/basewid*altwid)

    print(f'base font changed to: {base["A"].width}x{base["A"].vwidth}')

    # merge fonts
    base.mergeFonts(alt)

    # transform all glyphs
    newWid: int = int(0.75*altwid)
    base.nltransform(f'x*{newWid}/{altwid}', 'y')

    def convBase(g):
        if base[g].isWorthOutputting():
            if base[g].width == altwid:
                base[g].width = newWid
            else:
                base[g].width = 2*newWid
    list(map(convBase, base))
    # base.addLookup('ligatures', 'gsub_ligature', 'ignore_ligatures', [['liga', [['latn', ['dflt']]]]])
    print(base['ff'].glyphclass)

    list(map(base.removeGlyph, ('fi','ff','fl','ffi','ffl')))

    # fix metadata
    base = cpOS2(src=alt, dest=base)
    base.os2_panose = (2, 0, 5, 3, 0, 0, 0, 0, 0, 0)

    base.familyname = fontName
    base.fontname = f'{fontName}-{i.weight}'
    base.fullname = f'{fontName}-{i.weight}'
    base.fondname = f'{fontName}-{i.weight}'
    # print(base.sfnt_names)
    base.sfnt_names=(
            ('English (US)', 'Fullname', f'{fontName}-{i.weight}'),
            ('English (US)', 'UniqueID', f':{fontName}-{i.weight}:2022'),
            )
    # base.weight = i.weight
    base.generate(f'{fontName}-{i.weight}.ttf')
    return f'{fontName}-{i.weight}.ttf'


future_list = []
with futures.ThreadPoolExecutor(max_workers=len(todoList)) as executor:
    for i in todoList:
        future = executor.submit(font_merger, i=i)
        future_list.append(future)
    _ = futures.as_completed(fs=future_list)

print(f'completed. {future_list}')
