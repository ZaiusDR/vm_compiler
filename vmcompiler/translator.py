import random

from vmcompiler import constants


def translate(instruction, static_name):
    if _is_access_command(instruction):
        # This (piece of crap) is to avoid changing too much the implementation
        # in order to support static Memory Access
        if _is_static(instruction):
            return _get_access_method(instruction)(instruction, static_name)
        else:
            return _get_access_method(instruction)(instruction)
    return _get_logic_method(instruction)(instruction)


# Memory Access methods
def _push_constant(instruction):
    parsed_instruction = _parse_instruction(instruction)
    translation = constants.PUSH_CONSTANT.format(
        instruction, parsed_instruction['index']
    )
    return translation


def _push_reg_segment(instruction):
    parsed_instruction = _parse_instruction(instruction)
    translation = constants.PUSH_REG_SEGMENT.format(
        instruction,
        parsed_instruction['index'],
        constants.POINTER_MAPS[parsed_instruction['segment']]
    )
    return translation


def _pop_reg_segment(instruction):
    parsed_instruction = _parse_instruction(instruction)
    translation = constants.POP_REG_SEGMENT.format(
        instruction,
        parsed_instruction['index'],
        constants.POINTER_MAPS[parsed_instruction['segment']]
    )
    return translation


def _push_temp(instruction):
    parsed_instruction = _parse_instruction(instruction)
    translation = constants.PUSH_TEMP.format(
        instruction,
        parsed_instruction['index']
    )
    return translation


def _pop_temp(instruction):
    parsed_instruction = _parse_instruction(instruction)
    translation = constants.POP_TEMP.format(
        instruction,
        parsed_instruction['index']
    )
    return translation


def _push_static(instruction, static_name):
    parsed_instruction = _parse_instruction(instruction)
    translation = constants.PUSH_STATIC.format(
        instruction,
        static_name,
        parsed_instruction['index']
    )
    return translation


def _pop_static(instruction, static_name):
    parsed_instruction = _parse_instruction(instruction)
    translation = constants.POP_STATIC.format(
        instruction,
        static_name,
        parsed_instruction['index']
    )
    return translation


def _push_pointer(instruction):
    parsed_instruction = _parse_instruction(instruction)
    translation = constants.PUSH_POINTER.format(
        instruction,
        constants.POINTER_MAPPING[parsed_instruction['index']]
    )
    return translation


def _pop_pointer(instruction):
    parsed_instruction = _parse_instruction(instruction)
    translation = constants.POP_POINTER.format(
        instruction,
        constants.POINTER_MAPPING[parsed_instruction['index']]
    )
    return translation


# Logic Operation methods
def _ops(instruction):
    return constants.OPS.format(instruction, constants.OPS_MAPS[instruction])


def _negation(instruction):
    return constants.NEG.format(instruction, constants.NEG_MAPS[instruction])


def _comp(instruction):
    return constants.COMP.format(
        instruction,
        # TODO: Get rid of this crap
        random.randint(3000, 3256),
        constants.COMP_MAPS[instruction]
    )


# Helper Methods
def _get_access_method(instruction):
    access_maps = {
        'temp': {
            'push': _push_temp,
            'pop': _pop_temp
        },
        'reg_segment': {
            'push': _push_reg_segment,
            'pop': _pop_reg_segment
        },
        'constant': {
            'push': _push_constant
        },
        'static': {
            'push': _push_static,
            'pop': _pop_static
        },
        'pointer': {
            'push': _push_pointer,
            'pop': _pop_pointer
        }
    }

    access_type = _get_access_type(instruction)
    parsed_instruction = _parse_instruction(instruction)
    return access_maps[access_type][parsed_instruction['command']]


def _get_logic_method(instruction):
    logic_maps = {
        'add': _ops,
        'sub': _ops,
        'neg': _negation,
        'eq': _comp,
        'gt': _comp,
        'lt': _comp,
        'and': _ops,
        'or': _ops,
        'not': _negation
    }
    return logic_maps[instruction]


def _parse_instruction(instruction):
    dict_keys = ['command', 'segment', 'index']
    key_value_maps = [
        (key, value)
        for key, value
        in zip(dict_keys, instruction.split())
    ]
    return dict(key_value_maps)


def _is_access_command(instruction):
    return 'push' in instruction or 'pop' in instruction


def _is_reg_segment(instruction):
    return instruction.split()[1] in ['local', 'argument', 'this', 'that']


def _get_access_type(instruction):
    if _is_reg_segment(instruction):
        return 'reg_segment'
    return _parse_instruction(instruction)['segment']


def _is_static(instruction):
    return 'static' in instruction
