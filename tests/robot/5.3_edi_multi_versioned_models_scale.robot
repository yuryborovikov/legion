*** Settings ***
Documentation       Legion's EDI check for one model_id but different model versions scale command
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
Check EDI scale up 1 of 2 models with different versions but the same id
    [Documentation]  Try to scale up 1 of 2 models with different versions but the same id through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI scale with version      ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    2   ${TEST_MODEL_1_VERSION}
                    Should Be Equal As Integers     ${resp.rc}              0
                    Sleep                           10  # because no way to control explicitly scaling the model inside
    # TODO remove sleep
    ${resp}=        Run EDI inspect with parse by model id       ${MODEL_TEST_ENCLAVE}      ${TEST_MODEL_ID}
    ${model_1}=     Find model information in edi   ${resp}      ${TEST_MODEL_ID}   ${TEST_MODEL_1_VERSION}
                    Log                             ${model_1}
    ${model_2}=     Find model information in edi   ${resp}      ${TEST_MODEL_ID}   ${TEST_MODEL_2_VERSION}
                    Log                             ${model_2}
                    Verify model info from edi      ${model_1}   ${TEST_MODEL_ID}   ${TEST_MODEL_IMAGE_1}   ${TEST_MODEL_1_VERSION}  2
                    Verify model info from edi      ${model_2}   ${TEST_MODEL_ID}   ${TEST_MODEL_IMAGE_2}   ${TEST_MODEL_2_VERSION}  1

Check EDI scale down 1 of 2 models with different versions but the same id
    [Documentation]  Try to scale down 1 of 2 models with different versions but the same id through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI scale with version      ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    2   ${TEST_MODEL_1_VERSION}
                    Should Be Equal As Integers     ${resp.rc}              0
                    Sleep                           10  # because no way to control explicitly scaling the model inside
    # TODO remove sleep
    ${resp}=        Run EDI inspect with parse by model id       ${MODEL_TEST_ENCLAVE}      ${TEST_MODEL_ID}
    ${model_1}=     Find model information in edi   ${resp}      ${TEST_MODEL_ID}   ${TEST_MODEL_1_VERSION}
                    Log                             ${model_1}
    ${model_2}=     Find model information in edi   ${resp}      ${TEST_MODEL_ID}   ${TEST_MODEL_2_VERSION}
                    Log                             ${model_2}
                    Verify model info from edi      ${model_1}   ${TEST_MODEL_ID}   ${TEST_MODEL_IMAGE_1}   ${TEST_MODEL_1_VERSION}  2
                    Verify model info from edi      ${model_2}   ${TEST_MODEL_ID}   ${TEST_MODEL_IMAGE_2}   ${TEST_MODEL_2_VERSION}  1

    ${resp}=        Run EDI scale with version      ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    1   ${TEST_MODEL_1_VERSION}
                    Should Be Equal As Integers     ${resp.rc}              0
                    Sleep                           10  # because no way to control explicitly scaling the model inside
    # TODO remove sleep
    ${resp}=        Run EDI inspect with parse by model id       ${MODEL_TEST_ENCLAVE}      ${TEST_MODEL_ID}
    ${model_1}=     Find model information in edi   ${resp}      ${TEST_MODEL_ID}   ${TEST_MODEL_1_VERSION}
                    Log                             ${model_1}
    ${model_2}=     Find model information in edi   ${resp}      ${TEST_MODEL_ID}   ${TEST_MODEL_2_VERSION}
                    Log                             ${model_2}
                    Verify model info from edi      ${model_1}   ${TEST_MODEL_ID}   ${TEST_MODEL_IMAGE_1}   ${TEST_MODEL_1_VERSION}  1
                    Verify model info from edi      ${model_2}   ${TEST_MODEL_ID}   ${TEST_MODEL_IMAGE_2}   ${TEST_MODEL_2_VERSION}  1

Check EDI scale up all instances for 2 models(diff versions) by versions=*
    [Documentation]  Try to scale up 2 models with different versions but the same id by all versions through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI scale with version      ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    2   *
                    Should Be Equal As Integers     ${resp.rc}              0
                    Sleep                           10  # because no way to control explicitly scaling the model inside
    # TODO remove sleep
    ${resp}=        Run EDI inspect with parse by model id       ${MODEL_TEST_ENCLAVE}      ${TEST_MODEL_ID}
    ${model_1}=     Find model information in edi   ${resp}      ${TEST_MODEL_ID}   ${TEST_MODEL_1_VERSION}
                    Log                             ${model_1}
    ${model_2}=     Find model information in edi   ${resp}      ${TEST_MODEL_ID}   ${TEST_MODEL_2_VERSION}
                    Log                             ${model_2}
                    Verify model info from edi      ${model_1}   ${TEST_MODEL_ID}   ${TEST_MODEL_IMAGE_1}   ${TEST_MODEL_1_VERSION}  2
                    Verify model info from edi      ${model_2}   ${TEST_MODEL_ID}   ${TEST_MODEL_IMAGE_2}   ${TEST_MODEL_2_VERSION}  2

Check EDI scale up all instances for 2 models(diff versions) by id=*
    [Documentation]  Try to scale up 2 models with different versions but the same id by all ids through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI scale                   ${MODEL_TEST_ENCLAVE}   *    2
                    Should Be Equal As Integers     ${resp.rc}              0
                    Sleep                           10  # because no way to control explicitly scaling the model inside
    # TODO remove sleep
    ${resp}=        Run EDI inspect with parse by model id       ${MODEL_TEST_ENCLAVE}      ${TEST_MODEL_ID}
    ${model_1}=     Find model information in edi   ${resp}      ${TEST_MODEL_ID}   ${TEST_MODEL_1_VERSION}
                    Log                             ${model_1}
    ${model_2}=     Find model information in edi   ${resp}      ${TEST_MODEL_ID}   ${TEST_MODEL_2_VERSION}
                    Log                             ${model_2}
                    Verify model info from edi      ${model_1}   ${TEST_MODEL_ID}   ${TEST_MODEL_IMAGE_1}   ${TEST_MODEL_1_VERSION}  2
                    Verify model info from edi      ${model_2}   ${TEST_MODEL_ID}   ${TEST_MODEL_IMAGE_2}   ${TEST_MODEL_2_VERSION}  2

Check EDI scale up 1 of 2 models by invalid version
    [Documentation]  Try to scale up 1 of 2 models with different versions but the same id by invalid version through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI scale with version      ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    2   ${TEST_MODEL_1_VERSION}121
                    Should Be Equal As Integers     ${resp.rc}              2
                    Should contain                  ${resp.stderr}          No one model can be found

Check EDI scale up 1 of 2 models without version
    [Documentation]  Try to scale up 1 of 2 models with different versions but the same id without version through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI scale                   ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    2
                    Should Be Equal As Integers     ${resp.rc}              2
                    Should contain                  ${resp.stderr}          Please specify version of model