#include "arm_mcdhelper.hpp"
#include "ab_mcdhelper.hpp"
#include "at_mcdhelper.hpp"
#include "atb_mcdhelper.hpp"
#include "riscv_mcdhelper.hpp"
#include "pc_mcdhelper.hpp"
#include "cc_mcdhelper.hpp"
#include "dt16x2_mcdhelper.hpp"
#include "dt32x1_mcdhelper.hpp"

void setup_decoders()
{
    arm::mcdhelper::setup_decoder();
    ab::mcdhelper::setup_decoder();
    at::mcdhelper::setup_decoder();
    atb::mcdhelper::setup_decoder();
    riscv::mcdhelper::setup_decoder();
    pc::mcdhelper::setup_decoder();
    cc::mcdhelper::setup_decoder();
    dt16x2::mcdhelper::setup_decoder();
    dt32x1::mcdhelper::setup_decoder();
}
