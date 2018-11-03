from vmcompiler import constants


class Translator():
    label_count = 3000

    def __init__(self, static_name):
        self.instruction = None
        self.static_name = static_name

    def translate(self, instruction):
        self.instruction = instruction
        if self.is_access_command:
            return self.access_method()
        return self.logic_method()

    # Memory Access methods
    def _push_constant(self):
        translation = constants.PUSH_CONSTANT.format(
            self.instruction, self.parsed_instruction['index']
        )
        return translation

    def _push_reg_segment(self):
        translation = constants.PUSH_REG_SEGMENT.format(
            self.instruction,
            self.parsed_instruction['index'],
            constants.POINTER_MAPS[self.parsed_instruction['segment']]
        )
        return translation

    def _pop_reg_segment(self):
        translation = constants.POP_REG_SEGMENT.format(
            self.instruction,
            self.parsed_instruction['index'],
            constants.POINTER_MAPS[self.parsed_instruction['segment']]
        )
        return translation

    def _push_temp(self):
        translation = constants.PUSH_TEMP.format(
            self.instruction,
            self.parsed_instruction['index']
        )
        return translation

    def _pop_temp(self):
        translation = constants.POP_TEMP.format(
            self.instruction,
            self.parsed_instruction['index']
        )
        return translation

    def _push_static(self):
        translation = constants.PUSH_STATIC.format(
            self.instruction,
            self.static_name,
            self.parsed_instruction['index']
        )
        return translation

    def _pop_static(self):
        translation = constants.POP_STATIC.format(
            self.instruction,
            self.static_name,
            self.parsed_instruction['index']
        )
        return translation

    def _push_pointer(self):
        translation = constants.PUSH_POINTER.format(
            self.instruction,
            constants.POINTER_MAPPING[self.parsed_instruction['index']]
        )
        return translation

    def _pop_pointer(self):
        translation = constants.POP_POINTER.format(
            self.instruction,
            constants.POINTER_MAPPING[self.parsed_instruction['index']]
        )
        return translation

    # Logic Operation methods
    def _ops(self):
        return constants.OPS.format(
            self.instruction, constants.OPS_MAPS[self.instruction]
        )

    def _negation(self):
        return constants.NEG.format(
            self.instruction, constants.NEG_MAPS[self.instruction]
        )

    def _comp(self):
        translation = constants.COMP.format(
            self.instruction,
            self.label_count,
            constants.COMP_MAPS[self.instruction]
        )
        self.label_count += 1
        return translation

    # Helper Methods
    @property
    def access_method(self):
        access_maps = {
            'temp': {
                'push': self._push_temp,
                'pop': self._pop_temp
            },
            'reg_segment': {
                'push': self._push_reg_segment,
                'pop': self._pop_reg_segment
            },
            'constant': {
                'push': self._push_constant
            },
            'static': {
                'push': self._push_static,
                'pop': self._pop_static
            },
            'pointer': {
                'push': self._push_pointer,
                'pop': self._pop_pointer
            }
        }

        command = self.parsed_instruction['command']
        return access_maps[self.access_type][command]

    @property
    def logic_method(self):
        logic_maps = {
            'add': self._ops,
            'sub': self._ops,
            'neg': self._negation,
            'eq': self._comp,
            'gt': self._comp,
            'lt': self._comp,
            'and': self._ops,
            'or': self._ops,
            'not': self._negation
        }
        return logic_maps[self.instruction]

    @property
    def parsed_instruction(self):
        dict_keys = ['command', 'segment', 'index']
        key_value_maps = [
            (key, value)
            for key, value
            in zip(dict_keys, self.instruction.split())
        ]
        return dict(key_value_maps)

    @property
    def is_access_command(self):
        return 'push' in self.instruction or 'pop' in self.instruction

    @property
    def is_reg_segment(self):
        regular_segments = ['local', 'argument', 'this', 'that']
        return self.instruction.split()[1] in regular_segments

    @property
    def access_type(self):
        if self.is_reg_segment:
            return 'reg_segment'
        return self.parsed_instruction['segment']

    @property
    def is_static(self):
        return 'static' in self.instruction
