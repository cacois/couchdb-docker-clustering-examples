docker rm -f couchdb.one
docker rm -f couchdb.two
docker rm -f couchdb.three

rm -rf couch1data
rm -rf couch2data
rm -rf couch3data

docker network remove couch
rm /tmp/my.cookie