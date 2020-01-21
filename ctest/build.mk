BUILD_DIR = build

include $(BUILD_DIR)/conanbuildinfo.mak

#----------------------------------------
#	 Make variables
#----------------------------------------

COMMON_TEST_DIR = ../test
TEMPLATE_DIR = templates
STEPS_DIR = features/step_definitions
DECODER_DIR = out

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

DECODER_SRCS = \
	$(foreach element, $(DECODERS), $(DECODER_DIR)/$(strip $(firstword $(subst :, , $(element))))_mcdecoder.c)

CSRCS = \
	stub.c

CSRCS += $(DECODER_SRCS)

HELPER_SRCS = \
	$(foreach element, $(DECODERS), $(DECODER_DIR)/$(strip $(firstword $(subst :, , $(element))))_mcdhelper.cpp)

CPP_SRCS = \
	mcdhelper.cpp \
	$(STEPS_DIR)/mcdecoder_steps.cpp

CPP_SRCS += $(HELPER_SRCS)

CXX_OBJ_FILES = \
	$(patsubst %.c, $(BUILD_DIR)/%.o, $(notdir $(CSRCS))) \
	$(patsubst %.cpp, $(BUILD_DIR)/%.o, $(notdir $(CPP_SRCS)))

CXX_INCLUDES = \
	. \
	$(DECODER_DIR)

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
CPPFLAGS += $(addprefix -I, $(CXX_INCLUDES))
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
	$(EXE_FILENAME) & bundle exec cucumber

$(EXE_FILENAME) : $(CXX_OBJ_FILES)
	$(CREATE_EXE_COMMAND)

$(BUILD_DIR)/%.o: %.c
	$(COMPILE_C_COMMAND)

$(BUILD_DIR)/%.o: $(DECODER_DIR)/%.c
	$(COMPILE_C_COMMAND)

$(BUILD_DIR)/%.o: %.cpp
	$(COMPILE_CXX_COMMAND)

$(BUILD_DIR)/%.o: $(DECODER_DIR)/%.cpp
	$(COMPILE_CXX_COMMAND)

$(BUILD_DIR)/%.o: $(STEPS_DIR)/%.cpp
	$(COMPILE_CXX_COMMAND)

define decoder-target
$(DECODER_DIR)/$1_mcdecoder.c $(DECODER_DIR)/$1_mcdhelper.cpp: $(COMMON_TEST_DIR)/$2.yaml
	mcdecoder generate --output $(DECODER_DIR) $(COMMON_TEST_DIR)/$2.yaml; \
	mcdecoder generate --template $(TEMPLATE_DIR)/athrill_helper --output $(DECODER_DIR) $(COMMON_TEST_DIR)/$2.yaml

endef

$(foreach element, $(DECODERS), $(eval \
	$(call decoder-target,$(strip $(firstword $(subst :, , $(element)))),$(strip $(word 2, $(subst :, , $(element))))) \
	))
