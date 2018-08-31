*** Settings ***
Documentation       Legionctl inspect command robot keywords
Resource            keywords.robot

*** Keywords ***
Run EDI inspect
    [Documentation]  run legionctl 'inspect command', logs result and return dict with return code and output
    [Arguments]           ${enclave}
    ${result}=            Run Process   legionctl --verbose inspect --format column --edi ${HOST_PROTOCOL}://edi-${enclave}.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}    shell=True
    Log                   stdout = ${result.stdout}
    Log                   stderr = ${result.stderr}
    Set Suite Variable    ${INSPECT_RESPONSE}    ${result}

Run EDI inspect by model id
    [Documentation]  run legionctl 'inspect command', logs result and return dict with return code and output
    [Arguments]           ${enclave}    ${model_id}
    ${result}=            Run Process   legionctl --verbose inspect --model-id ${model_id} --format column --edi ${HOST_PROTOCOL}://edi-${enclave}.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}    shell=True
    Log                   stdout = ${result.stdout}
    Log                   stderr = ${result.stderr}
    Set Suite Variable    ${INSPECT_RESPONSE}    ${result}

Run EDI inspect by model version
    [Documentation]  run legionctl 'inspect command', logs result and return dict with return code and output
    [Arguments]           ${enclave}    ${model_ver}
    ${result}=            Run Process   legionctl --verbose inspect --model-version ${model_ver} --format column --edi ${HOST_PROTOCOL}://edi-${enclave}.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}    shell=True
    Log                   stdout = ${result.stdout}
    Log                   stderr = ${result.stderr}
    Set Suite Variable    ${INSPECT_RESPONSE}    ${result}

Run EDI inspect by model id and model version
    [Documentation]  run legionctl 'inspect command', logs result and return dict with return code and output
    [Arguments]           ${enclave}    ${model_id}     ${model_ver}
    ${result}=            Run Process   legionctl --verbose inspect --model-id ${model_id} --model-version ${model_ver} --format column --edi ${HOST_PROTOCOL}://edi-${enclave}.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}    shell=True
    Log                   stdout = ${result.stdout}
    Log                   stderr = ${result.stderr}
    Set Suite Variable    ${INSPECT_RESPONSE}    ${result}

Run EDI inspect with parse
    [Documentation]  get parsed inspect result for validation and logs it
    [Arguments]           ${enclave}
    ${edi_state} =        Run EDI inspect                                ${enclave}
    ${parsed} =           Parse edi inspect columns info                 ${edi_state.stdout}
    Log                   ${parsed}
    Set Suite Variable    ${PARSED_INSPECT_RESPONSE}    ${parsed}

Run EDI inspect with parse by model id
    [Documentation]  get parsed inspect result for validation and logs it
    [Arguments]           ${enclave}        ${model_id}
    ${edi_state} =        Run EDI inspect by model id    ${enclave}      ${model_id}
    ${parsed} =           Parse edi inspect columns info                 ${edi_state.stdout}
    Log                   ${parsed}
    Set Suite Variable    ${PARSED_INSPECT_RESPONSE}    ${parsed}
