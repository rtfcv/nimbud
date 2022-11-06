all: fonts nerdfonts

fonts:\
	fonts/NimbUDMono-Regular.ttf fonts/NimbUDMono75-Regular.ttf\
	fonts/NimbUDRoman-Regular.ttf fonts/NimbUDSans-Regular.ttf\
	fonts/NimbUDRomanHint-Regular.ttf\
	fonts/GoUDMono-Regular.ttf fonts/GoUDMono75-Regular.ttf 

nerdfonts: fonts\
	nerdfonts/Nimb\ UDMono\ Nerd\ Font\ Complete.ttf\
	nerdfonts/Nimb\ UDMono75\ Nerd\ Font\ Complete.ttf\
	nerdfonts/Go\ UDMono\ Nerd\ Font\ Complete.ttf\
	nerdfonts/Go\ UDMono75\ Nerd\ Font\ Complete.ttf

.PHONY: install
install: fonts nerdfonts
	mkdir -p ~/.local/share/fonts/numbudFonts
	cp -r fonts ~/.local/share/fonts/numbudFonts/
	cp -r nerdfonts ~/.local/share/fonts/numbudFonts/

# specify fonts # do we need specific one of these
NimbUDMono/NimbUDMono-Regular.ttf: NimbUDMono/genNimbUDMono.py

NimbUDMono75/NimbUDMono75-Regular.ttf: NimbUDMono75/genNimbUDMono75.py

NimbUDRoman/NimbUDRoman-Regular.ttf: NimbUDRoman/genNimbUDRoman.py

NimbUDRomanHint/NimbUDRomanHint-Regular.ttf: NimbUDRomanHint/genNimbUDRomanHint.py

NimbUDSans/NimbUDSans-Regular.ttf: NimbUDSans/genNimbUDSans.py

GoUDMono/GoUDMono-Regular.ttf: GoUDMono/genGoUDMono.py

GoUDMono75/GoUDMono75-Regular.ttf: GoUDMono75/genGoUDMono75.py


# remote sources
srcfonts/urw-core35-fonts/NimbusRoman-Regular.otf:
	git submodule update --init --depth 1 --remote  --merge --jobs 4

srcfonts/%.ttf:
	git submodule update --init --depth 1 --remote  --merge --jobs 4

patcher/font-patcher:
	mkdir -p patcher
	cd patcher && rm -rf ./* && wget https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FontPatcher.zip && unzip FontPatcher.zip


# copy fonts
fonts/%-Regular.ttf: %/%-Regular.ttf
	cp $(*F)/$(*F)-Regular.ttf fonts/
	cp $(*F)/$(*F)-Bold.ttf fonts/
	cp $(*F)/$(*F)-BoldItalic.ttf fonts/
	cp $(*F)/$(*F)-Italic.ttf fonts/


# build fonts
%/%-Regular.ttf: \
	srcfonts/urw-core35-fonts/NimbusRoman-Regular.otf\
	srcfonts/morisawa-biz-ud-gothic/fonts/ttf/BIZUDGothic-Regular.ttf\
	srcfonts/morisawa-biz-ud-mincho/fonts/ttf/BIZUDPMincho-Regular.ttf
	cd $(@D) && python3 gen$(*F).py


# patch fonts
nerdfonts/Nimb\ UDMono\ Nerd\ Font\ Complete.ttf: patcher/font-patcher fonts/NimbUDMono-Regular.ttf
	ls fonts/* | grep 'NimbUDMono-[a-zA-Z]*.ttf' | xargs -P10 -n1 fontforge patcher/font-patcher --complete --makegroups --outputdir nerdfonts

nerdfonts/Nimb\ UDMono75\ Nerd\ Font\ Complete.ttf: patcher/font-patcher fonts/NimbUDMono75-Regular.ttf
	ls fonts/* | grep 'NimbUDMono75-[a-zA-Z]*.ttf' | xargs -P10 -n1 fontforge patcher/font-patcher --complete --makegroups --outputdir nerdfonts

nerdfonts/Go\ UDMono\ Nerd\ Font\ Complete.ttf: patcher/font-patcher fonts/GoUDMono-Regular.ttf
	ls fonts/* | grep 'GoUDMono-[a-zA-Z]*.ttf' | xargs -P10 -n1 fontforge patcher/font-patcher --complete --makegroups --outputdir nerdfonts

nerdfonts/Go\ UDMono75\ Nerd\ Font\ Complete.ttf: patcher/font-patcher fonts/GoUDMono75-Regular.ttf
	ls fonts/* | grep 'GoUDMono75-[a-zA-Z]*.ttf' | xargs -P10 -n1 fontforge patcher/font-patcher --complete --makegroups --outputdir nerdfonts
