BUILD_DIR = build

include $(BUILD_DIR)/conanbuildinfo.mak

#----------------------------------------
#	 Make variables
#----------------------------------------

COMMON_TEST_DIR = ../test
TEMPLATE_DIR = templates
STEPS_DIR = features/step_definitions
DECODER_DIR = out
ATHRILL_DECODER_DIR = $(DECODER_DIR)/athrill
ATHRILL_BUILD_DIR = $(BUILD_DIR)/athrill

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
	mcdhelper.cpp \
	$(STEPS_DIR)/mcdecoder_steps.cpp

COMMON_CXX_INCLUDES = \
	.

COMMON_CXX_OBJ_FILES = $(patsubst %.cpp, $(BUILD_DIR)/%.o, $(notdir $(COMMON_CXX_SRCS)))

ATHRILL_DECODER_SRCS = \
	$(foreach element, $(DECODERS), $(ATHRILL_DECODER_DIR)/$(strip $(firstword $(subst :, , $(element))))_mcdecoder.c)

ATHRILL_HELPER_SRCS = \
	$(foreach element, $(DECODERS), $(ATHRILL_DECODER_DIR)/$(strip $(firstword $(subst :, , $(element))))_mcdhelper.cpp)

ATHRILL_CSRCS = \
	stub.c

ATHRILL_CSRCS += $(ATHRILL_DECODER_SRCS)

ATHRILL_CINCLUDES = \
	$(ATHRILL_DECODER_DIR)

ATHRILL_COBJ_FILES = $(patsubst %.c, $(ATHRILL_BUILD_DIR)/%.o, $(notdir $(ATHRILL_CSRCS)))

ATHRILL_CXX_SRCS = \
	athrill_setup.cpp

ATHRILL_CXX_SRCS += $(ATHRILL_HELPER_SRCS)

ATHRILL_CXX_INCLUDES = \
	$(ATHRILL_DECODER_DIR)

ATHRILL_CXX_INCLUDES += $(COMMON_CXX_INCLUDES)

ATHRILL_CXX_OBJ_FILES = $(patsubst %.cpp, $(ATHRILL_BUILD_DIR)/%.o, $(notdir $(ATHRILL_CXX_SRCS)))
ATHRILL_EXE_FILENAME = $(ATHRILL_BUILD_DIR)/test


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


#----------------------------------------
#	 Make Rules
#----------------------------------------

.PHONY: all clean exe generate test

all: exe

generate: $(ATHRILL_DECODER_SRCS)

exe: generate $(ATHRILL_EXE_FILENAME)

clean:
	rm -vf $(COMMON_COBJ_FILES) $(COMMON_CXX_OBJ_FILES)
	rm -vfr $(ATHRILL_BUILD_DIR)
	rm -vfr $(DECODER_DIR)

test: exe
	$(ATHRILL_EXE_FILENAME) & bundle exec cucumber

$(ATHRILL_EXE_FILENAME) : $(ATHRILL_BUILD_DIR) $(COMMON_COBJ_FILES) $(COMMON_CXX_OBJ_FILES) $(ATHRILL_COBJ_FILES) $(ATHRILL_CXX_OBJ_FILES)
	g++ $(COMMON_COBJ_FILES) $(COMMON_CXX_OBJ_FILES) $(ATHRILL_COBJ_FILES) $(ATHRILL_CXX_OBJ_FILES) \
	$(ATHRILL_CXXFLAGS) $(ATHRILL_LDFLAGS) $(ATHRILL_LDLIBS) -o $(ATHRILL_EXE_FILENAME)

$(ATHRILL_BUILD_DIR):
	mkdir -p $(ATHRILL_BUILD_DIR)

$(BUILD_DIR)/%.o: %.c
	$(COMMON_COMPILE_C_COMMAND)

$(BUILD_DIR)/%.o: %.cpp
	$(COMMON_COMPILE_CXX_COMMAND)

$(BUILD_DIR)/%.o: $(STEPS_DIR)/%.cpp
	$(COMMON_COMPILE_CXX_COMMAND)

$(ATHRILL_BUILD_DIR)/%.o: %.c
	$(ATHRILL_COMPILE_C_COMMAND)

$(ATHRILL_BUILD_DIR)/%.o: %.cpp
	$(ATHRILL_COMPILE_CXX_COMMAND)

$(ATHRILL_BUILD_DIR)/%.o: $(ATHRILL_DECODER_DIR)/%.c
	$(ATHRILL_COMPILE_C_COMMAND)

$(ATHRILL_BUILD_DIR)/%.o: $(ATHRILL_DECODER_DIR)/%.cpp
	$(ATHRILL_COMPILE_CXX_COMMAND)

define athrill-decoder-target
$(ATHRILL_DECODER_DIR)/$1_mcdecoder.c $(ATHRILL_DECODER_DIR)/$1_mcdhelper.cpp: $(COMMON_TEST_DIR)/$2.yaml
	mcdecoder generate --output $(ATHRILL_DECODER_DIR) $(COMMON_TEST_DIR)/$2.yaml; \
	mcdecoder generate --template $(TEMPLATE_DIR)/athrill_helper --output $(ATHRILL_DECODER_DIR) $(COMMON_TEST_DIR)/$2.yaml

endef

$(foreach element, $(DECODERS), $(eval \
	$(call athrill-decoder-target,$(strip $(firstword $(subst :, , $(element)))),$(strip $(word 2, $(subst :, , $(element))))) \
	))
