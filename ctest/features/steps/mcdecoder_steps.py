from dataclasses import dataclass
from typing import Dict, List, Optional

from behave import given, then, when

from mcdecoder import core, emulator

_DEC_NAME_TO_MC_DESC_NAME: Dict[str, str] = {
    'arm': 'arm',
    'ab': 'arm_big',
    'at': 'arm_thumb',
    'atb': 'arm_thumb_big',
    'riscv': 'riscv',
    'pc': 'primitive_condition',
    'cc': 'complex_condition',
    'dt16x2': 'decision_tree_code16x2',
    'dt32x1': 'decision_tree_code32x1',
}


@dataclass
class _Context:
    decoder: str
    results: List[core.InstructionDecodeResult]
    result: Optional[core.InstructionDecodeResult]


@given('decoding instructions with the decoder "{decoder}"')
def given_decoding(context: _Context, decoder: str) -> None:
    context.decoder = decoder


@when('I decode "{code}"')
def when_decode(context: _Context, code: str) -> None:
    context.results = emulator._emulate(
        'test/' + _DEC_NAME_TO_MC_DESC_NAME[context.decoder] + '.yaml', code, 16, 'raw')

    if len(context.results) >= 1:
        context.result = context.results[0]


@then('the decoding should be succeeded')
def then_succeeded(context: _Context) -> None:
    assert len(context.results) == 1


@then('the decoding should be failed')
def then_failed(context: _Context) -> None:
    assert len(context.results) != 1


@then('the instruction should be "{instruction}"')
def then_instruction_be(context: _Context, instruction: str) -> None:
    assert context.result.decoder.name == instruction


@then('the fields "{fields}" should be "{values}"')
def then_fields_be(context: _Context, fields: str, values: str) -> None:
    field_list = fields.split(',')
    value_list = values.split(',')
    assert len(field_list) == len(value_list)

    for field, value in zip(field_list, value_list):
        field_results = [
            field_result for field_result in context.result.fields if field_result.decoder.name == field]
        assert len(field_results) == 1
        assert field_results[0].value == int(value, 16)
