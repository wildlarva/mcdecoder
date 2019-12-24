#----------------------------------------
#	 Make Rules
#----------------------------------------

.PHONY: clean generate setup test
all: setup generate
	make -f build.mk all

test: all
	make -f build.mk test

generate: out/arm_mcdecoder.c out/arm_mcdecoder.h out/riscv_mcdecoder.c out/riscv_mcdecoder.h

clean: setup
	rm -vfr out
	make -f build.mk clean

setup: build/conanbuildinfo.mak

build/conanbuildinfo.mak: conanfile.txt
	rm -vfr build && \
	mkdir build && \
	conan install -if build .

out/arm_mcdecoder.c out/arm_mcdecoder.h: ../test/arm.yaml
	python3.8 -m mcdecoder generate $<

out/riscv_mcdecoder.c out/riscv_mcdecoder.h: ../test/riscv.yaml
	python3.8 -m mcdecoder generate $<
