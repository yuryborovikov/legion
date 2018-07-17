node {
    def legion = load legion()

    legion.pod(memory: '1Gi'){
        stage('clone repo'){
            checkout scm
        }

        stage('run perf tests'){
            legion.runPerfomanceTests('test_basic.py')
        }
    }
}