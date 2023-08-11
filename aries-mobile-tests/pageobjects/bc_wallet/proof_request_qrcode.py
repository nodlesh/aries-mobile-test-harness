import base64
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class ProofRequestQRCodePage(BasePage):
    """Proof Request QRCode page object"""

    # Locators
    qrcode_locator = (AppiumBy.ID, "com.ariesbifold:id/QRCode")

    def on_this_page(self):
        return super().on_this_page(self.qrcode_locator)

    def get_qr_code_image(self):
        if self.on_this_page():
            # use appium driver to get the screenshot of the QR code
            return self.driver.get_screenshot_as_base64()
            # qrcode = base64.b64encode(open("mobile_verifier_qr_code.png", "rb").read())
            # qrcode = base64.b64encode(open("qrcode.png", "rb").read())
            # return qrcode.decode('utf-8')
        else:
            raise Exception(f"App not on the {type(self)} page")