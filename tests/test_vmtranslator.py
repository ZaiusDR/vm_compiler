import pytest

from vmcompiler import VMTranslator


def test__parse_args__no_file():
    with pytest.raises(SystemExit):
        VMTranslator._parse_args([''])


def test__parse_static_name():
    assert VMTranslator._parse_static_name('/somefile.vm') == 'somefile'
