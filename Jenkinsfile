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
