# -----------------------------------------------------------
# Behave Step Definitions for a Mobile Verifier and wallet to wallet proofs
#
# -----------------------------------------------------------

from behave import given, when, then
import os, json
from decouple import config
#from behave import step
from behave.api.async_step import async_run_until_complete
import threading

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation, table_to_str, create_non_revoke_interval
from device_service_handler.device_service_handler_factory import DeviceServiceHandlerFactory


# @step("{n} wallet users")
# @async_run_until_complete
# async def step_impl(context, n):
#     """Determine the roles each user is playing and the device they are set to, then start appium drivers for each"""

#     # Create a dictionary that will be indexed on role and give the device_service_handler apropriate for the device set
#     context.multi_device_service_handlers = {}
#     tasks = []

#     for row in context.table:
#         if row["role"] == "holder":
#             if row["device"] == "default" and row["device_handler"] == "existing":
#                 #await setup_holder(context)
#                 tasks.append(asyncio.create_task(setup_holder(context)))
#                 #context.multi_device_service_handlers[row["role"]] = context.device_service_handler
#             elif row["device"] == "opposite":
#                 # pass for now
#                 # TODO add the creation of a new device service handler for the opposite device
#                 pass

#         elif row["role"] == "verifier" and row["device_handler"] == "new":
#             if row["device"] == "default":
#                 # start a device service handler the same as the default device handler
#                 #await setup_verifier(context)
#                 tasks.append(asyncio.create_task(setup_verifier(context)))
#                 # # Get the Device Cloud Service passed in from manage
#                 # device_cloud_service = config('DEVICE_CLOUD')
#                 # os.environ['SAUCE_USERNAME'] = 'oauth-shel2cventures-1c214'
#                 # os.environ['SAUCE_ACCESS_KEY'] = 'd9badc39-f746-4f9d-9358-da6a5ec38aa7'

#                 # # get the dafault config filed
#                 # config_file_path = os.path.join(os.getcwd(), "config.json")

#                 # # Create the Device Service Handler requested 
#                 # dcshf = DeviceServiceHandlerFactory()
#                 # device_service_handler = dcshf.create_device_service_handler(device_cloud_service, config_file_path)

#                 # context.multi_device_service_handlers[row["role"]] = device_service_handler

#                 # extra_desired_capabilities = {
#                 #     'name': context.scenario.name
#                 # }
#                 # context.multi_device_service_handlers[row["role"]].set_desired_capabilities(extra_desired_capabilities)

#                 # context.multi_device_service_handlers[row["role"]].initialize_driver()

#                 # print("\nActual Capabilities used by Appium:")
#                 # print(json.dumps(context.multi_device_service_handlers[row["role"]]._driver.capabilities,indent=4))

#             elif row["device"] == "opposite":
#                 # pass for now
#                 # TODO add the creation of a new device service handler for the opposite device
#                 # start a device service handler the same as the default device handler

#                 # # Get the Device Cloud Service passed in from manage
#                 # device_cloud_service = config('DEVICE_CLOUD')

#                 # # Check if there is a config file override. If not, use the default
#                 # try: 
#                 #     config_file_path = config('CONFIG_FILE_OVERRIDE')
#                 # except:
#                 #     config_file_path = os.path.join(os.path.dirname(__file__), '..', "config.json")
#                 # # Create the Device Service Handler requested 
#                 # dcshf = DeviceServiceHandlerFactory()
#                 # device_service_handler = dcshf.create_device_service_handler(device_cloud_service, config_file_path)
#                 pass

#         else:
#             role = row["role"]
#             print(
#                 f"Data table in step contains an unrecognized role '{role}', must be holder or verifier"
#             )
#     await asyncio.gather(*tasks)

#     # # Onboard each user to the app
#     # context.execute_steps(f'''
#     #     Given the Holder has setup thier wallet
#     # ''')

#     # # swap Drivers for the steps to execute on the other wallet
#     # context.driver = context.multi_device_service_handlers["verifier"]._driver

