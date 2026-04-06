class DashboardPage:
    def __init__(self, page):
        self.page = page
        
    def go_to_dashboard(self, url):
        self.page.goto(url)
    
    def _is_cards_visible(self):
        cards_locator = self.page.locator(".kpi-section.ng-star-inserted")
        cards_locator.wait_for(state="visible")
        return cards_locator.is_visible()
    
    def _cards_parent(self):
        cards_parent = self.page.locator("div.kpi-section.ng-star-inserted")
        cards_parent.wait_for(state="visible")
        return cards_parent

    def _card_elements(self):
        return self._cards_parent().locator(":scope > div")

    def get_cards_count(self):
        return self._card_elements().count()

    def get_card_element(self, index):
        return self._card_elements().nth(index)
    
    def get_cards_title_text(self, index):
        card = self.get_card_element(index)
        card_title_locator = card.locator("div.kpi-details span").nth(0)
        card_title_locator.wait_for(state="visible")
        return card_title_locator.inner_text()
    
    def get_cards_inner_count(self, index):
        card = self.get_card_element(index)
        card_count_locator = card.locator("div.kpi-details span").nth(1)
        card_count_locator.wait_for(state="visible")
        return card_count_locator.inner_text()
