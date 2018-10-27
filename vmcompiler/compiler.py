from vmcompiler import translator


class Compiler():
    def __init__(self, vm_file, asm_file, static_name):
        self.vm_file = vm_file
        self.asm_file = asm_file
        self.static_name = static_name

    def compile(self):
        for raw_line in self.vm_file.readlines():
            instruction = self._clean_line(raw_line)
            if not instruction:
                continue
            translation = translator.translate(instruction, self.static_name)
            self.asm_file.write(translation)

    def _clean_line(self, line):
        if '//' in line:
            line = line.split('//')[0]
        return line.strip()
