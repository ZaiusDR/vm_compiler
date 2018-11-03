import pytest

from vmcompiler import constants
from vmcompiler import translator


@pytest.fixture(scope='module')
def vm_translator():
    return translator.Translator('fake_static_name')


def test_translate(vm_translator):
    push_constant_0 = 'push constant 0'
    pop_static_5 = 'pop static 5'
    add = 'add'

    assert vm_translator.translate(push_constant_0) \
        == constants.PUSH_CONSTANT.format(push_constant_0, '0')
    assert vm_translator.translate(pop_static_5) \
        == constants.POP_STATIC.format(pop_static_5, 'fake_static_name', '5')
    assert vm_translator.translate(add) == constants.OPS.format(add, '+')


# Memory Access tests
def test__push_constant(vm_translator):
    push_constant = 'push constant 10'
    vm_translator.instruction = push_constant
    expected_asm = constants.PUSH_CONSTANT.format(push_constant, '10')

    assert vm_translator._push_constant() == expected_asm


def test__push_reg_segment(vm_translator):
    push_reg_segment = 'push local 10'
    vm_translator.instruction = push_reg_segment
    expected_asm = constants.PUSH_REG_SEGMENT.format(
        push_reg_segment, '10', 'LCL'
    )

    assert vm_translator._push_reg_segment() == expected_asm


def test__pop_reg_segment(vm_translator):
    pop_reg_seg = 'pop local 0'
    vm_translator.instruction = pop_reg_seg
    expected_asm = constants.POP_REG_SEGMENT.format(pop_reg_seg, '0', 'LCL')

    assert vm_translator._pop_reg_segment() == expected_asm


def test__push_temp(vm_translator):
    push_temp = 'push temp 2'
    vm_translator.instruction = push_temp
    expected_asm = constants.PUSH_TEMP.format(push_temp, '2')

    assert vm_translator._push_temp() == expected_asm


def test__pop_temp(vm_translator):
    pop_temp = 'pop temp 2'
    vm_translator.instruction = pop_temp
    expected_asm = constants.POP_TEMP.format(pop_temp, '2')

    assert vm_translator._pop_temp() == expected_asm


def test__push_static(vm_translator):
    push_static = 'push static 0'
    vm_translator.instruction = push_static
    expected_asm = constants.PUSH_STATIC.format(
        push_static, 'fake_static_name', '0'
    )

    assert vm_translator._push_static() == expected_asm


def test__pop_static(vm_translator):
    pop_static = 'pop static 0'
    vm_translator.instruction = pop_static
    expected_asm = constants.POP_STATIC.format(
        pop_static, 'fake_static_name', '0'
    )

    assert vm_translator._pop_static() == expected_asm


def test__push_pointer(vm_translator):
    point_this = 'push pointer 0'
    vm_translator.instruction = point_this
    this_expected_asm = constants.PUSH_POINTER.format(point_this, 'THIS')

    assert vm_translator._push_pointer() == this_expected_asm


def test__pop_pointer(vm_translator):
    point_that = 'pop pointer 1'
    vm_translator.instruction = point_that
    that_expected_asm = constants.POP_POINTER.format(point_that, 'THAT')

    assert vm_translator._pop_pointer() == that_expected_asm


# Logic Operation tests
def test__ops(vm_translator):
    add_inst = 'add'
    sub_inst = 'sub'
    and_inst = 'and'
    or_inst = 'or'

    expected_asm_add = constants.OPS.format(add_inst, '+')
    expected_asm_sub = constants.OPS.format(sub_inst, '-')
    expected_asm_and = constants.OPS.format(and_inst, '&')
    expected_asm_or = constants.OPS.format(or_inst, '|')

    vm_translator.instruction = add_inst
    assert vm_translator._ops() == expected_asm_add

    vm_translator.instruction = sub_inst
    assert vm_translator._ops() == expected_asm_sub

    vm_translator.instruction = and_inst
    assert vm_translator._ops() == expected_asm_and

    vm_translator.instruction = or_inst
    assert vm_translator._ops() == expected_asm_or


