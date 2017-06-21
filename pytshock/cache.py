class Cache:
    def get_token(self, host_ip: str, host_port: str):
        raise NotImplementedError

    def save_token(self, host_ip: str, host_port: str):
        raise NotImplementedError
