NAME=vgg_owl
byte: $(NAME).ml jbuild
	jbuilder build $(NAME).bc
	cp _build/default/$(NAME).bc .

native: $(NAME).ml jbuild
	jbuilder build $(NAME).exe
	cp _build/default/$(NAME).exe .

js: $(NAME).ml jbuild
	jbuilder build $(NAME).js
	cp _build/default/$(NAME).js .

clean:
	rm -rf _build