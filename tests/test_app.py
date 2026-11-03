from streamlit.testing.v1 import AppTest
from pathlib import Path
import pytest

APP = Path(__file__).resolve().parents[1] / "app.py"


@pytest.mark.parametrize("page", ["Paneli", "Social Golfers", "Sudoku", "Latin Square", "Pemët e kërkimit",
                                  "Analiza e performancës", "Shpjegimet matematikore"])
def test_pages_render_without_exception(page):
    app = AppTest.from_file(APP).run()
    app.sidebar.radio[0].set_value(page).run()
    assert not app.exception


def test_latin_interaction_and_persistent_result():
    app = AppTest.from_file(APP).run()
    app.sidebar.radio[0].set_value("Latin Square").run()
    app.button[0].click().run(timeout=15)
    assert not app.exception
    assert app.success
    app.run()
    assert app.success
