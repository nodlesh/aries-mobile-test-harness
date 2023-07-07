# https://github.com/bcgov/bc-wallet-mobile/issues/800
@Mobile-Verifier @bc_wallet @Story_800
Feature: Mobile Verifier
   In order to easily prove the data from a holder
   As a verfier in the field
   I want to be able to do a proof with my mobile device


   @T001-MobileVerifier @critical @AcceptanceTest @wip
   Scenario Outline: A wallet user wants to verify someones credential through the wallet they are not connected to
      Given "2" wallet users
         | role     | device   | device_handler |
         | holder   | default  | existing       |
         | verifier | <device> | new            |
      And the "holder" has credentials
         | issuer_agent_type | credential_name   | credential                  | revokable |
         | CANdyUVPIssuer    | Unverified Person | cred_data_unverified_person | False     |
      And the "verifier" wants to prove that the holder <proof_name>
      When the holder scans the QR Code from the Verifier
      And the holder receives the proof request
      And the holder shares the information
      Then the holder is informed that the information sent successfully
      And the verifier receives the information
      And the verifier reviews details of the information

      Examples:
         | device  | proof_name           |
         | default | Over 19 years of age |
   #| opposite     |


   @T002-MobileVerifier @critical @AcceptanceTest @wip
   Scenario: A wallet user wants to verify someones credential through the wallet they are connected to

   @T003-MobileVerifier @critical @AcceptanceTest @wip
   Scenario: A wallet user wants to verify someones credential through the wallet with a connectionless proof request
