"""Spec §8.5/§22.1: CSV/Excel formula-injection protection on exports.

User-controlled free text (chat messages, notes, gratitude/CBT entries) is written into
CSV exports that clinicians/researchers open in spreadsheets. A cell starting with = + - @
must be neutralised so it renders as text, not an executable formula.
"""
import io

import pytest

import api


DANGEROUS = ["=cmd|' /C calc'!A0", "+1+1", "-2+3", "@SUM(A1)", "\ttab", "\rreturn"]
SAFE = ["hello", "2+2=4", "user@example only mid", "", "normal note"]


class TestSanitizeCsvCell:
    @pytest.mark.parametrize("value", DANGEROUS)
    def test_dangerous_cells_are_quoted(self, value):
        out = api.sanitize_csv_cell(value)
        assert out.startswith("'"), f"{value!r} not neutralised -> {out!r}"

    def test_safe_cells_unchanged(self):
        assert api.sanitize_csv_cell("hello") == "hello"
        assert api.sanitize_csv_cell("2+2=4") == "2+2=4"  # leading char is '2', safe

    def test_none_becomes_empty(self):
        assert api.sanitize_csv_cell(None) == ""

    def test_numbers_pass_through(self):
        assert api.sanitize_csv_cell(42) == "42"


class TestSafeCsvWriter:
    def test_writer_sanitises_rows(self):
        buf = io.StringIO()
        w = api.SafeCsvWriter(buf)
        w.writerow(["=danger", "safe", "@evil"])
        w.writerows([["-formula", "ok"]])
        content = buf.getvalue()
        # The raw dangerous tokens must not appear unquoted at a cell start.
        assert "'=danger" in content
        assert "'@evil" in content
        assert "'-formula" in content
        assert "safe" in content
