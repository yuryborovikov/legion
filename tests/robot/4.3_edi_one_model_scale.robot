*** Settings ***
Documentation       Legion's EDI check for one model scale command
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
Check EDI scale up procedure
    [Documentation]  Try to scale up model through EDI console
    [Tags]  edi  cli  enclave   one_version
    ${resp}=        Run EDI scale                  ${MODEL_TEST_ENCLAVE}    ${TEST_MODEL_ID}    2
                    Should Be Equal As Integers    ${resp.rc}           0
                    Sleep                          10  # because no way to control explicitly scaling the model inside
    # TODO remove sleep
    ${resp}=        Run EDI inspect with parse     ${MODEL_TEST_ENCLAVE}
    ${model}=       Find model information in edi  ${resp}    ${TEST_MODEL_ID}
                    Log                            ${model}
                    Verify model info from edi     ${model}   ${TEST_MODEL_ID}    ${TEST_MODEL_IMAGE_1}   ${TEST_MODEL_1_VERSION}   2

Check EDI scale down procedure
    [Documentation]  Try to scale down model through EDI console
    [Tags]  edi  cli  enclave   one_version
    ${resp}=        Run EDI scale                  ${MODEL_TEST_ENCLAVE}    ${TEST_MODEL_ID}    2
                    Should Be Equal As Integers    ${resp.rc}          0
                    Sleep                          10
    # TODO remove sleep
    ${resp}=        Run EDI inspect with parse     ${MODEL_TEST_ENCLAVE}
    ${model}=       Find model information in edi  ${resp}    ${TEST_MODEL_ID}
                    Log                            ${model}
                    Verify model info from edi     ${model}   ${TEST_MODEL_ID}    ${TEST_MODEL_IMAGE_1}   ${TEST_MODEL_1_VERSION}   2

    ${resp}=        Run EDI scale                  ${MODEL_TEST_ENCLAVE}    ${TEST_MODEL_ID}    1
                    Should Be Equal As Integers    ${resp.rc}          0
                    Sleep                          10
    # TODO remove sleep
    ${resp}=        Run EDI inspect with parse     ${MODEL_TEST_ENCLAVE}
    ${model}=       Find model information in edi  ${resp}    ${TEST_MODEL_ID}
                    Log                            ${model}
                    Verify model info from edi     ${model}   ${TEST_MODEL_ID}    ${TEST_MODEL_IMAGE_1}   ${TEST_MODEL_1_VERSION}   1

Check EDI scale to 0 procedure
    [Documentation]  Try to scale to 0 model through EDI console
    [Tags]  edi  cli  enclave one_version
    ${resp}=        Run EDI scale                  ${MODEL_TEST_ENCLAVE}    ${TEST_MODEL_ID}    0
                    Should Be Equal As Integers    ${resp.rc}          2
                    Should contain                 ${resp.stderr}      Invalid scale parameter: should be greater then 0

Check EDI invalid model id scale up procedure
    [Documentation]  Try to scale up dummy model with invalid name through EDI console
    [Tags]  edi  cli  enclave   one_version
    ${resp}=        Run EDI scale                ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}test   2
                    Should Be Equal As Integers  ${resp.rc}         2
                    Should contain               ${resp.stderr}     No one model can be found