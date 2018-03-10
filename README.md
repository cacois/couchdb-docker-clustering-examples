# CouchDB 2.1.1 Clustering Examples

CouchDB clustering can be infuriating. Here are some magic incantations to help clarify the process.

For the quick demo, run the following commands:

    $ ./setup.sh
    <wait 2 seconds...>
    $ ./cluster.sh
    {"error":"bad_request","reason":"Cluster is already enabled"}
    {"ok":true}
    {"ok":true}
    {"ok":true}
    {"ok":true}
    {"ok":true}

_Note: See that bad_request error? Ignore it. It isn't a problem, but you DO need to run the command that returns it, or the whole clustering process will fail._

To tear everything down again, run:

    $ ./destroy

## Testing your cluster

First, to see if your cluster is setup, check membership:

    $ curl http://admin:admin@localhost:5984/_membership | python -m json.tool
    {
        "all_nodes": [
            "couchdb@couchdb.one",
            "couchdb@couchdb.three",
            "couchdb@couchdb.two"
        ],
        "cluster_nodes": [
            "couchdb@couchdb.one",
            "couchdb@couchdb.three",
            "couchdb@couchdb.two"
        ]
    }

You should see the above output. `cluster_nodes` represents the list of nodes that are stored in the DB as part of the cluster. This shows what nods are known, but not what nods are connected. `all_nodes` represents the list of nodes actually connected to the cluster and communicating. This is the really important bit. 

At this point, if you create a DB or add a document, you will see it replicated across all three cluster nodes. But you aren't done yet! Your cluster is not really complete until you can shut down a node and have it automatically reconnect when it comes back up. Until you see this happen, don't assume your cluster is ready. Let's try it:

    $ docker stop couchdb.two

Now check membership again:

    $ curl http://admin:admin@localhost:5984/_membership | python -m json.tool
    {
        "all_nodes": [
            "couchdb@couchdb.one",
            "couchdb@couchdb.three"
        ],
        "cluster_nodes": [
            "couchdb@couchdb.one",
            "couchdb@couchdb.three",
            "couchdb@couchdb.two"
        ]
    }

Node down. Now, if things are set up right, it will rejoin the cluster when we start up the container:

    $ docker start couchdb.two

Wait a few seconds for it to connect...

    $ curl http://admin:admin@localhost:5984/_membership | python -m json.tool
    {
        "all_nodes": [
            "couchdb@couchdb.one",
            "couchdb@couchdb.three",
            "couchdb@couchdb.two"
        ],
        "cluster_nodes": [
            "couchdb@couchdb.one",
            "couchdb@couchdb.three",
            "couchdb@couchdb.two"
        ]
    }

Now you can be confident. 

## Loading data

If you want to test your cluster with some data load, run the load.py script i've included:

    $ ./load.py

This script will randomly insert (and occasionally delete) documents from the cluster. Leave it to run, and it will add more and more data, which you will see replicated across the whole cluster.

## Secrets of the erlang cookie

The shared erlang cookie is the key to making a cluster resilient to nodes leaving and reconnecting. Without it, your cluster will form and look good, but nodes will not reconnect after disconnection. This is bad. Here's some things to know:

* You need an erlang cookie that is identical on ALL cluster nodes. This can only be set in two ways:
    * set the cookie /opt/couchdb/.erlang.cookie file (this is what we're doing in the examples in this repo), or
    * set it in the vm.args file
* You will find references on the interwebz to a recieve_cookie action you can post to the _cluster_setup endpoint. THIS IS A LIE. There are only two ways to set this cookie - see above.
* The .erlang.cookie file MUST be set to 600 permissions, only accessible by the user running the couchdb process
