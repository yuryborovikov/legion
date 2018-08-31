*** Settings ***
Documentation       Legionctl deploy command robot keywords
Resource            keywords.robot

*** Keywords ***
Run EDI deploy
    [Documentation]  run legionctl 'deploy command', logs result and return dict with return code and output(for exceptions)
    [Arguments]           ${enclave}    ${image}
    ${result}=            Run Process   legionctl --verbose deploy ${image} --edi ${HOST_PROTOCOL}://edi-${enclave}.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}    shell=True
    Log                   stdout = ${result.stdout}
    Log                   stderr = ${result.stderr}
    Set Suite Variable    ${DEPLOY_RESPONSE}    ${result}

Run EDI deploy with scale
    [Documentation]  run legionctl 'deploy command with scale option', logs result and return dict with return code and output(for exceptions)
    [Arguments]           ${enclave}    ${image}    ${scale_count}
    ${result}=            Run Process   legionctl --verbose deploy ${image} --scale ${scale_count} --edi ${HOST_PROTOCOL}://edi-${enclave}.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}    shell=True
    Log                   stdout = ${result.stdout}
    Log                   stderr = ${result.stderr}
    Set Suite Variable    ${DEPLOY_RESPONSE}    ${result}

Run EDI deploy and check model started
    [Arguments]          ${enclave}    ${image}    ${model_id}    ${model_ver}
    Run EDI deploy       ${enclave}    ${image}
    Should Be Equal As Integers    ${DEPLOY_RESPONSE.rc}    0
    Check model started  ${enclave}    ${model_id}    ${model_ver}
    Should contain       ${MODEL_RESPONSE}    "model_version": "${model_ver}"
