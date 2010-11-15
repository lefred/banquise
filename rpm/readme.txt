how to create the source archive to build the rpm :

git archive master --format tar --prefix banquise-server-0.5/ | gzip > ~/rpmbuild/SOURCES/banquise-0.5.tgz
rpmbuild -ba banquise-server.spec
