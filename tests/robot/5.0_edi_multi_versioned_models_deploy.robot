*** Settings ***
Documentation       Legion's EDI check for one model_id but different model versions deploy command
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
Test Setup          Run Keywords
...                 Run EDI deploy and check model started          ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_IMAGE_1}   ${TEST_MODEL_ID}    ${TEST_MODEL_1_VERSION}   AND
...                 Run EDI deploy and check model started          ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_IMAGE_2}   ${TEST_MODEL_ID}    ${TEST_MODEL_2_VERSION}
Test Teardown       Run Keywords
...                 Run EDI undeploy by model version and check     ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}   ${TEST_MODEL_1_VERSION}   ${TEST_MODEL_IMAGE_1}    AND
...                 Run EDI undeploy by model version and check     ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}   ${TEST_MODEL_2_VERSION}   ${TEST_MODEL_IMAGE_2}

*** Test Cases ***
Check EDI deploy 2 models with different versions but the same id
    [Setup]         NONE
    [Documentation]  Try to deploy 2 dummy models with different versions but the same id through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI deploy                      ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_IMAGE_1}
                    Should Be Equal As Integers         ${resp.rc}         0
    ${resp}=        Check model started                 ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    ${TEST_MODEL_1_VERSION}
                    Should contain                      ${resp}                 "model_version": "${TEST_MODEL_1_VERSION}"
    ${resp}=        Run EDI deploy                      ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_IMAGE_2}
                    Should Be Equal As Integers         ${resp.rc}         0
    ${resp}=        Check model started                 ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    ${TEST_MODEL_2_VERSION}
                    Should contain                      ${resp}                 "model_version": "${TEST_MODEL_2_VERSION}"