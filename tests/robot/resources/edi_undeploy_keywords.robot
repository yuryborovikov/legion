*** Settings ***
Documentation       Legionctl undeploy command robot keywords
Resource            keywords.robot

*** Keywords ***
Run EDI undeploy by model version and check
    [Arguments]   ${enclave}    ${model_id}    ${model_ver}    ${model_image}
    Run EDI undeploy with version  ${enclave}   ${model_id}    ${model_ver}
    Should Be Equal As Integers    ${UNDEPLOY_RESPONSE.rc}       0
    Run EDI inspect                ${enclave}
    Should Be Equal As Integers    ${INSPECT_RESPONSE.rc}        0
    Should not contain             ${INSPECT_RESPONSE.stdout}    ${model_image}

Run EDI undeploy model without version and check
    [Arguments]   ${enclave}    ${model_id}
    Run EDI undeploy without version  ${enclave}   ${model_id}
    Should Be Equal As Integers  ${UNDEPLOY_RESPONSE.rc}       0
    Should not contain           ${UNDEPLOY_RESPONSE.stdout}   ${model_id}
    Run EDI inspect              ${enclave}
    Should Be Equal As Integers  ${INSPECT_RESPONSE.rc}        0
    Should not contain           ${INSPECT_RESPONSE.stdout}    ${model_id}

Run EDI undeploy with version
    [Arguments]           ${enclave}   ${model_id}   ${model_version}
    ${result}=            Run Process   legionctl --verbose undeploy ${model_id} --model-version ${model_version} --ignore-not-found --edi ${HOST_PROTOCOL}://edi-${enclave}.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}     shell=True
    Log                   stdout = ${result.stdout}
    Log                   stderr = ${result.stderr}
    Set Suite Variable    ${UNDEPLOY_RESPONSE}    ${result}

Run EDI undeploy without version
    [Documentation]  run legionctl 'undeploy command', logs result and return dict with return code and output(for exceptions)
    [Arguments]           ${enclave}    ${model_id}
    ${result}=            Run Process   legionctl --verbose undeploy ${model_id} --ignore-not-found --edi ${HOST_PROTOCOL}://edi-${enclave}.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}    shell=True
    Log                   stdout = ${result.stdout}
    Log                   stderr = ${result.stderr}
    Set Suite Variable    ${UNDEPLOY_RESPONSE}    ${result}
