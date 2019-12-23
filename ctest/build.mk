include build/conanbuildinfo.mak

#----------------------------------------
#	 Make variables for a sample App
#----------------------------------------

CXX_SRCS = \
	test.cpp \
	stub.c \
	out/arm_mcdecoder.c \
	out/riscv_mcdecoder.c

CXX_OBJ_FILES = \
	build/test.o \
	build/stub.o \
	build/arm_mcdecoder.o \
	build/riscv_mcdecoder.o

EXE_FILENAME = \
	build/test


#----------------------------------------
#	 Prepare flags from variables
#----------------------------------------

CFLAGS += $(CONAN_CFLAGS)
CXXFLAGS += $(CONAN_CXXFLAGS)
CPPFLAGS += $(addprefix -I, $(CONAN_INCLUDE_DIRS))
CPPFLAGS += $(addprefix -D, $(CONAN_DEFINES))
CPPFLAGS += -D_GLIBCXX_USE_CXX11_ABI=0
LDFLAGS += $(addprefix -L, $(CONAN_LIB_DIRS))
LDLIBS += $(addprefix -l, $(CONAN_LIBS))


#----------------------------------------
#	 Make Commands
#----------------------------------------

COMPILE_CXX_COMMAND ?= \
	g++ -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

COMPILE_C_COMMAND ?= \
	gcc -c $(CFLAGS) $< -o $@

CREATE_EXE_COMMAND ?= \
	g++ $(CXX_OBJ_FILES) \
	$(CXXFLAGS) $(LDFLAGS) $(LDLIBS) \
	-o $(EXE_FILENAME)


#----------------------------------------
#	 Make Rules
#----------------------------------------

.PHONY: all clean exe test

all: exe

exe: $(EXE_FILENAME)

clean:
	rm -vf $(EXE_FILENAME) $(CXX_OBJ_FILES)

test: exe
	$(EXE_FILENAME)

$(EXE_FILENAME) : $(CXX_OBJ_FILES)
	$(CREATE_EXE_COMMAND)

build/%.o: %.cpp
	$(COMPILE_CXX_COMMAND)

build/%.o: %.c
	$(COMPILE_C_COMMAND)

build/%.o: out/%.c
	$(COMPILE_C_COMMAND)
