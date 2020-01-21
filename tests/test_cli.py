from unittest import mock

import pytest
from click.testing import CliRunner

from danger_python.cli import cli
from tests.fixtures.shell import (danger_js_missing_path_fixture,
                                  danger_js_path_fixture,
                                  danger_success_fixture, subprocess_fixture)


def test_pr_command_invokes_danger_js_passing_arguments():
    """
    Test that pr command invokes danger_js passing correct arguments.
    """
    runner = CliRunner()
    arguments = [
        "pr",
        "https://github.com/microsoft/TypeScript/pull/34806",
        "--use-github-checks",
    ]
    danger_path = "/usr/bin/danger-js"
    expected_arguments = [
        "pr",
        "https://github.com/microsoft/TypeScript/pull/34806",
        "--use-github-checks",
        "-p",
        "danger-python",
        "-u",
    ]
    danger_fixture = danger_success_fixture(
        danger_path=danger_path, output="danger-js output", arguments=expected_arguments
    )

    with subprocess_fixture(danger_js_path_fixture(danger_path), danger_fixture):
        result = runner.invoke(cli, arguments)

    assert result.exit_code == 0
    assert result.output == "danger-js output\n"


def test_local_command_invokes_danger_js_passing_arguments():
    """
    Test that local command invokes danger_js passing correct arguments.
    """
    runner = CliRunner()
    arguments = [
        "local",
        "-i",
        "fake_danger_id",
        "-t",
    ]
    danger_path = "/usr/bin/js-danger"
    expected_arguments = [
        "local",
        "-i",
        "fake_danger_id",
        "-t",
        "-p",
        "danger-python",
        "-u",
    ]
    danger_fixture = danger_success_fixture(
        danger_path=danger_path,
        output="parsed local output",
        arguments=expected_arguments,
    )

    with subprocess_fixture(danger_js_path_fixture(danger_path), danger_fixture):
        result = runner.invoke(cli, arguments)

    assert result.exit_code == 0
    assert result.output == "parsed local output\n"


def test_ci_command_invokes_danger_js_passing_arguments():
    """
    Test that ci command invokes danger_js passing correct arguments.
    """
    runner = CliRunner()
    arguments = [
        "ci",
        "-v",
        "--no-publish-check",
    ]
    danger_path = "/usr/bin/very-danger"
    expected_arguments = ["ci", "-v", "--no-publish-check", "-p", "danger-python", "-u"]
    danger_fixture = danger_success_fixture(
        danger_path=danger_path, output="The output!", arguments=expected_arguments
    )

    with subprocess_fixture(danger_js_path_fixture(danger_path), danger_fixture):
        result = runner.invoke(cli, arguments)

    assert result.exit_code == 0
    assert result.output == "The output!\n"


@pytest.mark.parametrize(
    "dangerfile", ['print("Hello world")\n' 'print("Goodbye world")']
)
@pytest.mark.usefixtures("danger")
def test_run_command_invokes_dangerfile():
    """
    Test that run command invokes dangerfile.py contents.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["run"])

    assert result.exit_code == 0
    assert result.output == "Hello world\nGoodbye world\n"


@pytest.mark.parametrize("dangerfile", ["This is not a valid syntax of Python"])
@pytest.mark.usefixtures("danger")
def test_run_command_shows_traceback_when_dangerfile_fails():
    """
    Test that run command shows traceback when dangerfile.py fails.
    """
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["run"])

    expected_error = (
        "There was an error when executing dangerfile.py:\n"
        "SyntaxError at line 1: invalid syntax\n\n"
        "Stacktrace:\n"
    )

    assert result.exit_code == -1
    assert result.stderr.startswith(expected_error)


@pytest.mark.parametrize("dangerfile", ['print("Default command")'])
@pytest.mark.usefixtures("danger")
def test_default_command_invokes_dangerfile():
    """
    Test that default command invokes dangerfily.py contents.
    """
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert result.output == "Default command\n"


@pytest.mark.parametrize("modified_files", [["a.py", "b.py"]])
@pytest.mark.parametrize("dangerfile", ["print(danger.git.modified_files)"])
@pytest.mark.usefixtures("danger")
def test_executing_dangerfile_passes_danger_instance_to_the_script():
    """
    Test that executing run command passes danger instance with parsed input
    to the Dangerfile locals.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["run"])

    assert result.exit_code == 0
    assert result.output == "['a.py', 'b.py']\n"
