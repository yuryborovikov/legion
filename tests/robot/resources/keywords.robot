*** Settings ***
Documentation       Legion robot resources
Resource            variables.robot
Resource            edi_deploy_keywords.robot
Resource            edi_undeploy_keywords.robot
Resource            edi_inspect_keywords.robot
Resource            edi_scale_keywords.robot
Library             String
Library             OperatingSystem
Library             Collections
Library             legion_test.robot.K8s
Library             legion_test.robot.Jenkins
Library             legion_test.robot.Utils
Library             legion_test.robot.Grafana
Library             legion_test.robot.Airflow

*** Keywords ***
Connect to enclave Grafana
    [Arguments]           ${enclave}
    Connect to Grafana    ${HOST_PROTOCOL}://grafana-${enclave}.${HOST_BASE_DOMAIN}                      ${SERVICE_ACCOUNT}          ${SERVICE_PASSWORD}

Connect to Jenkins endpoint
    Connect to Jenkins    ${HOST_PROTOCOL}://jenkins.${HOST_BASE_DOMAIN}

Connect to enclave Airflow
    [Arguments]           ${enclave}
    Connect to Airflow    ${HOST_PROTOCOL}://airflow-${enclave}.${HOST_BASE_DOMAIN}

Connect to enclave Flower
    [Arguments]           ${enclave}
    Connect to Flower    ${HOST_PROTOCOL}://flower-${enclave}.${HOST_BASE_DOMAIN}

Check model started
    [Documentation]  check if model run in container by http request
    [Arguments]           ${enclave}   ${model_id}  ${model_ver}
    Log                   request url is ${HOST_PROTOCOL}://edge-${enclave}.${HOST_BASE_DOMAIN}/api/model/${model_id}/${model_ver}/info
    ${resp}=              Check valid http response   ${HOST_PROTOCOL}://edge-${enclave}.${HOST_BASE_DOMAIN}/api/model/${model_id}/${model_ver}/info
    Log                   ${resp}
    Should not be empty   ${resp}
    Log                   ${resp}
    Set Suite Variable    ${MODEL_RESPONSE}    ${resp}

Verify model info from edi
    [Arguments]      ${target_model}       ${model_id}        ${model_image}      ${model_version}    ${scale_num}
    Should Be Equal  ${target_model[0]}    ${model_id}        invalid model id
    Should Be Equal  ${target_model[1]}    ${model_image}     invalid model image
    Should Be Equal  ${target_model[2]}    ${model_version}   invalid model version
    Should Be Equal  ${target_model[3]}    ${scale_num}       invalid actual scales
    Should Be Equal  ${target_model[4]}    ${scale_num}       invalid desired scale
#    Should Be Empty  ${target_model[5]}                       got some errors ${target_model[5]}

Run and wait Jenkins job
    [Arguments]          ${model_name}                      ${enclave}
    Log                  Start running model: ${model_name}
    Run Jenkins job                                         DYNAMIC MODEL ${model_name}   Enclave=${enclave}
    Log                  Waiting for running model: ${model_name}
    Wait Jenkins job                                        DYNAMIC MODEL ${model_name}   600

Test model pipeline
    [Arguments]          ${model_name}                      ${enclave}=${CLUSTER_NAMESPACE}
    Run and wait Jenkins job                                ${model_name}        ${enclave}
    Last Jenkins job is successful                          DYNAMIC MODEL ${model_name}
    Jenkins artifact present                                DYNAMIC MODEL ${model_name}   notebook.html
    ${model_meta} =      Jenkins log meta information       DYNAMIC MODEL ${model_name}
    Log                  Model meta is ${model_meta}
    ${model_path} =      Get From Dictionary                ${model_meta}                 modelPath
    ${model_id} =        Get From Dictionary                ${model_meta}                 modelId
    ${model_version} =   Get From Dictionary                ${model_meta}                 modelVersion
    ${model_path} =	     Get Regexp Matches	                ${model_path}                 (.*)://[^/]+/(?P<path>.*)   path
    ${model_url} =       Set Variable                       ${HOST_PROTOCOL}://nexus.${HOST_BASE_DOMAIN}/${model_path[0]}
    Log                  External model URL is ${model_url}
    Check remote file exists                                ${model_url}                  ${SERVICE_ACCOUNT}          jonny
    Connect to enclave Grafana                              ${enclave}
    Dashboard should exists                                 ${model_id}
    Sleep                15s
    Metric should be presented                              ${model_id}                   ${model_version}
    ${edi_state}=        Run      legionctl inspect --model-id ${model_id} --format column --edi ${HOST_PROTOCOL}://edi.${HOST_BASE_DOMAIN} --user ${SERVICE_ACCOUNT} --password ${SERVICE_PASSWORD}
    Log                  State of ${model_id} is ${edi_state}

