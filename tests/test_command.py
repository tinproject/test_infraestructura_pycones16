import pytest
import requests


def test__echo(Command):
    cmd = Command("echo 'Hola PyConES'")
    assert cmd.rc == 0
    assert "PyConES" in cmd.stdout
    assert cmd.stderr == ""


def test__echo_output(Command):
    output = Command.check_output("echo 'Hola PyConES'")
    assert "Hola" in output


def test__echo_return_code(LocalCommand):
    cmd = LocalCommand.run_test("echo 'Hola PyConES'")
    assert cmd.rc == 0
