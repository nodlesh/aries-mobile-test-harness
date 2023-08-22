import time
import datetime
import base64
import json
import io
from qrcode import QRCode
from PIL import Image
from pyzbar.pyzbar import decode
from collections import defaultdict

# This code is responsible for generating a QR code from the invitation url
# and returning a base64 encoded string of the image.

# get_qr_code_from_invitation
# invitation_json: json object containing an invitation url
# print_qr_code: boolean, print the qr code to the console
# save_qr_code: boolean, save the qr code to a file
# qr_code_border: int, border size of the qr code
# returns: base64 encoded string of the qr code image
def get_qr_code_from_invitation(invitation_json, print_qr_code=False, save_qr_code=False, qr_code_border=40):
    if "invitation_url" in invitation_json:
        invite_url_key = "invitation_url"
    elif "invitationUrl" in invitation_json:
        invite_url_key = "invitationUrl"
    else:
        raise Exception(
            f"Could not find an invitation url in invitation json {invitation_json}")
    invitation_url = invitation_json[invite_url_key]

    qr = QRCode(border=qr_code_border)
    qr.add_data(invitation_url)
    qr.make()
    #img = qr.make_image(fill_color="red", back_color="#23dda0")
    img = qr.make_image()
    if save_qr_code:
        img.save('./qrcode.png')
    if print_qr_code:
        qr.print_ascii(invert=True)

    with io.BytesIO() as output:
        img.save(output, format="PNG")
        contents = base64.b64encode(output.getvalue())

    return contents.decode('utf-8')
    
def get_invite_url_from_qrcode(qrcode_image) -> str:
    """Extracts the invite url from the qrcode image"""
    # qr = QRCode()
    # qr.add_data(qrcode)
    # qr.make()
    # return qr.data_list[0].data.decode('utf-8')
    if isinstance(qrcode_image, str):
        # Decode base64 and create a PIL image
        image_data = base64.b64decode(qrcode_image)
        qrcode_image = Image.open(io.BytesIO(image_data))

    decoded_objects = decode(qrcode_image)

    if decoded_objects:
        data = decoded_objects[0].data.decode('utf-8')
        return data

    return ""

def create_non_revoke_interval(timeframe):
    # timeframe containes two variables, the To and from of the non-revoked to and from parameters in the send presentation request message
    # The to and from timeframe variables are always relative to now. 
    # The to and from time is represented as a total number of seconds from Unix Epoch
    # Deconstruct the timeframe and add it to the context to be used in the request later.
    # putting timefrom here where the revoke happens just in case it is needed. It may not and could be removed from here and added to the request step.
    #
    # Timeframe examples:
    # -86400:+86400
    # now:now
    # -86400:0
    # :now (openended from)
    # now: (openended to)

    timeframe_list = timeframe.split(":")
    from_reference = timeframe_list[0]
    to_reference = timeframe_list[1]

    if (from_reference == 'now') or (from_reference == ''):
        if from_reference == 'now': from_interval = int(time.time())
        if from_reference == '': from_interval = None
        #from_interval = from_reference
    else:
        from_interval = int(from_reference) + int(time.time())

    if (to_reference == 'now') or (to_reference == ''):
        if to_reference == 'now': to_reference = int(time.time())
        to_interval = to_reference
    else:
        to_interval = int(to_reference) + int(time.time())

    return {
        "non_revoked": {
            "from": from_interval,
            "to": to_interval
        }
    }

def get_relative_timestamp_to_epoch(timestamp):
    # timestamps are always relative to now. + or - is represented in seconds from Unix Epoch.
    # Valid timestsamps are 
    #  now
    #  +###### ie +86400
    #  -###### ie -86400

    if (timestamp == 'now'):
        epoch_time = int(time.time())
    else:
        epoch_time = int(timestamp) + int(time.time())

    return epoch_time

