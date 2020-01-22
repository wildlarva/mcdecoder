#include "ab_mcdhelper.h"
#include "arm_mcdhelper.h"
#include "at_mcdhelper.h"
#include "atb_mcdhelper.h"
#include "cc_mcdhelper.h"
#include "dt16x2_mcdhelper.h"
#include "dt32x1_mcdhelper.h"
#include "pc_mcdhelper.h"
#include "riscv_mcdhelper.h"

namespace mcdhelper {

void SetupDecoders() {
  arm::mcdhelper::SetupDecoder();
  ab::mcdhelper::SetupDecoder();
  at::mcdhelper::SetupDecoder();
  atb::mcdhelper::SetupDecoder();
  riscv::mcdhelper::SetupDecoder();
  pc::mcdhelper::SetupDecoder();
  cc::mcdhelper::SetupDecoder();
  dt16x2::mcdhelper::SetupDecoder();
  dt32x1::mcdhelper::SetupDecoder();
}

}  // namespace mcdhelper
