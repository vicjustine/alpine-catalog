import pytest

from catalog.settings import SettingsError, load

def test_defaults_load(tmp_path):
    assert load("catalog.ini").theme == "contrast"

def test_page_count_rounds_up(tmp_path): 
    settings = load("catalog.ini")
    assert settings.page_count(41) == 2

def test_unknown_theme_rejected(tmp_path): 
    bad= tmp_path / "catalog.ini"
    bad.write_text("[display]\ntheme=neon\npage_size=20\n", encoding="utf-8")
    with pytest.raises(SettingsError, match="unknown theme"): 
        load(bad)

def test_page_size_bounds(tmp_path): 
    bad = tmp_path / "catalog.ini"
    bad.write_text("[display]\ntheme=ink\npage_size=400\n", encoding="utf-8")
    with pytest.raises(SettingsError, match="outside 5-100"):
        load(bad)

def test_size_must_be_numeric(tmp_path): 
    bad = tmp_path / "catalog.ini"
    bad.write_text("[display]\ntheme=ink\npage_size=twenty\n", encoding="utf-8")
    with pytest.raises(SettingsError, match="whole number"):
        load(bad)
                      
