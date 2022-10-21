all: NimbUDMono/NimbUDMono-Regular.ttf NimbUDMono75/NimbUDMono75-Regular.ttf NimbUDRoman/NimbUDRoman-Regular.ttf NimbUDSans/NimbUDSans-Regular.ttf

NimbUDMono/NimbUDMono-Regular.ttf: NimbUDMono/genNimbUDMono.py

NimbUDMono75/NimbUDMono75-Regular.ttf: NimbUDMono75/genNimbUDMono75.py

NimbUDRoman/NimbUDRoman-Regular.ttf: NimbUDRoman/genNimbUDRoman.py

NimbUDSans/NimbUDSans-Regular.ttf: NimbUDSans/genNimbUDSans.py

%-Regular.ttf: srcfonts/urw-core35-fonts/NimbusRoman-Regular.otf srcfonts/morisawa-biz-ud-gothic/fonts/ttf/BIZUDGothic-Regular.ttf srcfonts/morisawa-biz-ud-mincho/fonts/ttf/BIZUDPMincho-Regular.ttf
	cd $(@D) && python3 gen$(*F).py


srcfonts/urw-core35-fonts/NimbusRoman-Regular.otf:
	git submodule update --init --depth 1 --remote  --merge --jobs 4

srcfonts/morisawa-biz-ud-gothic/fonts/ttf/BIZUDGothic-Regular.ttf:
	git submodule update --init --depth 1 --remote  --merge --jobs 4

srcfonts/morisawa-biz-ud-mincho/fonts/ttf/BIZUDPMincho-Regular.ttf:
	git submodule update --init --depth 1 --remote  --merge --jobs 4
