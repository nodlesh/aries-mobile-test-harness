import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.use_this_proof_request import UseThisProofRequestPage


# These classes can inherit from a BasePage to do common setup and functions
class ChooseAProofRequestPage(BasePage):
    """Choose a Proof Request page object"""

    # Locators
    proof_request_locator = (AppiumBy.ACCESSIBILITY_ID, "Credentials")

    # this is the one that contains all the text for that particular credential
    proof_request_locator = (AppiumBy.ID, "com.ariesbifold:id/ProofRequestCard")

    def on_this_page(self):
        return super().on_this_page(self.proof_request_locator)

    def select_proof_request(self, proof_name):
        if self.on_this_page():
            self.find_multiple_by(self.proof_request_locator)
            # iterate through the list of proof requests and find the one that matches the proof_name
            for proof in self.find_multiple_by(self.proof_request_locator):
                if proof_name in proof.text:
                    proof.click()
            return UseThisProofRequestPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def proof_request_exists(self, proof_name):
        return proof_name in self.driver.page_source