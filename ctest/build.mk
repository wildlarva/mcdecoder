BUILD_DIR = build

include $(BUILD_DIR)/conanbuildinfo.mak

#----------------------------------------
#	 Make variables
#----------------------------------------

COMMON_TEST_DIR = ../test

DECODER_DIR = out

DECODER_SRCS = \
	$(DECODER_DIR)/arm_mcdecoder.c \
	$(DECODER_DIR)/ab_mcdecoder.c \
	$(DECODER_DIR)/at_mcdecoder.c \
	$(DECODER_DIR)/atb_mcdecoder.c \
	$(DECODER_DIR)/riscv_mcdecoder.c \
	$(DECODER_DIR)/pc_mcdecoder.c \
	$(DECODER_DIR)/cc_mcdecoder.c \
	$(DECODER_DIR)/dt16x2_mcdecoder.c\
	$(DECODER_DIR)/dt32x1_mcdecoder.c

CSRCS = \
	stub.c

CSRCS += $(DECODER_SRCS)

CPP_SRCS = \
	test.cpp

CXX_OBJ_FILES = \
	$(patsubst %.c, $(BUILD_DIR)/%.o, $(notdir $(CSRCS))) \
	$(patsubst %.cpp, $(BUILD_DIR)/%.o, $(notdir $(CPP_SRCS)))

EXE_FILENAME = \
	$(BUILD_DIR)/test


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

COMPILE_CXX_COMMAND = \
	g++ -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

COMPILE_C_COMMAND = \
	gcc -c $(CFLAGS) $< -o $@

CREATE_EXE_COMMAND = \
	g++ $(CXX_OBJ_FILES) \
	$(CXXFLAGS) $(LDFLAGS) $(LDLIBS) \
	-o $(EXE_FILENAME)

CREATE_DECODER_COMMAND = \
	mcdecoder generate --output $(DECODER_DIR) $<


#----------------------------------------
#	 Make Rules
#----------------------------------------

.PHONY: all clean exe generate test

all: exe

generate: $(DECODER_SRCS)

exe: generate $(EXE_FILENAME)

clean:
	rm -vf $(EXE_FILENAME) $(CXX_OBJ_FILES)
	rm -vfr $(DECODER_DIR)

test: exe
	$(EXE_FILENAME)

$(EXE_FILENAME) : $(CXX_OBJ_FILES)
	$(CREATE_EXE_COMMAND)

$(BUILD_DIR)/%.o: %.cpp
	$(COMPILE_CXX_COMMAND)

$(BUILD_DIR)/%.o: %.c
	$(COMPILE_C_COMMAND)

$(BUILD_DIR)/%.o: $(DECODER_DIR)/%.c
	$(COMPILE_C_COMMAND)

$(DECODER_DIR)/arm_mcdecoder.c: $(COMMON_TEST_DIR)/arm.yaml
	$(CREATE_DECODER_COMMAND)

$(DECODER_DIR)/ab_mcdecoder.c: $(COMMON_TEST_DIR)/arm_big.yaml
	$(CREATE_DECODER_COMMAND)

$(DECODER_DIR)/at_mcdecoder.c: $(COMMON_TEST_DIR)/arm_thumb.yaml
	$(CREATE_DECODER_COMMAND)

$(DECODER_DIR)/atb_mcdecoder.c: $(COMMON_TEST_DIR)/arm_thumb_big.yaml
	$(CREATE_DECODER_COMMAND)

$(DECODER_DIR)/riscv_mcdecoder.c: $(COMMON_TEST_DIR)/riscv.yaml
	$(CREATE_DECODER_COMMAND)

$(DECODER_DIR)/pc_mcdecoder.c: $(COMMON_TEST_DIR)/primitive_condition.yaml
	$(CREATE_DECODER_COMMAND)

$(DECODER_DIR)/cc_mcdecoder.c: $(COMMON_TEST_DIR)/complex_condition.yaml
	$(CREATE_DECODER_COMMAND)

$(DECODER_DIR)/dt16x2_mcdecoder.c: $(COMMON_TEST_DIR)/decision_tree_code16x2.yaml
	$(CREATE_DECODER_COMMAND)

$(DECODER_DIR)/dt32x1_mcdecoder.c: $(COMMON_TEST_DIR)/decision_tree_code32x1.yaml
	$(CREATE_DECODER_COMMAND)
