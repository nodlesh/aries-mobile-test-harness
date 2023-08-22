"""
Absctact Base Class for actual issuer agent interfaces to implement
"""

from abc import ABC, abstractmethod

class HolderAgentInterface(ABC):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    @abstractmethod
    def get_issuer_type(self) -> str:
        """Return the type of holder you are ie 'AATHHolder' or a possible web based wallet holder"""

    @abstractmethod
    def accept_invitation(self, qrcode: str = None, invite_url: str = None):
        """Accept an invitation from an issuer or verifier in the format of a QR code or a URL"""


    @abstractmethod
    def connected(self) -> bool:
        """Return True/False indicating if this holder is connected to the issuer or verifier """

    @abstractmethod
    def accept_credential(self):
        """Accept a credential offer from an issuer """

    @abstractmethod
    def accept_proof(self):
        """Accept a proof request from a verifier """
