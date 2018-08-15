*** Settings ***
Documentation       Legion's EDI check for one model inspect command
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
Check EDI enclave inspect procedure
    [Documentation]  Try to inspect enclave through EDI console
    [Tags]  edi  cli  enclave   one_version
    ${resp}=        Run EDI inspect                ${MODEL_TEST_ENCLAVE}
                    Should Be Equal As Integers    ${resp.rc}          0
                    Should contain                 ${resp.stdout}      ${TEST_MODEL_ID}

Check EDI invalid enclave name inspect procedure
    [Documentation]  Try to inspect invalid enclave through EDI console
    [Tags]  edi  cli  enclave   one_version
    ${resp}=        Run EDI inspect                ${MODEL_TEST_ENCLAVE}test
                    Should Be Equal As Integers    ${resp.rc}          2
                    Should contain                 ${resp.stderr}      ERROR - Failed to connect

Check EDI enclave inspect procedure without deployed model
    [Setup]         NONE
    [Documentation]  Try inspect through EDI console on empty enclave
    [Tags]  edi  cli  enclave   one_version
    ${resp}=        Run EDI inspect                ${MODEL_TEST_ENCLAVE}
                    Should Be Equal As Integers    ${resp.rc}          0
                    Should Not Contain             ${resp.stdout}      ${model_id}
    [Teardown]      NONE