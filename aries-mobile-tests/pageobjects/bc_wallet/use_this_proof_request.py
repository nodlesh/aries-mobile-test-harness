import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.proof_request_qrcode import ProofRequestQRCodePage


# These classes can inherit from a BasePage to do common setup and functions
class UseThisProofRequestPage(BasePage):
    """Use This Proof Request page object"""

    # Locators
    use_this_proof_request_locator = (AppiumBy.ID, "com.ariesbifold:id/UseThisProofRequest")

    def on_this_page(self):
        return super().on_this_page(self.use_this_proof_request_locator)

    def select_use_this_proof_request(self):
        if self.on_this_page():
            self.find_by(self.use_this_proof_request_locator).click()
            return ProofRequestQRCodePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")