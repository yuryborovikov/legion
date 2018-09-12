*** Settings ***
Variables           ../load_variables_from_profiles.py   ${PATH_TO_PROFILES_DIR}

*** Variables ***
@{SUBDOMAINS}                       jenkins  nexus
@{ENCLAVE_SUBDOMAINS}               edi  edge  airflow  flower
${TEST_MODEL_ID}                    demo-abc-model
${TEST_EDI_MODEL_ID}                edi-test-model
${TEST_MODEL_1_VERSION}             1.0
${TEST_MODEL_2_VERSION}             1.1
${TEST_MODEL_3_VERSION}             1.2