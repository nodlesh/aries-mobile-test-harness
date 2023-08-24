"""
Class for actual AATH holder agent
"""


from agent_factory.holder_agent_interface import HolderAgentInterface
from agent_factory.aath.aath_agent_interface import AATHAgentInterface
import json
import base64
import urllib.parse
from agent_test_utils import get_qr_code_from_invitation, get_invite_url_from_qrcode
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from random import randint

class AATHHolderAgentInterface(HolderAgentInterface, AATHAgentInterface):

    _my_public_did: str

    def __init__(self, endpoint):
        self._my_public_did = None
        super().__init__(endpoint)

    def get_issuer_type(self) -> str:
        """return the type of holder as a string AATHHolder"""
        return "AATHHolder"
        

    def connected(self):
        return self.connected_util()


    def accept_invitation(self, qrcode: str = None, invite_url: str = None):
        """Accept an invitation from an issuer or verifier in the format of a QR code or a URL"""
        # if a qrcode then decode the qrcode to get the invitation url
        if qrcode is not None:
            invite_url = get_invite_url_from_qrcode(qrcode)
        # if no invite_url then error
        if invite_url is None:
            raise Exception("No invite url or QR code provided")

        #data = {"serviceEndpoint": invite_url}
        # data will equal the decoded base64 invite url. Everything in the Url past the ?c_i= will be the data after decode.
        # Parse the URL to extract the query parameters
        url_parts = urllib.parse.urlparse(invite_url)
        query_params = urllib.parse.parse_qs(url_parts.query)
        encoded_data = query_params.get('c_i', [''])[0]

        # Decoding the Base64 URL encoded data
        decoded_data = base64.urlsafe_b64decode(encoded_data + '=' * (4 - len(encoded_data) % 4))

        # Convert bytes to string
        data = decoded_data.decode('utf-8')

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/agent/command/",
            "connection",
            operation="receive-invitation",
            data=data,
        )
        if resp_status != 200:
            raise Exception(
                f"Call to accept invitation failed: {resp_status}; {resp_text}"
            )
        else:
            self.invitation_json = json.loads(resp_text)
            self.connection_id = self.invitation_json["connection_id"]
  


    def accept_credential(self):
        """Accept a credential offer from an issuer """


    def accept_proof(self):
        """Accept a proof request from a verifier """


    def send_credential(self, version=1, schema=None, credential_offer=None, revokable=False):
        """send a credential to the holder"""

        if version == 2:
            topic = "issue-credential-v2"
            type = "issue-credential/2.0/credential-preview"
        else:
            topic = "issue-credential"
            type = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview"

        # How is the schema and cred def setup? Should be done here in the agent interface. Need to check if it exists first
        if self._my_public_did is None:
            self._get_public_did()
        if schema is None:
            self._schema = self.DEFAULT_SCHEMA_TEMPLATE.copy()
        else:
            self._schema = schema
        # Check for an existing schema. If it doesn't exist create it.
        if self._schema.get("schema_id") is None:
            self._create_schema(self._schema)
        # Check for an existing credential definition. If it doesn't exist create it.
        if self._credential_definition is None or self._credential_definition.get("credential_definition_id") is None or self._credential_definition.get("schema_id") != self._schema.get("schema_id"):
            if schema is None:
                self._credential_definition = self.DEFAULT_CRED_DEF_TEMPLATE.copy()
            else:
                # self._credential_definition = {
                #     "schema_id": self._schema["schema_id"],
                #     "tag": str(randint(1, 10000)),
                # }
                self._credential_definition = {
                    "schema_id": self._schema["schema_id"],
                    "tag": self._schema["schema_name"],
                }
            self._create_credential_definition(
                self._credential_definition, revokable)

        # if data is none, use a default cred
        # if data is not none then use it as the cred
        if credential_offer:
            cred_data = credential_offer["attributes"] 
        else:
            cred_data = self.DEFAULT_CREDENTIAL_ATTR_TEMPLATE.copy()

        cred_offer = {
            "cred_def_id": self._credential_definition["credential_definition_id"],
            "credential_preview": {
                "@type": type,
                "attributes": cred_data,
            },
            "connection_id": self.invitation_json['connection_id'],
        }

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/agent/command/",
            topic,
            operation="send-offer",
            data=cred_offer,
        )
        if resp_status != 200:
            raise Exception(
                f"Call to send credential failed: {resp_status}; {resp_text}"
            )
        else:
            self.credential_json = json.loads(resp_text)
            # also add it to the credential json dict just in case we the tests are using multiple credentials
            self._credential_json_dict[self._credential_definition["tag"]] = self.credential_json



    def _get_public_did(self):
        (resp_status, resp_text) = agent_controller_GET(
            self.endpoint + "/agent/command/", "did"
        )
        if resp_status != 200:
            raise Exception(
                f"Call to get issuer public did failed: {resp_status}; {resp_text}"
            )
        else:
            resp_json = json.loads(resp_text)
            self._my_public_did = resp_json["did"]

