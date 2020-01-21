#include "arm_mcdhelper.hpp"
#include "ab_mcdhelper.hpp"
#include "at_mcdhelper.hpp"
#include "atb_mcdhelper.hpp"
#include "riscv_mcdhelper.hpp"
#include "pc_mcdhelper.hpp"
#include "cc_mcdhelper.hpp"
#include "dt16x2_mcdhelper.hpp"
#include "dt32x1_mcdhelper.hpp"

namespace mcdhelper
{

void SetupDecoders()
{
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

} // namespace mcdhelper
