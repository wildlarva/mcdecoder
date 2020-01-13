#----------------------------------------
#	 Make Rules
#----------------------------------------

.PHONY: clean generate setup test
all: setup generate
	make -f build.mk all

test: all
	make -f build.mk test

generate: out/arm_mcdecoder.c out/at_mcdecoder.c out/riscv_mcdecoder.c out/pc_mcdecoder.c out/cc_mcdecoder.c

clean: setup
	rm -vfr out
	make -f build.mk clean

setup: build/conanbuildinfo.mak

build/conanbuildinfo.mak: conanfile.txt
	rm -vfr build && \
	mkdir build && \
	conan install -if build .

out/arm_mcdecoder.c: ../test/arm.yaml
	mcdecoder generate --output out $<

out/at_mcdecoder.c: ../test/arm_thumb.yaml
	mcdecoder generate --output out $<

out/riscv_mcdecoder.c: ../test/riscv.yaml
	mcdecoder generate --output out $<

out/pc_mcdecoder.c: ../test/primitive_condition.yaml
	mcdecoder generate --output out $<

out/cc_mcdecoder.c: ../test/complex_condition.yaml
	mcdecoder generate --output out $<