def format_cred_proposal_by_aip_version(context, aip_version, cred_data, connection_id, filters=None):

    if aip_version == "AIP20":

        filters = amend_filters_with_runtime_data(context, filters)

        # credential_proposal = {
        #     "connection_id": connection_id,
        #     "credential_preview": {
        #         "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
        #         "attributes": cred_data,
        #     },
        #     "filter": filters
        # }
        credential_proposal = {
            "connection_id": connection_id,
            "credential_preview": {
                "@type": "issue-credential/2.0/credential-preview",
                "attributes": cred_data,
            },
            "filter": filters
        }

    return credential_proposal

def amend_filters_with_runtime_data(context, filters):
    # This method will need comdification as new types of filters are used. Intially "indy" is used.
    if "indy" in filters:
        if "schema_issuer_did" in filters["indy"] and filters["indy"]["schema_issuer_did"] == "replace_me":
            filters["indy"]["schema_issuer_did"] = context.issuer_did_dict[context.schema['schema_name']]
        if "issuer_did" in filters["indy"] and filters["indy"]["issuer_did"] == "replace_me":
            filters["indy"]["issuer_did"] = context.issuer_did_dict[context.schema['schema_name']]
        if "cred_def_id" in filters["indy"] and filters["indy"]["cred_def_id"] == "replace_me":
            filters["indy"]["cred_def_id"] = context.issuer_credential_definition_dict[context.schema['schema_name']]["id"]
        if "schema_id" in filters["indy"] and filters["indy"]["schema_id"] == "replace_me":
            filters["indy"]["schema_id"] = context.issuer_schema_dict[context.schema['schema_name']]["id"]

    if "json-ld" in filters:
        json_ld = filters.get("json-ld")
        credential = json_ld.get("credential")
        options = json_ld.get("options")

        issuer = context.issuer_did_dict[context.schema['schema_name']]

        if "issuer" in credential:
            # "issuer": "replace_me"
            if credential.get("issuer") == "replace_me":
                credential["issuer"] = issuer
            # "issuer": { "id": "replace_me" }
            elif credential.get("issuer", {}).get("id") == "replace_me":
                credential["issuer"]["id"] = issuer
        if options.get("proofType") == "replace_me":
            options["proofType"] = context.proof_type
        if "issuanceDate" in credential:
            created_datetime = str(datetime.datetime.now().replace(microsecond=0).isoformat(timespec='seconds'))  + "Z"
            credential["issuanceDate"] = created_datetime


    return filters

def amend_presentation_definition_with_runtime_data(context, presentation_definition):
    # presentation definition is outer object with presentation definition and options
    pd = presentation_definition.get("presentation_definition", {})
    format = pd.get("format", {})
    ldp_vp_proof_type = format.get("ldp_vp", {}).get("proof_type", [])

    # Only ldp_vp with a single proof type replaced is supported ATM
    if "replace_me" in ldp_vp_proof_type:
        index = ldp_vp_proof_type.index("replace_me")
        ldp_vp_proof_type[index] = context.proof_type

        presentation_definition["presentation_definition"]["format"]["ldp_vp"]["proof_type"] = ldp_vp_proof_type

    return presentation_definition

def table_to_str(table):
    result = ''
    if table.headings:
        result = '|'
    for heading in table.headings:
        result += heading + '|'
    result += '\n'
    for row in table.rows:
        if row.cells:
            result += '|'
        for cell in row.cells:
            result += cell + '|'
        result += '\n'
    return result

def set_current_page_object_context(context, user=None):
    if user:
        return context.multi_device_page_objects[user]
    else:
        return context
    
# Custom dictionary class with nested attribute-style access
# class NestedAttributeDict(dict):
#     def __getattr__(self, attr):
#         if attr in self:
#             return self[attr]
#         else:
#             sub_dict = NestedAttributeDict()
#             self[attr] = sub_dict
#             return sub_dict

#     def __getitem__(self, item):
#         if item in self:
#             return self[item]
#         else:
#             sub_dict = NestedAttributeDict()
#             self[item] = sub_dict
#             return sub_dict
        
class NestedAttributeDict(defaultdict):
    def __init__(self):
        super().__init__(NestedAttributeDict)
        
    def __getattr__(self, attr):
        return self[attr]