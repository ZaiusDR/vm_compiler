from vmcompiler import translator


class Compiler():
    def __init__(self, vm_file, asm_file, static_name):
        self.vm_file = vm_file
        self.asm_file = asm_file
        self.static_name = static_name

    def compile(self):
        vm_translator = translator.Translator(self.static_name)
        for raw_line in self.vm_file.readlines():
            instruction = self._clean_line(raw_line)
            if not instruction:
                continue
            translation = vm_translator.translate(instruction)
            self.asm_file.write(translation)

    def _clean_line(self, line):
        if '//' in line:
            line = line.split('//')[0]
        return line.strip()
