# Redis Replication Set Client

**Warning**: This is not the offical redis-py package. I write this since I didn't find a way to automatically connect to available hosts in a redis replication set using StricRedis from the offical redis-py package.

(If you know there is a way to do that, please let me know.....I google it for a long time and did not see useful information.)


## Basic Usage

```
# Suppose you have two redis-server on localhost at port 6379 and 6380, respectively, and the one at port 6380 is the primary host.

from redis_replica import RedisReplicaClient

hosts = ["localhost:6379", "localhost:6380"]
r_rs = RedisReplicaClient(hosts = hosts)
r_rs.connection_info() # Current connection established on: localhost:6380
```

- `RedisReplicaClient` will automatically connect to the primary host.
- all the keyword arguments apply to `StricRedis` are also valid in `RedisReplicaClient`.

## Installation

- `git clone https://github.com/dboyliao/redis_replica.git && cd redis_replica`
- `python setup.py install`


I hope you enjoy using it. :)
