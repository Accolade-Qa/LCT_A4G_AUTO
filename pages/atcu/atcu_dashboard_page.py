from pages.common_dashboard_page import DashboardPage
from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuDashboardPage(DashboardPage):
    def __init__(self, page):
        super().__init__(page)
        logger.info("AtcuDashboardPage initialized")

    def go_to_atcu_dashboard(self, url):
        logger.info("Navigating to ATCU device dashboard URL %s", url)
        try:
            self.page.goto(url)
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            logger.warning("page.goto direct navigation failed/timed out: %s. Trying header navbar navigation.", e)

        # Wait for loading spinner overlay to detach if present
        try:
            self.page.locator(".ngx-spinner-overlay").wait_for(state="detached", timeout=10000)
        except Exception:
            pass

        # If page is still not on dashboard or graph section is not visible, click navbar dropdown link
        if "device-dashboard" not in self.page.url or not self.page.locator(".graph-section, .graph-card").is_visible():
            logger.info("Using navbar navigation to switch to Device Dashboard")
            try:
                self.page.locator("a.dropdown-toggle:has-text('Dashboard')").first.click()
                self.page.locator("a:has-text('Device Dashboard')").first.click()
                self.page.wait_for_load_state("networkidle", timeout=10000)
            except Exception as nav_err:
                logger.error("Navbar navigation failed: %s", nav_err)

        # Wait for graph section or cards to be visible
        try:
            self.page.locator(".graph-section, .kpi-section, .graph-card").first.wait_for(state="visible", timeout=15000)
        except Exception as vis_err:
            logger.warning("Graph/KPI section visibility wait: %s", vis_err)

        current_url = self.page.url
        logger.info("Successfully navigated to ATCU dashboard. Current URL: %s", current_url)
        return current_url

    def click_state_wise_graph_card(self, graph_title="State Wise Details"):
        logger.info("Clicking graph card with title: %s", graph_title)
        try:
            self.page.locator(".graph-section, .graph-card").first.wait_for(state="visible", timeout=15000)
        except Exception:
            pass

        graph_locator = self.page.locator(
            f".graph-card:has-text('{graph_title}'), h3.graph-title:has-text('{graph_title}'), .graph-title:has-text('{graph_title}')"
        ).first
        graph_locator.wait_for(state="visible", timeout=15000)
        graph_locator.scroll_into_view_if_needed()
        graph_locator.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)
        logger.info("Successfully clicked graph card: %s", graph_title)

    def get_state_wise_table_title(self):
        logger.info("Retrieving component table title after graph card click")
        title_locator = self.page.locator(".component-title").first
        title_locator.wait_for(state="visible", timeout=10000)
        title = title_locator.inner_text().strip()
        logger.info("Component table title: %s", title)
        return title

    def search_imei_in_state_wise_table(self, imei):
        logger.info("Searching State Wise Details table for IMEI: %s", imei)
        try:
            search_input = self.page.locator(
                "input[formcontrolname='searchInput'], input[placeholder*='Search'], .search-bar input"
            ).first
            search_input.wait_for(state="visible", timeout=10000)
            search_input.fill(str(imei))
            search_input.press("Enter")
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            logger.warning("Direct search input fill fallback to SearchHelper: %s", e)
            self.search_helper.run_search(str(imei))

    def is_imei_present_in_state_wise_table(self, imei, timeout=10000):
        logger.info("Checking if IMEI '%s' is present in State Wise Details table", imei)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{imei}')]]")
            row_locator.wait_for(state="visible", timeout=timeout)
            is_vis = row_locator.is_visible()
            logger.info("IMEI '%s' present in table: %s", imei, is_vis)
            return is_vis
        except Exception as e:
            logger.warning("IMEI '%s' not found in table within %s ms: %s", imei, timeout, e)
            return False

    def get_imei_row_state_details(self, imei):
        logger.info("Getting row details for IMEI '%s'", imei)
        try:
            headers = [th.inner_text().strip() for th in self.page.locator("table thead th").all()]
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{imei}')]]").first
            cells = [td.inner_text().strip() for td in row_locator.locator("td").all()]
            row_dict = dict(zip(headers, cells)) if headers else cells
            logger.info("Row details for IMEI '%s': %s", imei, row_dict)
            return row_dict
        except Exception as e:
            logger.error("Failed to get row details for IMEI '%s': %s", imei, e)
            return {}
