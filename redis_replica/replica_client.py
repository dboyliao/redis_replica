from redis import StrictRedis
from redis import ConnectionError

class RedisReplicaClient(StrictRedis):
    
    def __init__(self, hosts = None, **kwargs):
        """
        A redis client which will automatically search for the available master host 
        from `hosts`. In the case no master host available, it will connect to one of 
        the available slaves.
        
        Example:
            >>> # Supose localhost:6380 is the master host.
            >>> hosts = ["localhost:6379", "localhost:6380"] 
            >>> r_rs = RedisReplicaClient(hosts = hosts)
            >>> r_rs.connection_info() # Current connection established on: localhost:6380
        """
        
        # Properly initialize hosts.
        if hosts == None:
            hosts = ["localhost:6379"]
        elif isinstance(hosts, str):
            hosts = [hosts]
        
        assert isinstance(hosts, list), "hosts must be a string or a list of urls os the hosts."
        
        self.__alive_hosts = []
        while True:
            try:
                host, port = hosts.pop(0).split(":")
                super(RedisReplicaClient, self).__init__(host = host, port = port, **kwargs)
                info = self.info() # If this pass, hosts is alive.
                self.__alive_hosts.append(":".join([host, port]))
                if info["role"] == "master":
                    self._host = host
                    self._port = port
                    break
            except:
                if len(hosts) == 0 and len(self.__alive_hosts) == 0:
                    raise ConnectionError("No host available.")
                elif len(hosts) == 0 and len(self.__alive_hosts) > 0:
                    host, port = self.__alive_hosts.pop(0).split(":")
                    super(RedisReplicaClient, self).__init__(host = host, port = port, **kwargs)
                    self._host, self._port = host, port
                    break
                    
                continue
    
    @property            
    def connection_info(self):
        msg = "Current connection established on: {host}:{port}"
        print msg.format(host = self._host, port = self._port)