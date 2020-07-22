BUILD_DIR = build

include $(BUILD_DIR)/conanbuildinfo.mak

#----------------------------------------
#	 Make variables
#----------------------------------------

COMMON_TEST_DIR = ../common
SRC_TEMPLATE_DIR = ../../src/mcdecoder/templates
TEST_TEMPLATE_DIR = templates
STEPS_DIR = features/step_definitions
DECODER_DIR = out

ATHRILL_DECODER_DIR = $(DECODER_DIR)/athrill
ATHRILL_BUILD_DIR = $(BUILD_DIR)/athrill

MCDECODER_DECODER_DIR = $(DECODER_DIR)/mcdecoder
MCDECODER_BUILD_DIR = $(BUILD_DIR)/mcdecoder

# <decoder name>:<MC description file name>
DECODERS = \
	arm:arm \
	ab:arm_big \
	at:arm_thumb \
	atb:arm_thumb_big \
	riscv:riscv \
	pc:primitive_condition \
	cc:complex_condition \
	dt16x2:decision_tree_code16x2 \
	dt32x1:decision_tree_code32x1

COMMON_CXX_SRCS = \
	mcdhelper.cc \
	$(STEPS_DIR)/mcdecoder_steps.cc

COMMON_CXX_INCLUDES = \
	.

COMMON_CXX_OBJ_FILES = $(patsubst %.cc, $(BUILD_DIR)/%.o, $(notdir $(COMMON_CXX_SRCS)))

ATHRILL_DECODER_SRCS = \
	$(foreach element, $(DECODERS), $(ATHRILL_DECODER_DIR)/$(strip $(firstword $(subst :, , $(element))))_mcdecoder.c)

ATHRILL_HELPER_SRCS = \
	$(foreach element, $(DECODERS), $(ATHRILL_DECODER_DIR)/$(strip $(firstword $(subst :, , $(element))))_mcdhelper.cc)

ATHRILL_CSRCS = $(ATHRILL_DECODER_SRCS)

ATHRILL_CINCLUDES = \
	$(ATHRILL_DECODER_DIR)

ATHRILL_COBJ_FILES = $(patsubst %.c, $(ATHRILL_BUILD_DIR)/%.o, $(notdir $(ATHRILL_CSRCS)))

ATHRILL_CXX_SRCS = \
	athrill_setup.cc

ATHRILL_CXX_SRCS += $(ATHRILL_HELPER_SRCS)

ATHRILL_CXX_INCLUDES = \
	$(ATHRILL_DECODER_DIR)

ATHRILL_CXX_INCLUDES += $(COMMON_CXX_INCLUDES)

ATHRILL_CXX_OBJ_FILES = $(patsubst %.cc, $(ATHRILL_BUILD_DIR)/%.o, $(notdir $(ATHRILL_CXX_SRCS)))
ATHRILL_EXE_FILENAME = $(ATHRILL_BUILD_DIR)/test

MCDECODER_DECODER_SRCS = \
	$(foreach element, $(DECODERS), $(MCDECODER_DECODER_DIR)/$(strip $(firstword $(subst :, , $(element))))_mcdecoder.c)

MCDECODER_HELPER_SRCS = \
	$(foreach element, $(DECODERS), $(MCDECODER_DECODER_DIR)/$(strip $(firstword $(subst :, , $(element))))_mcdhelper.cc)

MCDECODER_CSRCS = $(MCDECODER_DECODER_SRCS)

MCDECODER_CINCLUDES = \
	$(MCDECODER_DECODER_DIR)

MCDECODER_COBJ_FILES = $(patsubst %.c, $(MCDECODER_BUILD_DIR)/%.o, $(notdir $(MCDECODER_CSRCS)))

MCDECODER_CXX_SRCS = \
	mcdecoder_setup.cc

MCDECODER_CXX_SRCS += $(MCDECODER_HELPER_SRCS)

MCDECODER_CXX_INCLUDES = \
	$(MCDECODER_DECODER_DIR)

MCDECODER_CXX_INCLUDES += $(COMMON_CXX_INCLUDES)

MCDECODER_CXX_OBJ_FILES = $(patsubst %.cc, $(MCDECODER_BUILD_DIR)/%.o, $(notdir $(MCDECODER_CXX_SRCS)))
MCDECODER_EXE_FILENAME = $(MCDECODER_BUILD_DIR)/test


