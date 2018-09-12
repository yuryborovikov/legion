*** Settings ***
Documentation       Legion stack operational check
Resource            ../../resources/keywords.robot
Resource            ../../resources/variables.robot
Variables           ../../load_variables_from_profiles.py    ${PATH_TO_PROFILES_DIR}
Library             legion_test.robot.Utils
Library             legion_test.robot.Jenkins
Suite Setup         Run Keywords
...                 Connect to Jenkins endpoint    AND
...                 Run Jenkins job    PERF TEST Vertical-Scaling   Enclave=${MODEL_TEST_ENCLAVE}    AND
...                 Run all test Jenkins jobs for enclave    ${MODEL_TEST_ENCLAVE}

*** Test Cases ***
Running, waiting and checks jobs in Jenkins
    [Documentation]  Build and check every example in Jenkins
    [Tags]  jenkins  models  enclave
    Wait all test Jenkins jobs are finished
    Check all test models are successful and have metrics    ${MODEL_TEST_ENCLAVE}

Check Vertical Scailing
    [Documentation]  Runs "PERF TEST Vertical-Scaling" jenkins job to test vertical scailing
    [Tags]  jenkins model
    :FOR  ${enclave}    IN    @{ENCLAVES}
    \  Connect to Jenkins endpoint
        Wait Jenkins job                  PERF TEST Vertical-Scaling   600
        Last Jenkins job is successful    PERF TEST Vertical-Scaling