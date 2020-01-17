#----------------------------------------
#	 Make variables
#----------------------------------------

BUILD_DIR = build


#----------------------------------------
#	 Make Rules
#----------------------------------------

.PHONY: clean generate setup test
all: setup
	make -f build.mk all

test: setup
	make -f build.mk test

generate: setup
	make -f build.mk generate

clean: setup
	make -f build.mk clean

setup: $(BUILD_DIR)/conanbuildinfo.mak

build/conanbuildinfo.mak: conanfile.txt
	rm -vfr $(BUILD_DIR) && \
	mkdir $(BUILD_DIR) && \
	conan install -if $(BUILD_DIR) .