#----------------------------------------
#	 Prepare flags from variables
#----------------------------------------

COMMON_CFLAGS = \
	$(CONAN_CFLAGS) \
	$(addprefix -I, $(CONAN_INCLUDE_DIRS)) \
	$(addprefix -D, $(CONAN_DEFINES)) \

COMMON_CXXFLAGS = -D_GLIBCXX_USE_CXX11_ABI=0
COMMON_CXXFLAGS += \
	$(CONAN_CXXFLAGS) \
	$(addprefix -I, $(CONAN_INCLUDE_DIRS)) \
	$(addprefix -D, $(CONAN_DEFINES)) \
	$(addprefix -I, $(COMMON_CXX_INCLUDES))

COMMON_LDFLAGS = $(addprefix -L, $(CONAN_LIB_DIRS))
COMMON_LDLIBS = $(addprefix -l, $(CONAN_LIBS))

ATHRILL_CFLAGS = \
	$(COMMON_CFLAGS) \
	$(addprefix -I, $(ATHRILL_CINCLUDES))

ATHRILL_CXXFLAGS = \
	$(COMMON_CXXFLAGS) \
	$(addprefix -I, $(ATHRILL_CXX_INCLUDES))

ATHRILL_LDFLAGS = $(COMMON_LDFLAGS)
ATHRILL_LDLIBS = $(COMMON_LDLIBS)

MCDECODER_CFLAGS = \
	$(COMMON_CFLAGS) \
	$(addprefix -I, $(MCDECODER_CINCLUDES))

MCDECODER_CXXFLAGS = \
	$(COMMON_CXXFLAGS) \
	$(addprefix -I, $(MCDECODER_CXX_INCLUDES))

MCDECODER_LDFLAGS = $(COMMON_LDFLAGS)
MCDECODER_LDLIBS = $(COMMON_LDLIBS)


#----------------------------------------
#	 Make Commands
#----------------------------------------

COMMON_COMPILE_C_COMMAND = \
	gcc -c $(COMMON_CFLAGS) $< -o $@

COMMON_COMPILE_CXX_COMMAND = \
	g++ -c $(COMMON_CXXFLAGS) $< -o $@

ATHRILL_COMPILE_C_COMMAND = \
	gcc -c $(ATHRILL_CFLAGS) $< -o $@

ATHRILL_COMPILE_CXX_COMMAND = \
	g++ -c $(ATHRILL_CXXFLAGS) $< -o $@

MCDECODER_COMPILE_C_COMMAND = \
	gcc -c $(MCDECODER_CFLAGS) $< -o $@

MCDECODER_COMPILE_CXX_COMMAND = \
	g++ -c $(MCDECODER_CXXFLAGS) $< -o $@


#----------------------------------------
#	 Make Rules
#----------------------------------------

.PHONY: all clean exe generate test

all: exe

generate: $(ATHRILL_DECODER_SRCS) $(MCDECODER_DECODER_SRCS)

exe: generate $(ATHRILL_EXE_FILENAME) $(MCDECODER_EXE_FILENAME)

clean:
	rm -vf $(COMMON_COBJ_FILES) $(COMMON_CXX_OBJ_FILES)
	rm -vfr $(ATHRILL_BUILD_DIR)
	rm -vfr $(MCDECODER_BUILD_DIR)
	rm -vfr $(DECODER_DIR)

test: exe
	$(ATHRILL_EXE_FILENAME) & bundle exec cucumber
	$(MCDECODER_EXE_FILENAME) & bundle exec cucumber

$(BUILD_DIR)/%.o: %.c
	$(COMMON_COMPILE_C_COMMAND)

$(BUILD_DIR)/%.o: %.cc
	$(COMMON_COMPILE_CXX_COMMAND)

$(BUILD_DIR)/%.o: $(STEPS_DIR)/%.cc
	$(COMMON_COMPILE_CXX_COMMAND)

