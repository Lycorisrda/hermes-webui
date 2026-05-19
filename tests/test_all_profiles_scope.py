from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (REPO / path).read_text(encoding="utf-8")


def test_all_profiles_scope_is_persistent_and_fetches_aggregate_lists():
    sessions_js = read("static/sessions.js")
    assert "PROFILE_SCOPE_KEY = 'hermes-profile-scope'" in sessions_js
    assert "localStorage.getItem(PROFILE_SCOPE_KEY) === 'all'" in sessions_js
    assert "function setProfileScopeAll(enabled" in sessions_js
    assert "_showAllProfiles ? '?all_profiles=1' : ''" in sessions_js
    assert "api('/api/sessions' + allProfilesQS)" in sessions_js
    assert "api('/api/projects' + allProfilesQS)" in sessions_js


def test_titlebar_profile_menu_has_all_profiles_without_profile_switch():
    panels_js = read("static/panels.js")
    start = panels_js.index("const allOpt=document.createElement('div');")
    end = panels_js.index("for (const p of profiles) {", start)
    all_opt = panels_js[start:end]
    assert "All profiles" in all_opt
    assert "setProfileScopeAll(true)" in all_opt
    assert "/api/profile/switch" not in all_opt


def test_all_profiles_rows_show_profile_badge_even_in_compact_sidebar():
    sessions_js = read("static/sessions.js")
    assert "session-profile-badge" in sessions_js
    assert "if(_showAllProfiles&&s.profile)" in sessions_js
    style_css = read("static/style.css")
    assert ".session-profile-badge" in style_css


def test_sync_topbar_preserves_all_profiles_chip_label():
    ui_js = read("static/ui.js")
    boot_js = read("static/boot.js")
    assert "syncProfileChipLabel()" in ui_js
    assert "syncProfileChipLabel()" in boot_js
