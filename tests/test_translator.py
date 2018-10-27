from vmcompiler import constants
from vmcompiler import translator


def test_translate():
    push_constant_0 = 'push constant 0'
    add = 'add'
    pop_static_5 = 'pop static 5'

    assert translator.translate(push_constant_0, 'fake_static_name') \
        == constants.PUSH_CONSTANT.format(push_constant_0, '0')
    assert translator.translate(add, 'fake_static_name') \
        == constants.OPS.format(add, '+')
    assert translator.translate(pop_static_5, 'fake_static_name') \
        == constants.POP_STATIC.format(pop_static_5, 'fake_static_name', '5')


# Memory Access tests
def test__push_constant():
    instruction = 'push constant 10'
    expected_asm = constants.PUSH_CONSTANT.format(instruction, '10')

    assert translator._push_constant(instruction) == expected_asm


def test__push_reg_segment():
    instruction = 'push local 10'
    expected_asm = constants.PUSH_REG_SEGMENT.format(instruction, '10', 'LCL')

    assert translator._push_reg_segment(instruction) == expected_asm


def test__pop_reg_segment():
    instruction = 'pop local 0'
    expected_asm = constants.POP_REG_SEGMENT.format(instruction, '0', 'LCL')

    assert translator._pop_reg_segment(instruction) == expected_asm


def test__push_temp():
    instruction = 'push temp 2'
    expected_asm = constants.PUSH_TEMP.format(instruction, '2')

    assert translator._push_temp(instruction) == expected_asm


def test__pop_temp():
    instruction = 'pop temp 2'
    expected_asm = constants.POP_TEMP.format(instruction, '2')

    assert translator._pop_temp(instruction) == expected_asm


def test__push_static():
    instruction = 'push static 0'
    expected_asm = constants.PUSH_STATIC.format(
        instruction, 'fake_static_name', '0'
    )

    assert translator._push_static(instruction, 'fake_static_name') \
        == expected_asm


def test__pop_static():
    instruction = 'pop static 0'
    expected_asm = constants.POP_STATIC.format(
        instruction, 'fake_static_name', '0'
    )

    assert translator._pop_static(instruction, 'fake_static_name') \
        == expected_asm


def test__push_pointer():
    point_this = 'push pointer 0'
    this_expected_asm = constants.PUSH_POINTER.format(point_this, 'THIS')

    assert translator._push_pointer(point_this) == this_expected_asm


def test__pop_pointer():
    point_that = 'pop pointer 1'
    that_expected_asm = constants.POP_POINTER.format(point_that, 'THAT')

    assert translator._pop_pointer(point_that) == that_expected_asm


# Logic Operation tests
def test__ops():
    add_inst = 'add'
    sub_inst = 'sub'
    and_inst = 'and'
    or_inst = 'or'

    expected_asm_add = constants.OPS.format(add_inst, '+')
    expected_asm_sub = constants.OPS.format(sub_inst, '-')
    expected_asm_and = constants.OPS.format(and_inst, '&')
    expected_asm_or = constants.OPS.format(or_inst, '|')

    assert translator._ops(add_inst) == expected_asm_add
    assert translator._ops(sub_inst) == expected_asm_sub
    assert translator._ops(and_inst) == expected_asm_and
    assert translator._ops(or_inst) == expected_asm_or


def test__negation():
    neg_inst = 'neg'
    not_inst = 'not'

    expected_asm_neg = constants.NEG.format(neg_inst, '-')
    expected_asm_not = constants.NEG.format(not_inst, '!')

    assert translator._negation(neg_inst) == expected_asm_neg
    assert translator._negation(not_inst) == expected_asm_not


# Helper methods tests
def test__get_access_method():
    push_this = 'push this 10'
    pop_local = 'pop local 10'
    pop_temp = 'pop temp 2'
    push_constant = 'push constant 15'
    pop_static = 'pop static 5'
    push_pointer = 'push pointer 0'

    assert translator._get_access_method(push_this) \
        == translator._push_reg_segment
    assert translator._get_access_method(pop_local) \
        == translator._pop_reg_segment
    assert translator._get_access_method(pop_temp) \
        == translator._pop_temp
    assert translator._get_access_method(push_constant) \
        == translator._push_constant
    assert translator._get_access_method(pop_static) \
        == translator._pop_static
    assert translator._get_access_method(push_pointer) \
        == translator._push_pointer


def test__get_logic_method():
    add_inst = 'add'
    sub_inst = 'sub'
    neg_inst = 'neg'
    and_inst = 'and'
    or_inst = 'or'
    not_inst = 'not'

    assert translator._get_logic_method(add_inst) == translator._ops
    assert translator._get_logic_method(sub_inst) == translator._ops
    assert translator._get_logic_method(neg_inst) == translator._negation
    assert translator._get_logic_method(and_inst) == translator._ops
    assert translator._get_logic_method(or_inst) == translator._ops
    assert translator._get_logic_method(not_inst) == translator._negation


def test__parse_instruction():
    instruction = 'push constant 10'
    expected_dict = {
        'command': 'push',
        'segment': 'constant',
        'index': '10'
    }

    assert translator._parse_instruction(instruction) == expected_dict


def test__is_access_command():
    access_instruction = 'push local 10'
    not_access_instruction = 'add'

    assert translator._is_access_command(access_instruction)
    assert not translator._is_access_command(not_access_instruction)


def test__is_reg_segment():
    regular_segment = 'push local 10'
    not_regular_segment = 'push constant 0'

    assert translator._is_reg_segment(regular_segment)
    assert not translator._is_reg_segment(not_regular_segment)


def test__get_access_type():
    reg_seg_instruction = 'push this 10'
    temp_instruction = 'pop temp 5'

    assert translator._get_access_type(reg_seg_instruction) == 'reg_segment'
    assert translator._get_access_type(temp_instruction) == 'temp'


def test__is_static():
    static_inst = 'push static 10'
    not_static_inst = 'push local 0'

    assert translator._is_static(static_inst)
    assert not translator._is_static(not_static_inst)
