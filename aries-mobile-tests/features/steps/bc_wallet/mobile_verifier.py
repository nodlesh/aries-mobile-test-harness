# -----------------------------------------------------------
# Behave Step Definitions for a Mobile Verifier and wallet to wallet proofs
#
# -----------------------------------------------------------

import copy
import logging
from behave import given, when, then, step
import os, json
from decouple import config
#from behave import step
from behave.api.async_step import async_run_until_complete
import threading
from types import SimpleNamespace

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation, table_to_str, create_non_revoke_interval, NestedAttributeDict, set_current_page_object_context
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
    context.multi_device_threads = {}
    #holder_thread = threading.Thread(target=setup_holder, args=(context,))
    #verifier_thread = threading.Thread(target=setup_verifier, args=(context,))

    # Create a dictionary that will be indexed on role and give the page object apropriate for the device set
    # Create an instance of the custom dictionary
    custom_page_object_dict = NestedAttributeDict()
    # Assign the custom dictionary to the context object
    context.multi_device_page_objects = custom_page_object_dict

    for row in context.table:
        if row["role"] == "holder":
            if row["device"] == "default" and row["device_handler"] == "existing":
                context.multi_device_threads[row["role"]] = threading.Thread(target=setup_holder, args=(context, row["role"]))
                #holder_thread = threading.Thread(target=setup_holder, args=(context, row["role"]))
                #holder_thread.start()
                context.multi_device_threads[row["role"]].start()
            elif row["device"] == "opposite":
                # pass for now
                # TODO add the creation of a new device service handler for the opposite device
                pass

        elif row["role"] == "verifier":
            if row["device"] == "default":
                # start a device service handler the same as the default device handler
                context.multi_device_threads[row["role"]] = threading.Thread(target=setup_verifier, args=(context, row["role"], row["device_handler"]))
                context.multi_device_threads[row["role"]].start()
                #verifier_thread = threading.Thread(target=setup_verifier, args=(context, row["role"]))
                #verifier_thread.start()

            elif row["device"] == "opposite":
                # pass for now
                # TODO add the creation of a new device service handler for the opposite device
                pass

        else:
            role = row["role"]
            logging.ERROR(
                f"Data table in step contains an unrecognized role '{role}', must be holder or verifier"
            )
    # holder_thread.join()
    # verifier_thread.join()
    #context.multi_device_threads["holder"].join()
    #context.multi_device_threads["verifier"].join()
    



def setup_holder(context, holder_name, device_handler="existing"):
    context.multi_device_service_handlers[holder_name] = context.device_service_handler

    context.multi_device_page_objects[holder_name] = SimpleNamespace()
    context.execute_steps(f'''
        Given the "{holder_name}" has setup thier wallet
        And the "{holder_name}" has selected not to use biometrics to unlock BC Wallet
    ''')


def setup_verifier(context, verifier_name, device_handler="new"):
    if device_handler == "new":
        # Get the Device Cloud Service passed in from manage
        device_cloud_service = config('DEVICE_CLOUD')
        os.environ['SAUCE_USERNAME'] = 'oauth-shel2cventures-1c214'
        os.environ['SAUCE_ACCESS_KEY'] = 'd9badc39-f746-4f9d-9358-da6a5ec38aa7'

        # get the dafault config filed
        config_file_path = os.path.join(os.getcwd(), "config.json")

        # Create the Device Service Handler requested 
        dcshf = DeviceServiceHandlerFactory()
        device_service_handler = dcshf.create_device_service_handler(device_cloud_service, config_file_path)

        context.multi_device_service_handlers[verifier_name] = device_service_handler

        extra_desired_capabilities = {
            'name': context.scenario.name
        }
        context.multi_device_service_handlers[verifier_name].set_desired_capabilities(extra_desired_capabilities)

        context.multi_device_service_handlers[verifier_name].initialize_driver()

        print("\nActual Capabilities used by Appium:")
        print(json.dumps(context.multi_device_service_handlers[verifier_name]._driver.capabilities,indent=4))
    else:
        context.multi_device_service_handlers[verifier_name] = context.device_service_handler

    context.multi_device_page_objects[verifier_name] = SimpleNamespace()

    context.execute_steps(f'''
        Given the "{verifier_name}" has setup thier wallet
        And the "{verifier_name}" has selected not to use biometrics to unlock BC Wallet
    ''')

@step('a verifier wallet user wants to do a proof request')
def step_impl(context):
    context.execute_steps(f'''
        Given the user has setup thier wallet
        And the user has selected not to use biometrics to unlock BC Wallet
        Given the user has use Verifier capability turned on in dev options
    ''')

