pipeline {
        agent any

        stages {
            stage('allocate diskspace') { 
                steps {
                    sh 'mkdir -p /mnt/jenkins/rpmbuild/{,BUILD,BUILDROOT,RPMS,SOURCES,SRPMS}'
                }
            }

            stage('download release') { 
                steps {
                    sh 'wget -P /mnt/jenkins/rpmbuild/SOURCES -c https://github.com/c0re100/qBittorrent-Enhanced-Edition/archive/release-4.3.3.10.tar.gz'
                }
            }

            stage('unzip release') {
                steps {
                    dir('/mnt/jenkins/rpmbuild/SOURCES/') {
                        sh 'tar -zxvf release-4.3.3.10.tar.gz'
                    }
                }
            }

            stage('remove release') {
                steps {
                    dir('/mnt/jenkins/rpmbuild/SOURCES/') {
                        sh 'rm -rf release-4.3.3.10.tar.gz'
                    }
                }
            }

            stage('rename release dir') {
                steps {
                    dir('/mnt/jenkins/rpmbuild/SOURCES/') {
                        sh 'mv qBittorrent-Enhanced-Edition-* qbittorrent-enhanced-edition-4.3.3.10'
                    }
                }
            }

            stage('repack release') {
                steps {
                    dir('/mnt/jenkins/rpmbuild/SOURCES/') {
                        sh 'tar -czf qbittorrent-enhanced-edition-4.3.3.10.tar.gz qbittorrent-enhanced-edition-4.3.3.10 --remove-files'
                    }
                }
            }

            stage('Build project') {
                steps {
                    sh 'rpmbuild -bb --define "_topdir /mnt/jenkins/rpmbuild/" qbittorrent.spec'
                }
            }
        }

    // Post trigger
    post {
        always {
            emailext body: '''
<!DOCTYPE html>
<html>

    <body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4" offset="0">
        <table width="95%" cellpadding="0" cellspacing="0"  style="font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif">
        <tr>
            <br>
                This email was sent by Jenkins
            </br>
        </tr>
        <tr>
            <td>
                <b>
                    <br>
                        <font color="#6E6E6E">Project details</font>
                    </br>
                </b>
                <hr size="2" width="100%" align="center" />
            </td>
        </tr>
        <tr>
            <td>
                <ul>
                    <li>Project name: ${PROJECT_NAME}</li>
                    <li>Build branch: ${BRANCH_NAME}</li>
                    <li>Build number: #${BUILD_NUMBER}</li>
                    <li>Build result: ${BUILD_STATUS}</li>
                    <li>Trigger: ${CAUSE}</li>
                </ul>
                <hr size="2" width="100%" align="center" />
            </td>
        </tr>
        <tr>
            <td>
                <b>
                    <br>
                        <font color="#6E6E6E">Console output: <a href="${BUILD_URL}console">${PROJECT_NAME} #${BUILD_NUMBER}</a></font>
                    </br>
                </b>
            </td>
        </tr>
        </table>
    </body>
</html>
            ''',
            subject: 'Jenkins - $PROJECT_NAME build was $BUILD_STATUS #$BUILD_NUMBER',
            to: '${DEFAULT_RECIPIENTS}'
        }

        success {
            dir('/mnt/jenkins/rpmbuild/RPMS') {
                archiveArtifacts artifacts: 'aarch64/*.rpm',
                fingerprint: true,
                onlyIfSuccessful: true
            }
        }

        cleanup {
            dir('/mnt/jenkins/rpmbuild') {
                sh returnStatus: true, script: '/usr/bin/rm -rf *'
            }
        }
    }
}
