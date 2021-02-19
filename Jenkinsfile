pipeline {
        agent any

        stages {
            stage('allocate folder') {
                steps {
                    sh returnStatus: true,
                    script:
                    '''
                        mkdir -p /mnt/jenkins/rpmbuild/{,BUILD,BUILDROOT,RPMS,SOURCES,SRPMS}
                    '''
                }
            }

            stage('archive project') {
                steps {
                    sh returnStatus: true,
                    script:
                    '''
                        workspace=/tmp
                        archive_name=`cat qbittorrent.spec.template| grep "Name:    " | sed 's@^Name:    @@g'`-`cat qbittorrent.spec.template| grep "Version: " | sed 's@^Version: @@g'`
                        archive_file=$archive_name.tar.gz
                        archive_dir=$workspace/$archive_name
                        save_file=/mnt/jenkins/rpmbuild/SOURCES/$archive_file
                        mkdir -p $archive_dir
                        rsync -av * $archive_dir
                        cd $workspace
                        tar -czf $save_file $archive_name --remove-files
                    '''
                }
            }

            stage('Build project') {
                steps {
                    sh returnStatus: true,
                    script:
                    '''
                        rpmbuild -bb --define "_topdir /mnt/jenkins/rpmbuild/" qbittorrent.spec.template
                    '''
                }
            }
        }

    /*
        Post trigger
    */
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
