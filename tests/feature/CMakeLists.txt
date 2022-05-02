#------------------------------------------------------------------------------
# Setup Cucumber-Cpp
#------------------------------------------------------------------------------

# Fetch and load Cucumber-Cpp as ExternalProject
set(CUKE_ENABLE_BOOST_TEST OFF)
set(CUKE_ENABLE_QT OFF)
set(CUKE_TESTS_E2E OFF)
set(CUKE_TESTS_UNIT OFF)

include(FetchContent)
FetchContent_Declare(
  CucumberCpp
  GIT_REPOSITORY https://github.com/cucumber/cucumber-cpp.git
  GIT_TAG a41565d8fd7b87fd160e441602b398dc76f6d739
)
FetchContent_MakeAvailable(CucumberCpp)

# Get Google Test source directory
ExternalProject_Get_property(gmock SOURCE_DIR)
set(GTEST_ROOT ${SOURCE_DIR})

#------------------------------------------------------------------------------
# Variables
#------------------------------------------------------------------------------

# Types of decoders (mcdecoder --type option)
set(DECODER_TYPES c_decoder athrill)

# Generated decoder name prefixes
set(DECODERS
	arm
	ab
	at
	atb
	riscv
	pc
	cc
	dt16x2
	dt32x1
)

# Decoder models to generate decoders
# DECODER_MODELS must have the same size as that of DECORDERS
set(DECODER_MODELS
	arm
	arm_big
	arm_thumb
	arm_thumb_big
	riscv
	primitive_condition
	complex_condition
	decision_tree_code16x2
	decision_tree_code32x1
)

#------------------------------------------------------------------------------
# Derived variables
#------------------------------------------------------------------------------
set(DECODER_MODEL_FILES ${DECODER_MODELS})
list(TRANSFORM DECODER_MODEL_FILES PREPEND "${CMAKE_CURRENT_LIST_DIR}/../common/")
list(TRANSFORM DECODER_MODEL_FILES APPEND ".yaml")

list(LENGTH DECODERS DECODER_LENGTH)
math(EXPR DECODER_LAST_INDEX "${DECODER_LENGTH} - 1")

#------------------------------------------------------------------------------
# Test targets
#------------------------------------------------------------------------------

foreach(decoder_type ${DECODER_TYPES})
  #------------------------------------------------------------------------------
  # Derived variables for each decoder type
  #------------------------------------------------------------------------------
  set(DECODER_TEST_TARGET "${decoder_type}_test")
  set(DECODER_TEST "${decoder_type}_test")
  set(DECODER_DIR "${CMAKE_CURRENT_BINARY_DIR}/out/${decoder_type}")

  set(DECODER_FILES ${DECODERS})
  list(TRANSFORM DECODER_FILES PREPEND "${DECODER_DIR}/")
  list(TRANSFORM DECODER_FILES APPEND "_mcdecoder.c")

  set(DECODER_HELPER_FILES ${DECODERS})
  list(TRANSFORM DECODER_HELPER_FILES PREPEND "${DECODER_DIR}/")
  list(TRANSFORM DECODER_HELPER_FILES APPEND "_mcdhelper.cc")

  #------------------------------------------------------------------------------
  # Test targets for each decoder type
  #------------------------------------------------------------------------------
  add_executable(
    ${DECODER_TEST_TARGET}
    mcdecoder_setup.cc
    mcdhelper.cc
    features/step_definitions/mcdecoder_steps.cc
  )
  target_link_libraries(
    ${DECODER_TEST_TARGET}
    cucumber-cpp
  )
  target_include_directories(
    ${DECODER_TEST_TARGET} PRIVATE
    .
    ${DECODER_DIR}
    ${GTEST_ROOT}/googletest/include
  )

  #------------------------------------------------------------------------------
  # Commands to generate decoder files
  #------------------------------------------------------------------------------
  foreach(index RANGE ${DECODER_LAST_INDEX})
    list(GET DECODER_FILES ${index} decoder)
    list(GET DECODER_HELPER_FILES ${index} decoder_helper)
    list(GET DECODER_MODEL_FILES ${index} decoder_model)

    # Generate xxx_mcdecoder.cc
    add_custom_command(OUTPUT ${decoder}
      COMMAND mcdecoder generate --type ${decoder_type} --output ${DECODER_DIR} ${decoder_model}
      DEPENDS ${decoder_model}
    )

    # Generate xxx_mcdhelper.cc
    add_custom_command(OUTPUT ${decoder_helper}
      COMMAND mcdecoder generate --template ${CMAKE_CURRENT_LIST_DIR}/templates/${decoder_type}_helper --output ${DECODER_DIR} ${decoder_model}
      DEPENDS ${decoder_model}
    )

    # Add generated sources to test target
    target_sources(${DECODER_TEST_TARGET} PRIVATE ${decoder} ${decoder_helper})
  endforeach(index RANGE ${DECODER_LAST_INDEX})
  
  #------------------------------------------------------------------------------
  # Tests
  #------------------------------------------------------------------------------
  add_test(NAME ${DECODER_TEST}
    COMMAND bash -c "${CMAKE_CURRENT_BINARY_DIR}/${DECODER_TEST_TARGET} & bundle exec cucumber"
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  )
  set_tests_properties(${DECODER_TEST} PROPERTIES RUN_SERIAL ON)

endforeach(decoder_type ${DECODER_TYPES})
