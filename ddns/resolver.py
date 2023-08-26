from math import inf
import xmltodict
import tldextract
from req import req
from log import logger


class Resolver:
    def __init__(self, domain: str, resolve_type: str, key=str, ttl: int = 7000, ) -> None:
        self.domain = domain
        self.resolve_type = resolve_type
        self.ttl = ttl
        self.key = key
        self.ip = ""
        logger.info(f"{self} sync_ip... ")
        self.ip = self.get_resolve_ip()
        logger.info(f"{self}")

    def get_resolve_ip(self) -> str:
        """sync remote ip, raise if resolve recode not exists

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"Resolver:{self.__class__.__name__} domain:{self.domain} resolve_type:{self.resolve_type} ip:{self.ip}"

    def update(self, ip: str):
        """update resolve ip

        Args:
            ip (str): ip address

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()


class NamesiloResolver(Resolver):
    api_url = "https://www.namesilo.com/api"

    def __init__(self, domain: str, resolve_type: str, key=str, ttl: int = 7000,) -> None:
        ext = tldextract.extract(domain)
        self.main_domain = f"{ext.domain}.{ext.suffix}"
        self.sub = ext.subdomain
        super().__init__(domain, resolve_type=resolve_type, key=key, ttl=ttl)

    def get_resolve_ip(self):
        r = req(
            url=self.api_url + '/dnsListRecords',
            data={
                "version": 1,
                "type": "xml",
                "key": self.key,
                "domain": self.main_domain,
            }
        )
        resp = xmltodict.parse(r.text)

        if resp['namesilo']['reply']["code"] != "300":
            raise Exception(resp['namesilo']['reply']["detail"])

        infos = resp['namesilo']['reply']["resource_record"]
        infos = [infos] if isinstance(infos, dict) else infos
        for info in infos:
            if info["type"] == self.resolve_type and info["host"] == self.domain:
                self.record_id = info["record_id"]
                return info["value"]
        else:
            raise Exception(f"Resolve Not Fond: {self}")

    def update(self, ip):
        r = req(url=self.api_url + '/dnsUpdateRecord', data={
            "version": 1,
            "type": "xml",
            "rrttl": self.ttl,
            "key": self.key,
            "domain": self.main_domain,
            "rrid": self.record_id,
            "rrhost": self.sub,
            "rrvalue": ip,
        })
        resp = xmltodict.parse(r.text)

        if resp['namesilo']['reply']["code"] != "300":
            raise Exception(resp['namesilo']['reply']["detail"])
