*** Settings ***
Documentation       Legion's EDI check for one model undeploy command
Test Timeout        5 minutes
Resource            resources/keywords.robot
Resource            resources/variables.robot
Variables           load_variables_from_profiles.py    ${PATH_TO_PROFILES_DIR}
Library             legion_test.robot.Utils
Library             Collections
Library             Process
Suite Setup         Run Keywords
...                 Check EDI availability in all enclaves    AND
...                 Choose cluster context    ${CLUSTER_NAME}
Test Setup          Run EDI deploy and check model started              ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_IMAGE_1}   ${TEST_MODEL_ID}    ${TEST_MODEL_1_VERSION}
Test Teardown       Run EDI undeploy model without version and check    ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}

*** Test Cases ***
Check EDI undeploy procedure
    [Documentation]  Try to undeploy dummy valid model through EDI console
    [Tags]  edi  cli  enclave   one_version
    ${resp}=        Run EDI undeploy without version    ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_IMAGE_1}
                    Should Be Equal As Integers         ${resp.rc}         0
    ${resp}=        Run EDI inspect                     ${MODEL_TEST_ENCLAVE}
                    Should Be Equal As Integers         ${resp.rc}         0
                    Should not contain                  ${resp.stdout}     ${model_id}

Check EDI undeploy procedure by invalid model id
    [Setup]    NONE
    [Documentation]  Try to undeploy model through EDI console by invalid id
    [Tags]  edi  cli  enclave   one_version
    ${resp}=        Run EDI undeploy without version    ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_IMAGE_1}test
                    Should Be Equal As Integers         ${resp.rc}         0
                    Should contain                      ${resp.stdout}     Cannot find any deployment - ignoring
    [Teardown]    NONE