@step('the "{holder}" has credentials and the "{verifier}" wants to prove that the holder {proof_name}')
def step_the_user_has_a_credential(context, holder, verifier, proof_name):
    table = copy.deepcopy(context.table)
    # context.multi_device_threads[holder].join()
    # context.multi_device_threads[holder] = threading.Thread(target=the_user_has_a_credential, args=(context, holder, table))
    # context.multi_device_threads[holder].start()

    context.multi_device_threads[verifier].join()
    context.multi_device_threads[verifier] = threading.Thread(target=given_verifier_proof, args=(context, proof_name, verifier))
    context.multi_device_threads[verifier].start()

def the_user_has_a_credential(context, user, table):

    for row in table:
        if row["credential_name"] == "Unverified Person":
            credential = row["credential"]
            context.execute_steps(u'''
                Given the "{user}" has an Unverified Person {credential}
                {table}
            '''.format(user=user, credential=credential, table=table_to_str(table)))
        else:
            # pass for POC
            # TODO call the old Holder has credentials step
            pass

# @given('the "{user}" wants to prove that the holder {proof_name}')
# def step_given_verifier_proof(context, proof_name, user):
#     context.multi_device_threads[user].join()
#     context.multi_device_threads[user] = threading.Thread(target=given_verifier_proof, args=(context, proof_name, user))
#     context.multi_device_threads[user].start()


def given_verifier_proof(context, proof_name, user):
    # Code to set the proof information for the verifier
    context.execute_steps(f'''
        Given the "{user}" has user Verifier capability turned on in dev options
        And the "{user}" has selected to use the {proof_name} proof
    ''')


@given('the user has use Verifier capability turned on in dev options')
def step_turn_on_verifier_capability(context):
    context.thisSettingsPage = context.thisHomePage.select_settings()
    context.thisSettingsPage.enable_developer_mode()
    context.thisDeveloperSettingsPage = context.thisSettingsPage.select_developer()
    context.thisDeveloperSettingsPage.select_use_verifier_capability()
    context.thisSettingsPage = context.thisDeveloperSettingsPage.select_back()
    context.thisSettingsPage.select_back()
    if context.thisHomePage.welcome_to_bc_wallet_modal.is_displayed():
        context.thisHomePage.welcome_to_bc_wallet_modal.select_dismiss()
    assert context.thisHomePage.on_this_page()

@given('the "{user}" has use Verifier capability turned on in dev options')
def step_turn_on_verifier_capability(context, user):
    currentPageObjectContext = set_current_page_object_context(context, user)

    currentPageObjectContext.thisSettingsPage = currentPageObjectContext.thisHomePage.select_settings()
    currentPageObjectContext.thisSettingsPage.enable_developer_mode()
    currentPageObjectContext.thisDeveloperSettingsPage = currentPageObjectContext.thisSettingsPage.select_developer()
    currentPageObjectContext.thisDeveloperSettingsPage.select_use_verifier_capability()
    currentPageObjectContext.thisSettingsPage = currentPageObjectContext.thisDeveloperSettingsPage.select_back()
    currentPageObjectContext.thisSettingsPage.select_back()
    if currentPageObjectContext.thisHomePage.welcome_to_bc_wallet_modal.is_displayed():
        currentPageObjectContext.thisHomePage.welcome_to_bc_wallet_modal.select_dismiss()
    assert currentPageObjectContext.thisHomePage.on_this_page()

@given('the "{user}" has selected to use the {proof_name} proof')
def step_turn_on_verifier_capability(context, proof_name, user):
    currentPageObjectContext = set_current_page_object_context(context, user)

    currentPageObjectContext.thisSettingsPage = currentPageObjectContext.thisHomePage.select_settings()
    currentPageObjectContext.thisChooseAProofRequestPage = currentPageObjectContext.thisSettingsPage.select_send_a_proof_request()
    currentPageObjectContext.thisUseThisProofRequestPage = currentPageObjectContext.thisChooseAProofRequestPage.select_proof_request(proof_name)
    currentPageObjectContext.thisProofRequestQRCodePage = currentPageObjectContext.thisUseThisProofRequestPage.select_use_this_proof_request()
    context.mobile_verifier_qrcode_image = currentPageObjectContext.thisProofRequestQRCodePage.get_qr_code_image()


@when('the "{user}" scans the QR Code from the Verifier')
def step_when_holder_scans_QR_code(context, user):
    context.multi_device_threads[user].join()
    context.multi_device_threads["verifier"].join()

    currentPageObjectContext = set_current_page_object_context(context, user)

    context.multi_device_service_handlers[user].inject_qrcode(context.mobile_verifier_qrcode_image)
    currentPageObjectContext.thisNavBar.select_scan()


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