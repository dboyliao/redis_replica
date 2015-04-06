from redis import StrictRedis
from redis import ConnectionError

class RedisReplicaClient(StrictRedis):
    
    def __init__(self, hosts = None, **kwargs):
        """
        A redis client which will automatically search for the available primary host 
        from `hosts`.
        
        Example:
            hosts = ["localhost:6379", "localhost:6380"] # localhost:6380 --> primary
            r_rs = RedisReplicaClient(hosts = hosts)
            r_rs.connection_info() # Current connection established on: localhost:6380
        """
        
        # Properly initialize hosts.
        if hosts == None:
            hosts = ["localhost:6379"]
        elif isinstance(hosts, str):
            hosts = [hosts]
        
        assert isinstance(hosts, list), "hosts must be a string or a list of urls os the hosts."

        while True:
            try:
                host, port = hosts.pop(0).split(":")
                super(RedisReplicaClient, self).__init__(host = host, port = port, **kwargs)
                self.echo("ping")
                self._host = host
                self._port = port
                conf = self.config_get()
                if conf["slaveof"] == "":
                    break
            except:
                if len(hosts) == 0:
                    raise ConnectionError("No host available.")
                continue
                
    def connection_info(self):
        msg = "Current connection established on: {host}:{port}"
        print msg.format(host = self._host, port = self._port)