Check if all enclave domains are registered
    [Arguments]             ${enclave}
    :FOR    ${enclave_subdomain}    IN    @{ENCLAVE_SUBDOMAINS}
    \   Check domain exists  ${enclave_subdomain}-${enclave}.${HOST_BASE_DOMAIN}

Run, wait and check jenkins jobs for enclave
    [Arguments]             ${enclave}
    :FOR  ${model_name}  IN  @{JENKINS_JOBS}
    \    Test model pipeline    ${model_name}    ${enclave}

    # --------- TEMPLATE KEYWORDS SECTION -----------

Check if component domain has been secured
    [Arguments]     ${component}    ${enclave}
    [Documentation]  Check that a legion component is secured by auth
    &{response} =    Run Keyword If   '${enclave}' == '${EMPTY}'    Get component auth page    ${HOST_PROTOCOL}://${component}.${HOST_BASE_DOMAIN}/securityRealm/commenceLogin?from=/
    ...    ELSE      Get component auth page    ${HOST_PROTOCOL}://${component}-${enclave}.${HOST_BASE_DOMAIN}/securityRealm/commenceLogin?from=/
    Log              Auth page for ${component} is ${response}
    Dictionary Should Contain Item    ${response}    response_code    200
    ${auth_page} =   Get From Dictionary   ${response}    response_text
    Should contain   ${auth_page}    Log in to dex
    Should contain   ${auth_page}    Log in with Email

Secured component domain should not be accessible by invalid credentials
    [Arguments]     ${component}    ${enclave}
    [Documentation]  Check that a secured legion component does not provide access by invalid credentials
    &{creds} =       Create Dictionary 	login=admin   password=admin
    &{response} =    Run Keyword If   '${enclave}' == '${EMPTY}'    Post credentials to auth    ${HOST_PROTOCOL}://${component}    ${HOST_BASE_DOMAIN}    ${creds}
    ...    ELSE      Post credentials to auth    ${HOST_PROTOCOL}://${component}-${enclave}     ${HOST_BASE_DOMAIN}    ${creds}
    Log              Bad auth page for ${component} is ${response}
    Dictionary Should Contain Item    ${response}    response_code    200
    ${auth_page} =   Get From Dictionary   ${response}    response_text
    Should contain   ${auth_page}    Log in to Your Account
    Should contain   ${auth_page}    Invalid Email Address and password


Secured component domain should be accessible by valid credentials
    [Arguments]     ${component}    ${enclave}
    [Documentation]  Check that a secured legion component does not provide access by invalid credentials
    &{creds} =       Get static user data
    &{response} =    Run Keyword If   '${enclave}' == '${EMPTY}'    Post credentials to auth    ${HOST_PROTOCOL}://${component}    ${HOST_BASE_DOMAIN}    ${creds}
    ...    ELSE      Post credentials to auth    ${HOST_PROTOCOL}://${component}-${enclave}     ${HOST_BASE_DOMAIN}    ${creds}
    Log              Bad auth page for ${component} is ${response}
    Dictionary Should Contain Item    ${response}    response_code    200
    ${auth_page} =   Get From Dictionary   ${response}    response_text
    Should contain   ${auth_page}    ${component}
    Should not contain   ${auth_page}    Invalid Email Address and password