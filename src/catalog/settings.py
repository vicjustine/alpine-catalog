""" Catalog display settings, loaded from catalog.ini and validated on load """

from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path

THEMES = {"paper", "ink", "contrast"}
MIN_PAGE, MAX_PAGE = 5, 100

class SettingsError(ValueError):
    """Raised when catalog.ini carries a value the catalog cannot honour. """

@dataclass(frozen=True)
class Settings: 
    theme: str
    page_size: int

    @property
    def pages_for(self) -> int: 
        return self.page_size

    def page_count(self, items: int) -> int: 
        if items < 0:
            raise SettingsError(f"negative item count: {items}")
        return -(-items // self.page_size)

def load (path: str | Path = "catalog.ini") -> Settings: 
    parser = configparser.ConfigParser()
    read = parser.read(path, encoding="utf-8")
    if not read: 
        raise SettingsError(f"no settings file at {path}")

    if "display" not in parser: 
        raise SettingsError("catalog.ini has no [display] section")
      
    theme = parser["display"].get("theme", "").strip()
    if theme not in THEMES: 
        raise SettingsError(f"unknown theme {theme!r}, expected one of {sorted(THEMES)}")

    raw = parser ["display"].get("page_size", "").strip()
    if not raw.isdigit():
        raise SettingsError(f"page_size must be a whole number, got {raw!r}")

    page_size = int(raw)
    if not MIN_PAGE <= page_size <= MAX_PAGE: 
        raise SettingsError(f"page_size {page_size} outside {MIN_PAGE}-{MAX_PAGE}")
      
    return Settings(theme=theme, page_size=page_size)
