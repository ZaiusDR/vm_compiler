import io

from vmcompiler import compiler
from vmcompiler import constants


def test__compile():
    fake_vm_file_content = (
        'push constant 0\n'
        'push constant 5\n'
        'add\n'
    )
    expected_asm_file = '{0}{1}{2}'.format(
        constants.PUSH_CONSTANT.format('push constant 0', '0'),
        constants.PUSH_CONSTANT.format('push constant 5', '5'),
        constants.OPS.format('add', '+')
    )

    fake_vm_file = io.StringIO(fake_vm_file_content)
    fake_asm_file = io.StringIO(None)
    test_compiler = compiler.Compiler(
        fake_vm_file, fake_asm_file, 'fake_static_name'
    )
    test_compiler.compile()

    assert fake_asm_file.getvalue() == expected_asm_file


def test__clean_line():
    comment_line = '  FAKE=INSTRUCTION   // Fake comment\n'
    only_comment_line = '// Fake comment\n'

    test_compiler = compiler.Compiler(
        'fake_vm_file', 'fake_asm_file', 'static'
    )
    assert test_compiler._clean_line(comment_line) == 'FAKE=INSTRUCTION'
    assert test_compiler._clean_line(only_comment_line) == ''
