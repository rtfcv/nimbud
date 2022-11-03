import fontforge as ff

from concurrent import futures

scaleEm = "1000"

fontName = "GoUDMono"


class FINFO:
    def __init__(self, weight: str, baseFont: str, secondFont: str) -> None:
        self.weight = weight
        self.baseFont = baseFont
        self.secondFont = secondFont
        self.ttfweight = weight
        if weight=='BoldItalic':
            self.ttfweight='Bold Italic'


panoseWeight = dict(Regular=5,Italic=5, Bold=8, BoldItalic=8)


todoList = [
    FINFO(
        'Regular',
        "../srcfonts/image/font/gofont/ttfs/Go-Mono.ttf",
        "../srcfonts/morisawa-biz-ud-mincho/fonts/ttf/BIZUDMincho-Regular.ttf"
    ),
    FINFO(
        'Bold',
        "../srcfonts/image/font/gofont/ttfs/Go-Mono-Bold.ttf",
        "../srcfonts/morisawa-biz-ud-gothic/fonts/ttf/BIZUDGothic-Bold.ttf"
    ),
    FINFO(
        'Italic',
        "../srcfonts/image/font/gofont/ttfs/Go-Mono-Italic.ttf",
        "../srcfonts/morisawa-biz-ud-gothic/fonts/ttf/BIZUDGothic-Regular.ttf"
    ),
    FINFO(
        'BoldItalic',
        "../srcfonts/image/font/gofont/ttfs/Go-Mono-Bold-Italic.ttf",
        "../srcfonts/morisawa-biz-ud-gothic/fonts/ttf/BIZUDGothic-Bold.ttf"
    ),

]


def cpOS2(src, dest):
    dest.os2_codepages = src.os2_codepages
    # dest.os2_family_class = src.os2_family_class
    dest.os2_fstype = src.os2_fstype
    # dest.os2_stylemap = src.os2_stylemap # Regular Bold etc.
    dest.os2_panose = src.os2_panose
    dest.os2_strikeypos = src.os2_strikeypos
    dest.os2_strikeysize = src.os2_strikeysize
    # dest.os2_subxoff = src.os2_subxoff
    # dest.os2_subxsize = src.os2_subxsize
    # dest.os2_subyoff = src.os2_subyoff
    # dest.os2_subysize = src.os2_subysize
    # dest.os2_supxoff = src.os2_supxoff
    # dest.os2_supxsize = src.os2_supxsize
    # dest.os2_supyoff = src.os2_supyoff
    # dest.os2_supysize = src.os2_supysize
    # dest.os2_typoascent = src.os2_typoascent
    # dest.os2_typoascent_add = src.os2_typoascent_add
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
    # dest.hhea_ascent = src.hhea_ascent
    # dest.hhea_ascent_add = src.hhea_ascent_add
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
    basewid = base['A'].width

    # base.em = int(base.em * altwid/basewid)+1
    # changing em of base font break everything for some reason
    alt.em = int(alt.em * basewid/altwid)
    base.design_size = alt.design_size
    altwid = alt['A'].width

    print(f'base font changed to: {base["A"].width}x{base["A"].vwidth}')
    print(f'alt font is: {alt["A"].width}x{alt["A"].vwidth}')
    print(f'em for base changed to: {base.em}')
    basewid = base['A'].width

    base.selection.all()
    # base.nltransform(f'x*{altwid}/{basewid}', 'y')
    # base.transform((altwid/basewid,0, 0, 1, 0, 0))

    for key in base:
        # if key in bkey: continue
        base[key].autoHint()

    ## resize everything
    # for g in base:
    #     if base[g].isWorthOutputting():
    #         __origwid = base[g].width
    #         base[g].width = int(__origwid/basewid*altwid)

    print(f'base font changed to: {base["A"].width}x{base["A"].vwidth}')

    # merge fonts
    base.mergeFonts(alt)

    # remove ligatures
    # print(base['ff'].glyphclass)
    # list(map(base.removeGlyph, ('fi','ff','fl','ffi','ffl')))

    # fix metadata
    base = cpOS2(src=alt, dest=base)
    base.os2_version = 2 # setting this higher invokes bug in fontforge
    base.os2_family_class = 2057  # SS Typewriter Gothic
    base.os2_panose = (
        2,  # Latin: Text and Display
        11, # Nomal Sans
        panoseWeight[i.weight],
        9,  # Monospaced
        0,  # None
        0,  # No Variation
        0,  # Straight Arms/Wedge
        0,
        0,  # Standard/Trimmed
        0,  # Ducking/Large
    )

    base.familyname = fontName
    base.fontname = f'{fontName}-{i.weight}'
    base.fullname = f'{fontName} {i.ttfweight}'
    base.fondname = f'{fontName} {i.ttfweight}'
    print(base.sfnt_names)
    base.sfnt_names=(
            ('English (US)', 'Fullname', f'{fontName} {i.ttfweight}'),
            ('English (US)', 'Family', f'{fontName}'),
            ('English (US)', 'SubFamily', f'{i.ttfweight}'),
            ('English (US)', 'UniqueID', f':{fontName}-{i.weight}:2022'),
            )
    # base.weight = i.weight
    base.generate(f'{fontName}-{i.weight}.ttf')
    return f'{fontName}-{i.weight}.ttf'

# font_merger(todoList[0])

future_list = []
with futures.ThreadPoolExecutor(max_workers=len(todoList)) as executor:
    for i in todoList:
        future = executor.submit(font_merger, i=i)
        future_list.append(future)
    _ = futures.as_completed(fs=future_list)

print(f'completed. {future_list}')
