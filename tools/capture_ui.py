"""Optional visual QA using an installed Edge; not a runtime dependency."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / ".impeccable/review"


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        page.goto("http://localhost:8501")
        page.get_by_role("heading", name="Paneli", exact=True).wait_for()
        page.get_by_text("Zgjidh një seksion nga navigimi.", exact=False).wait_for()
        page.screenshot(path=str(OUTPUT / "dashboard.png"), full_page=True)
        page.locator('[data-testid="stSidebar"]').get_by_text("Latin Square", exact=True).click()
        page.get_by_role("button", name="Gjenero me IDDFS", exact=True).click()
        page.get_by_text("Zgjidhje e gjetur dhe e validuar", exact=True).wait_for()
        page.get_by_role("heading", name="Zgjidhja", exact=True).wait_for()
        page.get_by_role("button", name="Shkarko rezultatin dhe metrikat JSON", exact=True).wait_for()
        page.set_viewport_size({"width": 1440, "height": max(1000, page.locator('[data-testid="stMain"]').evaluate("e => e.scrollHeight") + 80)})
        page.screenshot(path=str(OUTPUT / "desktop.png"), full_page=True)
        print({"desktop": page.title(), "errors": page.locator('[data-testid="stException"]').count()})
        page.locator('[data-testid="stSidebar"]').get_by_text("Social Golfers", exact=True).click()
        page.get_by_text("Përgjigjja e provuar: 10 javë — dëshmia nga literatura", exact=True).click()
        page.get_by_role("button", name="Shkarko dëshminë dhe verifikimin JSON", exact=True).wait_for()
        page.get_by_role("button", name="Shkarko dëshminë dhe verifikimin JSON", exact=True).scroll_into_view_if_needed()
        page.locator('[data-testid="stMain"]').evaluate("e => e.scrollTop = 0")
        page.screenshot(path=str(OUTPUT / "certificate-desktop.png"), full_page=True, animations="disabled")
        page.close()
        page = browser.new_page(viewport={"width": 390, "height": 1800}, device_scale_factor=1)
        page.goto("http://localhost:8501")
        page.get_by_role("button", name="Expand sidebar", exact=True).click()
        page.locator('[data-testid="stSidebar"]').get_by_text("Latin Square", exact=True).click()
        page.get_by_role("button", name="Collapse sidebar", exact=True).click()
        page.wait_for_function("document.querySelector('[data-testid=stSidebar]').getBoundingClientRect().right <= 0")
        page.get_by_role("button", name="Gjenero me IDDFS", exact=True).click()
        page.get_by_role("button", name="Shkarko rezultatin dhe metrikat JSON", exact=True).wait_for()
        page.screenshot(path=str(OUTPUT / "mobile.png"), full_page=True)
        print({"mobile_width": 390, "document_width": page.evaluate("document.documentElement.scrollWidth")})
        page.get_by_role("button", name="Expand sidebar", exact=True).click()
        page.locator('[data-testid="stSidebar"]').get_by_text("Social Golfers", exact=True).click()
        page.get_by_role("button", name="Collapse sidebar", exact=True).click()
        page.wait_for_function("document.querySelector('[data-testid=stSidebar]').getBoundingClientRect().right <= 0")
        page.get_by_text("Përgjigjja e provuar: 10 javë — dëshmia nga literatura", exact=True).click()
        page.get_by_role("button", name="Shkarko dëshminë dhe verifikimin JSON", exact=True).wait_for()
        page.get_by_role("button", name="Shkarko dëshminë dhe verifikimin JSON", exact=True).scroll_into_view_if_needed()
        page.locator('[data-testid="stMain"]').evaluate("e => e.scrollTop = 0")
        page.set_viewport_size({"width": 390, "height": max(1800, page.locator('[data-testid="stMain"]').evaluate("e => e.scrollHeight") + 80)})
        page.screenshot(path=str(OUTPUT / "certificate-mobile.png"), full_page=True, animations="disabled")
        browser.close()


if __name__ == "__main__":
    main()