$(ATHRILL_EXE_FILENAME) : $(ATHRILL_BUILD_DIR) $(COMMON_COBJ_FILES) $(COMMON_CXX_OBJ_FILES) $(ATHRILL_COBJ_FILES) $(ATHRILL_CXX_OBJ_FILES)
	g++ $(COMMON_COBJ_FILES) $(COMMON_CXX_OBJ_FILES) $(ATHRILL_COBJ_FILES) $(ATHRILL_CXX_OBJ_FILES) \
	$(ATHRILL_CXXFLAGS) $(ATHRILL_LDFLAGS) $(ATHRILL_LDLIBS) -o $(ATHRILL_EXE_FILENAME)

$(ATHRILL_BUILD_DIR):
	mkdir -p $(ATHRILL_BUILD_DIR)

$(ATHRILL_BUILD_DIR)/%.o: %.c
	$(ATHRILL_COMPILE_C_COMMAND)

$(ATHRILL_BUILD_DIR)/%.o: %.cc
	$(ATHRILL_COMPILE_CXX_COMMAND)

$(ATHRILL_BUILD_DIR)/%.o: $(ATHRILL_DECODER_DIR)/%.c
	$(ATHRILL_COMPILE_C_COMMAND)

$(ATHRILL_BUILD_DIR)/%.o: $(ATHRILL_DECODER_DIR)/%.cc
	$(ATHRILL_COMPILE_CXX_COMMAND)

$(MCDECODER_EXE_FILENAME) : $(MCDECODER_BUILD_DIR) $(COMMON_COBJ_FILES) $(COMMON_CXX_OBJ_FILES) $(MCDECODER_COBJ_FILES) $(MCDECODER_CXX_OBJ_FILES)
	g++ $(COMMON_COBJ_FILES) $(COMMON_CXX_OBJ_FILES) $(MCDECODER_COBJ_FILES) $(MCDECODER_CXX_OBJ_FILES) \
	$(MCDECODER_CXXFLAGS) $(MCDECODER_LDFLAGS) $(MCDECODER_LDLIBS) -o $(MCDECODER_EXE_FILENAME)

$(MCDECODER_BUILD_DIR):
	mkdir -p $(MCDECODER_BUILD_DIR)

$(MCDECODER_BUILD_DIR)/%.o: %.c
	$(MCDECODER_COMPILE_C_COMMAND)

$(MCDECODER_BUILD_DIR)/%.o: %.cc
	$(MCDECODER_COMPILE_CXX_COMMAND)

$(MCDECODER_BUILD_DIR)/%.o: $(MCDECODER_DECODER_DIR)/%.c
	$(MCDECODER_COMPILE_C_COMMAND)

$(MCDECODER_BUILD_DIR)/%.o: $(MCDECODER_DECODER_DIR)/%.cc
	$(MCDECODER_COMPILE_CXX_COMMAND)

define athrill-decoder-target
$(ATHRILL_DECODER_DIR)/$1_mcdecoder.c $(ATHRILL_DECODER_DIR)/$1_mcdhelper.cc: $(COMMON_TEST_DIR)/$2.yaml
	mcdecoder generate --type athrill --output $(ATHRILL_DECODER_DIR) $(COMMON_TEST_DIR)/$2.yaml
	mcdecoder generate --template $(TEST_TEMPLATE_DIR)/athrill_helper --output $(ATHRILL_DECODER_DIR) $(COMMON_TEST_DIR)/$2.yaml

endef

$(foreach element, $(DECODERS), $(eval \
	$(call athrill-decoder-target,$(strip $(firstword $(subst :, , $(element)))),$(strip $(word 2, $(subst :, , $(element))))) \
	))

define mcdecoder-decoder-target
$(MCDECODER_DECODER_DIR)/$1_mcdecoder.c $(MCDECODER_DECODER_DIR)/$1_mcdhelper.cc: $(COMMON_TEST_DIR)/$2.yaml
	mcdecoder generate --output $(MCDECODER_DECODER_DIR) $(COMMON_TEST_DIR)/$2.yaml
	mcdecoder generate --template $(TEST_TEMPLATE_DIR)/mcdecoder_helper --output $(MCDECODER_DECODER_DIR) $(COMMON_TEST_DIR)/$2.yaml

endef

$(foreach element, $(DECODERS), $(eval \
	$(call mcdecoder-decoder-target,$(strip $(firstword $(subst :, , $(element)))),$(strip $(word 2, $(subst :, , $(element))))) \
	))
