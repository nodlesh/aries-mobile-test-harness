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
      And the "holder" has a <credential> credential
      And the verifier wants to prove that the holder <proof>
      When the holder scans the QR Code from the Verifier
      And the holder receives the proof request
      And the holder shares the information
      Then the holder is informed that the information sent successfully
      And the verifier receives the information
      And the verifier reviews details of the information

      Examples:
         | device  |
         | default |
   #| opposite     |


   @T002-MobileVerifier @critical @AcceptanceTest @wip
   Scenario: A wallet user wants to verify someones credential through the wallet they are connected to

   @T003-MobileVerifier @critical @AcceptanceTest @wip
   Scenario: A wallet user wants to verify someones credential through the wallet with a connectionless proof request
