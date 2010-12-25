how to create the source archive to build the rpm :

$ git archive master --format tar --prefix banquise-server-0.5/ | gzip > ~/rpmbuild/SOURCES/banquise-0.5.tgz
$ rpmbuild -ba banquise-server.spec

other needed sources are in the rpm folder :
- patches for django 1.1.x (used in centos)
- patches for json version used in centos
- banquise-server.conf file for apache

lefred

merry x-mas