#     # context.execute_steps(f'''
#     #     Given the Holder has setup thier wallet
#     # ''')


#     # # Onboard each user to the app
#     # context.execute_steps(f'''
#     #     Given the Holder has setup thier wallet
#     # ''')

#     # # swap Drivers for the steps to execute on the other wallet
#     # context.driver = context.multi_device_service_handlers["verifier"]._driver

#     # context.execute_steps(f'''
#     #     Given the Holder has setup thier wallet
#     # ''')

#     # # swap Drivers for the steps to execute on the other wallet
#     # context.driver = context.multi_device_service_handlers["holder"]._driver

#     # context.execute_steps(f'''
#     #     And the Holder has selected not to use biometrics to unlock BC Wallet
#     # ''')

#     # # swap Drivers for the steps to execute on the other wallet
#     # context.driver = context.multi_device_service_handlers["verifier"]._driver

#     # context.execute_steps(f'''
#     #     And the Holder has selected not to use biometrics to unlock BC Wallet
#     # ''')

# # @given('the {role} has a {credential} credential')
# # def step_given_holder_credential(context, role, credential):
# #     # Code to assign the specified credential to the holder
# #     pass

# async def setup_holder(context):
#     context.multi_device_service_handlers["holder"] = context.device_service_handler

#     context.driver = context.multi_device_service_handlers["holder"]._driver
#     # #context.execute_steps
#     # await context.async_execute_steps(f'''
#     #     Given the Holder has setup thier wallet
#     #     And the Holder has selected not to use biometrics to unlock BC Wallet
#     # ''')
#     context.execute_steps(f'''
#         Given the User has skipped on-boarding
#         And the User has accepted the Terms and Conditions
#         And a PIN has been set up with "369369"
#     ''')
#     context.execute_steps(f'''
#         Given the new user has opened the app for the first time
#         Given the user is on the onboarding Welcome screen
#         When the user selects Skip
#     ''')
#         context.execute_steps(f'''
#         Given the User is on the Terms and Conditions screen
#         And the users accepts the Terms and Conditions
#         And the user clicks continue
#     ''')
#         context.execute_steps(f'''
#         Given the User is on the PIN creation screen
#         When the User enters the first PIN as "{pin}"
#         And the User re-enters the PIN as "{pin}"
#         And the User selects Create PIN
#     ''')

# async def setup_verifier(context):
#     # Get the Device Cloud Service passed in from manage
#     device_cloud_service = config('DEVICE_CLOUD')
#     os.environ['SAUCE_USERNAME'] = 'oauth-shel2cventures-1c214'
#     os.environ['SAUCE_ACCESS_KEY'] = 'd9badc39-f746-4f9d-9358-da6a5ec38aa7'

#     # get the dafault config filed
#     config_file_path = os.path.join(os.getcwd(), "config.json")

#     # Create the Device Service Handler requested 
#     dcshf = DeviceServiceHandlerFactory()
#     device_service_handler = dcshf.create_device_service_handler(device_cloud_service, config_file_path)

#     context.multi_device_service_handlers["verifier"] = device_service_handler

#     extra_desired_capabilities = {
#         'name': context.scenario.name
#     }
#     context.multi_device_service_handlers["verifier"].set_desired_capabilities(extra_desired_capabilities)

#     context.multi_device_service_handlers["verifier"].initialize_driver()

#     print("\nActual Capabilities used by Appium:")
#     print(json.dumps(context.multi_device_service_handlers["verifier"]._driver.capabilities,indent=4))

#     context.driver = context.multi_device_service_handlers["verifier"]._driver
#     #context.execute_steps
#     # await context.async_execute_steps(f'''
#     #     Given the Holder has setup thier wallet
#     #     And the Holder has selected not to use biometrics to unlock BC Wallet
#     # ''')



