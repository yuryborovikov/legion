*** Settings ***
Documentation       Legion's EDI check for one model_id but different model versions inspect command
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
Check EDI model inspect by model id return 2 models
    [Documentation]  Try to inspect 2 models with different versions but the same id by model_id through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI inspect by model id     ${MODEL_TEST_ENCLAVE}    ${TEST_MODEL_ID}
                    Should Be Equal As Integers     ${resp.rc}          0
                    Should contain                  ${resp.stdout}      ${TEST_MODEL_IMAGE_1}
                    Should contain                  ${resp.stdout}      ${TEST_MODEL_IMAGE_2}

Check EDI model inspect by model version return 1 model
    [Documentation]  Try to inspect 2 models with different versions but the same id by model_id through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI inspect by model version    ${MODEL_TEST_ENCLAVE}    ${TEST_MODEL_1_VERSION}
                    Should Be Equal As Integers         ${resp.rc}          0
                    Should contain                      ${resp.stdout}      ${TEST_MODEL_IMAGE_1}
                    Should not contain                  ${resp.stdout}      ${TEST_MODEL_IMAGE_2}

Check EDI model inspect by model id and version return 1 model
    [Documentation]  Try to inspect 1 model by id and version through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI inspect by model id and model version    ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}      ${TEST_MODEL_1_VERSION}
                    Should Be Equal As Integers                      ${resp.rc}         0
                    Should contain                                   ${resp.stdout}     ${TEST_MODEL_IMAGE_1}
                    Should not contain                               ${resp.stdout}     ${TEST_MODEL_IMAGE_2}

Check EDI model inspect by model id=* return all models
    [Documentation]  Try to inspect 2 models by all ids through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI inspect by model id    ${MODEL_TEST_ENCLAVE}   '*'
                    Should Be Equal As Integers    ${resp.rc}         0
                    Should contain                 ${resp.stdout}     ${TEST_MODEL_IMAGE_1}
                    Should contain                 ${resp.stdout}     ${TEST_MODEL_IMAGE_2}

Check EDI model inspect by model version=* return all models
    [Documentation]  Try to inspect 2 models by all versions through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI inspect by model id and model version    ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    '*'
                    Should Be Equal As Integers    ${resp.rc}         0
                    Should contain                 ${resp.stdout}     ${TEST_MODEL_IMAGE_1}
                    Should contain                 ${resp.stdout}     ${TEST_MODEL_IMAGE_2}

Check EDI model inspect by invalid model id
    [Documentation]  Try to inspect model by invalid model_id through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI inspect by model id     ${MODEL_TEST_ENCLAVE}    ${TEST_MODEL_ID}test
                    Should Be Equal As Integers     ${resp.rc}          0
                    Should be empty                 ${resp.stdout}

Check EDI model inspect by invalid model version
    [Documentation]  Try to inspect model by invalid model_version through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI inspect by model version    ${MODEL_TEST_ENCLAVE}  ${TEST_MODEL_1_VERSION}test
                    Should Be Equal As Integers         ${resp.rc}        0
                    Should be empty                     ${resp.stdout}

Check EDI model inspect by invalid model id and invalid version
    [Documentation]  Try to inspect model by invalid model_id and model_version through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI inspect by model id and model version    ${MODEL_TEST_ENCLAVE}    ${TEST_MODEL_ID}test   ${TEST_MODEL_1_VERSION}test
                    Should Be Equal As Integers                      ${resp.rc}          0
                    Should be empty                                  ${resp.stdout}

Check EDI model inspect by invalid model id and VALID version
    [Documentation]  Try to inspect model by invalid model_id and VALID model_version through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI inspect by model id and model version    ${MODEL_TEST_ENCLAVE}    ${TEST_MODEL_ID}test   ${TEST_MODEL_1_VERSION}
                    Should Be Equal As Integers                      ${resp.rc}          0
                    Should be empty                                  ${resp.stdout}

Check EDI model inspect by VALID model id and invalid version
    [Documentation]  Try to inspect model by valid model_id and invalid model_version through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI inspect by model id and model version    ${MODEL_TEST_ENCLAVE}    ${TEST_MODEL_ID}   ${TEST_MODEL_1_VERSION}test
                    Should Be Equal As Integers                      ${resp.rc}          0
                    Should be empty                                  ${resp.stdout}
