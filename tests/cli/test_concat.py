# -*- coding: utf-8 -*-
from pathlib import Path

from mckit.cli.runner import mckit
from mckit.utils.resource import filename_resolver

data_filename_resolver = filename_resolver("tests.cli")


def test_when_there_is_no_args(runner, disable_log):
    with runner.isolated_filesystem():
        result = runner.invoke(mckit, args=["concat"], catch_exceptions=False)
        assert result.exit_code != 0, "Should fail when no arguments provided"
        assert "Usage:" in result.output


def test_not_existing_file(runner, disable_log):
    result = runner.invoke(
        mckit, args=["concat", "not-existing.txt"], catch_exceptions=False
    )
    assert result.exit_code > 0
    assert "Path 'not-existing.txt' does not exist" in result.output


def test_when_only_part_is_specified(runner, disable_log):
    part = data_filename_resolver("data/concat/test_load_table_1.csv")
    with runner.isolated_filesystem():
        result = runner.invoke(mckit, args=["concat", part], catch_exceptions=False)
        assert result.exit_code == 0, (
            "Should success without specified output: " + result.output
        )
        assert (
            "x   y" in result.output
        ), "Should send output to stdout, when the output is not specified"


def test_when_output_is_specified(runner, disable_log):
    part = data_filename_resolver("data/concat/test_load_table_1.csv")
    with runner.isolated_filesystem() as prefix:
        output_file = Path(prefix) / "test_when_output_is_specified.txt"
        result = runner.invoke(
            mckit,
            args=["concat", "--output", str(output_file), part],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, (
            "Should success with specified output: " + result.output
        )
        assert output_file.exists(), "Should create output file " + output_file
        # noinspection PyCompatibility
        assert "x   y" in output_file.read_text(
            encoding="Cp1251"
        ), f"Should contain content of '{part}'"


# noinspection PyCompatibility
def test_when_two_parts_are_specified(runner, disable_log):
    part1 = data_filename_resolver("data/concat/test_load_table_1.csv")
    part2 = data_filename_resolver("data/concat/test_load_table_2.csv")
    with runner.isolated_filesystem() as prefix:
        output_file = Path(prefix) / "test_when_output_is_specified.txt"
        result = runner.invoke(
            mckit,
            args=["concat", "--output", str(output_file), part1, part2],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, (
            "Should success with specified output: " + result.output
        )
        assert output_file.exists(), "Should create output file " + output_file
        text = output_file.read_text(encoding="Cp1251")
        assert "x   y" in text, f"Should contain content of '{part1}'"
        assert "x    ;   y" in text, f"Should contain content of '{part2}'"


def test_when_output_file_exists_and_override_is_not_specified(runner, disable_log):
    part = data_filename_resolver("data/concat/test_load_table_1.csv")
    with runner.isolated_filesystem() as prefix:
        output_file = Path(prefix) / "test_when_output_is_specified.txt"
        output_file.touch(exist_ok=False)
        result = runner.invoke(
            mckit, args=["concat", "-o", str(output_file), part], catch_exceptions=False
        )
        assert (
            result.exit_code != 0
        ), "Should fail when output file exist and override is not specified"