# async def the_new_user_has_opened_the_app_for_the_first_time(context):
#     # App opened already buy appium. 
#     # Intialize the page we should be on
#     context.thisOnboardingWelcomePage = OnboardingWelcomePage(context.driver)



@given("{n} wallet users")
def step_impl(context, n):
    """Determine the roles each user is playing and the device they are set to, then start appium drivers for each"""

    # Create a dictionary that will be indexed on role and give the device_service_handler apropriate for the device set
    context.multi_device_service_handlers = {}
    holder_thread = threading.Thread(target=setup_holder, args=(context,))
    verifier_thread = threading.Thread(target=setup_verifier, args=(context,))

    for row in context.table:
        if row["role"] == "holder":
            if row["device"] == "default" and row["device_handler"] == "existing":
                holder_thread.start()
            elif row["device"] == "opposite":
                # pass for now
                # TODO add the creation of a new device service handler for the opposite device
                pass

        elif row["role"] == "verifier" and row["device_handler"] == "new":
            if row["device"] == "default":
                # start a device service handler the same as the default device handler
                verifier_thread.start()

            elif row["device"] == "opposite":
                # pass for now
                # TODO add the creation of a new device service handler for the opposite device
                pass

        else:
            role = row["role"]
            print(
                f"Data table in step contains an unrecognized role '{role}', must be holder or verifier"
            )
    holder_thread.join()
    verifier_thread.join()


def setup_holder(context):
    context.multi_device_service_handlers["holder"] = context.device_service_handler

    context.driver = context.multi_device_service_handlers["holder"]._driver
    context.execute_steps(f'''
        Given the Holder has setup thier wallet
        And the Holder has selected not to use biometrics to unlock BC Wallet
    ''')

def setup_verifier(context):
    # Get the Device Cloud Service passed in from manage
    device_cloud_service = config('DEVICE_CLOUD')
    os.environ['SAUCE_USERNAME'] = 'oauth-shel2cventures-1c214'
    os.environ['SAUCE_ACCESS_KEY'] = 'd9badc39-f746-4f9d-9358-da6a5ec38aa7'

    # get the dafault config filed
    config_file_path = os.path.join(os.getcwd(), "config.json")

    # Create the Device Service Handler requested 
    dcshf = DeviceServiceHandlerFactory()
    device_service_handler = dcshf.create_device_service_handler(device_cloud_service, config_file_path)

    context.multi_device_service_handlers["verifier"] = device_service_handler

    extra_desired_capabilities = {
        'name': context.scenario.name
    }
    context.multi_device_service_handlers["verifier"].set_desired_capabilities(extra_desired_capabilities)

    context.multi_device_service_handlers["verifier"].initialize_driver()

    print("\nActual Capabilities used by Appium:")
    print(json.dumps(context.multi_device_service_handlers["verifier"]._driver.capabilities,indent=4))

    context.driver = context.multi_device_service_handlers["verifier"]._driver
    context.execute_steps(f'''
        Given the Holder has setup thier wallet
        And the Holder has selected not to use biometrics to unlock BC Wallet
    ''')



@given('the verifier wants to prove that the holder {proof}')
def step_given_verifier_proof(context, proof):
    # Code to set the proof information for the verifier
    pass

@when('the holder scans the QR Code from the Verifier')
def step_when_holder_scans_QR_code(context):
    # Code for the holder to scan the QR Code
    pass

@when('the holder receives the proof request')
def step_when_holder_receives_proof_request(context):
    # Code for the holder to receive the proof request
    pass

@when('the holder shares the information')
def step_when_holder_shares_information(context):
    # Code for the holder to share the information
    pass

@then('the holder is informed that the information sent successfully')
def step_then_holder_informed_success(context):
    # Code to verify that the holder is informed about successful information sending
    pass

@then('the verifier receives the information')
def step_then_verifier_receives_information(context):
    # Code to verify that the verifier receives the information
    pass

@then('the verifier reviews details of the information')
def step_then_verifier_sees_details(context):
    # Code to verify that the verifier can see the details of the information
    pass