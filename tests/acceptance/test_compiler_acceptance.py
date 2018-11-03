import os
import subprocess


def test_compiler_acceptance():
    test_path = 'tests/acceptance/files/'
    subprocess.run(['VMTranslator', os.path.join(test_path, 'vm_sample.vm')])

    with open(os.path.join(test_path, 'vm_sample.asm')) as f:
        result = f.readlines()

    with open(os.path.join(test_path, 'expected_asm.asm')) as f:
        expected = f.readlines()

    assert result == expected
