"""Tests for models.py and related database logic.

Run with: uv run pytest tests/
Requires offscreen Qt platform for model tests (set automatically below).
"""

import os
import sqlite3
import sys

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


# ---------------------------------------------------------------------------
# Session-scoped QApplication so Qt models can be instantiated
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def qapp():
    from PyQt6 import QtWidgets

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    return app


# ---------------------------------------------------------------------------
# Pure SQLite tests (no Qt required)
# ---------------------------------------------------------------------------


def make_db():
    """Return an in-memory SQLite connection with the pysdb3 schema applied."""
    from pysdb3.models import SCHEMA, DEFDATA

    conn = sqlite3.connect(":memory:")
    conn.text_factory = str
    for sql in SCHEMA.splitlines():
        conn.execute(sql)
    for sql in DEFDATA.splitlines():
        conn.execute(sql)
    conn.commit()
    return conn


def test_schema_creates_tables():
    conn = make_db()
    tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    assert {
        "sites",
        "units",
        "structype",
        "tags",
        "structdata",
        "tagged",
        "attach",
        "meta",
    }.issubset(tables)


def test_defdata_seeds_defaults():
    conn = make_db()
    units = conn.execute("SELECT name FROM units").fetchall()
    assert any("Default" in u[0] for u in units)
    structs = conn.execute("SELECT structure FROM structype").fetchall()
    assert {s[0] for s in structs} == {"S", "L"}


def test_insert_and_query_site():
    conn = make_db()
    unit_id = conn.execute("SELECT id FROM units LIMIT 1").fetchall()[0][0]
    conn.execute(
        "INSERT INTO sites (id_units, name, x_coord, y_coord, description) VALUES (?,?,?,?,?)",
        (unit_id, "TestSite", 14.5, 50.1, ""),
    )
    conn.commit()
    rows = conn.execute("SELECT name FROM sites WHERE name=?", ("TestSite",)).fetchall()
    assert len(rows) == 1


# ---------------------------------------------------------------------------
# Qt model tests (require qapp fixture)
# ---------------------------------------------------------------------------


def test_site_model_rowcount(qapp):
    from pysdb3.models import SiteModel

    model = SiteModel([[1, "A", 0.0, 0.0, "", 1], [2, "B", 1.0, 2.0, "", 1]])
    assert model.rowCount() == 2


def test_site_model_index_lookup(qapp):
    from pysdb3.models import SiteModel

    model = SiteModel([[10, "Alpha", 0.0, 0.0, "", 1], [20, "Beta", 1.0, 2.0, "", 1]])
    assert model.id2row[10] == 0
    assert model.id2row[20] == 1
    assert model.row2id[0] == 10
    assert model.row2id[1] == 20


def test_site_model_append_updates_index(qapp):
    from pysdb3.models import SiteModel

    model = SiteModel([[1, "A", 0.0, 0.0, "", 1]])
    model.appendRow([2, "B", 0.0, 0.0, "", 1])
    assert model.rowCount() == 2
    assert model.id2row[2] == 1


def test_site_model_remove_updates_index(qapp):
    from pysdb3.models import SiteModel

    model = SiteModel([[1, "A", 0.0, 0.0, "", 1], [2, "B", 0.0, 0.0, "", 1]])
    index = model.index(0, 0)
    model.removeRow(index)
    assert model.rowCount() == 1
    assert 1 not in model.id2row
    assert model.id2row[2] == 0


def test_tag_model_setdata_emits_only_on_change(qapp):
    from PyQt6 import QtCore
    from pysdb3.models import TagModel, tagcol

    model = TagModel([[1, "T", "", QtCore.Qt.CheckState.Unchecked]])
    emitted = []
    model.dataChanged.connect(lambda tl, br: emitted.append((tl.row(), br.row())))

    idx = model.index(0, tagcol["check"])

    # Setting same value → no emission
    model.setData(
        idx, QtCore.Qt.CheckState.Unchecked, QtCore.Qt.ItemDataRole.CheckStateRole
    )
    assert len(emitted) == 0

    # Changing value → emission
    model.setData(
        idx, QtCore.Qt.CheckState.Checked, QtCore.Qt.ItemDataRole.CheckStateRole
    )
    assert len(emitted) == 1

    # Setting same value again → no additional emission
    model.setData(
        idx, QtCore.Qt.CheckState.Checked, QtCore.Qt.ItemDataRole.CheckStateRole
    )
    assert len(emitted) == 1


def test_unit_model_bidirectional_lookup(qapp):
    from pysdb3.models import UnitModel

    model = UnitModel([[5, "Unit A", "desc"], [10, "Unit B", ""]])
    assert model.id2row[5] == 0
    assert model.id2row[10] == 1
    assert model.row2id[0] == 5
    assert model.row2id[1] == 10


def test_structure_model_isplanar(qapp):
    from pysdb3.models import StructureModel

    model = StructureModel(
        [
            [1, "S", 1, "planar", 0, 0],
            [2, "L", 0, "linear", 0, 0],
        ]
    )
    assert model.isplanar(0) is True
    assert model.isplanar(1) is False
