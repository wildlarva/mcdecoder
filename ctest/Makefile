#----------------------------------------
#	 Make Rules
#----------------------------------------

.PHONY: clean generate setup test
all: setup generate
	make -f build.mk all

test: all
	make -f build.mk test

generate: out/arm_mcparser.c out/arm_mcparser.h out/riscv_mcparser.c out/riscv_mcparser.h

clean: setup
	rm -vfr out
	make -f build.mk clean

setup: build/conanbuildinfo.mak

build/conanbuildinfo.mak: conanfile.txt
	rm -vfr build && \
	mkdir build && \
	conan install -if build .

out/arm_mcparser.c out/arm_mcparser.h: ../test/arm.yaml
	python3.8 -m mcparser_gen $<

out/riscv_mcparser.c out/riscv_mcparser.h: ../test/riscv.yaml
	python3.8 -m mcparser_gen $<
