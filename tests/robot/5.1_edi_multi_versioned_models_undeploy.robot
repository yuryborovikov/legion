*** Settings ***
Documentation       Legion's EDI check for one model_id but different model versions undeploy command
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
Check EDI undeploy 1 of 2 models with different versions but the same id
    [Documentation]  Try to undeploy 1 of 2 models with different versions but the same id through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI undeploy with version   ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    ${TEST_MODEL_1_VERSION}
                    Should Be Equal As Integers     ${resp.rc}         0
    ${resp}=        Run EDI inspect by model id     ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}
                    Should Be Equal As Integers     ${resp.rc}              0
                    Should not contain              ${resp.stdout}          ${TEST_MODEL_IMAGE_1}
                    Should contain                  ${resp.stdout}          ${TEST_MODEL_IMAGE_2}

Check EDI undeploy all model instances by version
    [Documentation]  Try to undeploy all models with different versions but the same id by version through EDI console
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

    ${resp}=        Run EDI undeploy with version   ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    ${TEST_MODEL_1_VERSION}
                    Should Be Equal As Integers     ${resp.rc}         0
    ${resp}=        Run EDI inspect by model id     ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}
                    Should Be Equal As Integers     ${resp.rc}              0
                    Should not contain              ${resp.stdout}          ${TEST_MODEL_1_VERSION}
                    Should contain                  ${resp.stdout}          ${TEST_MODEL_2_VERSION}

Check EDI undeploy all versioned model instances by id=*
    [Documentation]  Try to undeploy all models by id=* through EDI console
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI undeploy without version    ${MODEL_TEST_ENCLAVE}    '*'
                    Should Be Equal As Integers     ${resp.rc}         0
    ${resp}=        Run EDI inspect by model id     ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}
                    Should Be Equal As Integers     ${resp.rc}              0
                    Should be empty                 ${resp.stdout}

Check EDI undeploy all versioned model instances by versions=*
    [Documentation]  Try to undeploy all models by versions=* through EDI console
    [Tags]  edi  cli  enclave   multi_versions
   ${resp}=         Run EDI undeploy with version   ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}    '*'
                    Should Be Equal As Integers     ${resp.rc}         0
    ${resp}=        Run EDI inspect by model id     ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}
                    Should Be Equal As Integers     ${resp.rc}              0
                    Should be empty                 ${resp.stdout}

Check EDI undeploy 1 of 2 models without version
    [Documentation]  Try to undeploy 1 of 2 models with different versions but the same id without setting version
    [Tags]  edi  cli  enclave   multi_versions
    ${resp}=        Run EDI undeploy without version   ${MODEL_TEST_ENCLAVE}   ${TEST_MODEL_ID}
                    Should Be Equal As Integers        ${resp.rc}         2
                    Should contain                     ${resp.stderr}     Founded more then one deployment