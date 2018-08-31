*** Settings ***
Documentation       Legionctl scale command robot keywords
Resource            keywords.robot

*** Keywords ***
Run EDI scale
    [Documentation]  run legionctl 'scale command', logs result and return dict with return code and output(for exceptions)
    [Arguments]           ${enclave}    ${model_id}     ${new_scale}
    ${result}=            Run Process   legionctl --verbose scale ${model_id} ${new_scale} --edi ${HOST_PROTOCOL}://edi-${enclave}.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}   shell=True
    Log                   stdout = ${result.stdout}
    Log                   stderr = ${result.stderr}
    Set Suite Variable    ${SCALE_RESPONSE}    ${result}

Run EDI scale with version
    [Documentation]  run legionctl 'scale command', logs result and return dict with return code and output(for exceptions)
    [Arguments]           ${enclave}    ${model_id}     ${new_scale}    ${model_ver}
    ${result}=            Run Process   legionctl --verbose scale ${model_id} ${new_scale} --model-version ${model_ver} --edi ${HOST_PROTOCOL}://edi-${enclave}.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}    shell=True
    Log                   stdout = ${result.stdout}
    Log                   stderr = ${result.stderr}
    Set Suite Variable    ${SCALE_RESPONSE}    ${result}