def test__negation(vm_translator):
    neg_inst = 'neg'
    not_inst = 'not'

    expected_asm_neg = constants.NEG.format(neg_inst, '-')
    expected_asm_not = constants.NEG.format(not_inst, '!')

    vm_translator.instruction = neg_inst
    assert vm_translator._negation() == expected_asm_neg

    vm_translator.instruction = not_inst
    assert vm_translator._negation() == expected_asm_not


def test__comp(vm_translator):
    less_than = 'lt'
    greater_than = 'gt'
    equal = 'eq'

    expected_asm_lt = constants.COMP.format(
        less_than, 3000, 'JLT'
    )
    expected_asm_gt = constants.COMP.format(
        greater_than, 3001, 'JGT'
    )
    expected_asm_eq = constants.COMP.format(
        equal, 3002, 'JEQ'
    )

    vm_translator.instruction = less_than
    assert vm_translator._comp() == expected_asm_lt
    assert vm_translator.label_count == 3001

    vm_translator.instruction = greater_than
    assert vm_translator._comp() == expected_asm_gt
    assert vm_translator.label_count == 3002

    vm_translator.instruction = equal
    assert vm_translator._comp() == expected_asm_eq
    assert vm_translator.label_count == 3003


# Helper methods tests
def test__access_method(vm_translator):
    push_this = 'push this 10'
    pop_local = 'pop local 10'
    pop_temp = 'pop temp 2'
    push_constant = 'push constant 15'
    pop_static = 'pop static 5'
    push_pointer = 'push pointer 0'

    vm_translator.instruction = push_this
    assert vm_translator.access_method == vm_translator._push_reg_segment

    vm_translator.instruction = pop_local
    assert vm_translator.access_method == vm_translator._pop_reg_segment

    vm_translator.instruction = pop_temp
    assert vm_translator.access_method == vm_translator._pop_temp

    vm_translator.instruction = push_constant
    assert vm_translator.access_method == vm_translator._push_constant

    vm_translator.instruction = pop_static
    assert vm_translator.access_method == vm_translator._pop_static

    vm_translator.instruction = push_pointer
    assert vm_translator.access_method == vm_translator._push_pointer


def test__logic_method(vm_translator):
    add_inst = 'add'
    sub_inst = 'sub'
    neg_inst = 'neg'
    and_inst = 'and'
    or_inst = 'or'
    not_inst = 'not'

    vm_translator.instruction = add_inst
    assert vm_translator.logic_method == vm_translator._ops

    vm_translator.instruction = sub_inst
    assert vm_translator.logic_method == vm_translator._ops

    vm_translator.instruction = neg_inst
    assert vm_translator.logic_method == vm_translator._negation

    vm_translator.instruction = and_inst
    assert vm_translator.logic_method == vm_translator._ops

    vm_translator.instruction = or_inst
    assert vm_translator.logic_method == vm_translator._ops

    vm_translator.instruction = not_inst
    assert vm_translator.logic_method == vm_translator._negation


def test__parse_instruction(vm_translator):
    instruction = 'push constant 10'
    vm_translator.instruction = instruction
    expected_dict = {
        'command': 'push',
        'segment': 'constant',
        'index': '10'
    }

    assert vm_translator.parsed_instruction == expected_dict


def test__is_access_command(vm_translator):
    access_instruction = 'push local 10'
    not_access_instruction = 'add'

    vm_translator.instruction = access_instruction
    assert vm_translator.is_access_command

    vm_translator.instruction = not_access_instruction
    assert not vm_translator.is_access_command


def test__is_reg_segment(vm_translator):
    regular_segment = 'push local 10'
    not_regular_segment = 'push constant 0'

    vm_translator.instruction = regular_segment
    assert vm_translator.is_reg_segment

    vm_translator.instruction = not_regular_segment
    assert not vm_translator.is_reg_segment


def test__access_type(vm_translator):
    reg_seg_instruction = 'push this 10'
    temp_instruction = 'pop temp 5'

    vm_translator.instruction = reg_seg_instruction
    assert vm_translator.access_type == 'reg_segment'

    vm_translator.instruction = temp_instruction
    assert vm_translator.access_type == 'temp'


def test__is_static(vm_translator):
    static_inst = 'push static 10'
    not_static_inst = 'push local 0'

    vm_translator.instruction = static_inst
    assert vm_translator.is_static

    vm_translator.instruction = not_static_inst
    assert not vm_translator.is_static
