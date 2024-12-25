import json
import time
import traceback
from resolver import NamesiloResolver
from req import req
from log import logger


RESOLVER_DICT = {
    "NamesiloResolver": NamesiloResolver,
}


def get_current_ip(ip_version: int = 4):
    try:
        r = req(url=f"http://echov{ip_version}.irid.cc:8080")
    except Exception as error:
        logger.warning(f"get_current_ip error: make sure you can access {ip_version=} network! {error=}")
        return

    logger.info(f"get_current_ip: {ip_version=} {r.text}")
    return r.text


def check_and_update(ip: str, resolve_type: str, resolve_infos: list):
    for resolve_info in resolve_infos:
        if resolve_info["resolve_type"] != resolve_type:
            continue

        resolver = RESOLVER_DICT[resolve_info["Resolver"]](
            domain=resolve_info["domain"],
            resolve_type=resolve_info["resolve_type"],
            key=resolve_info["key"],
            ttl=resolve_info["ttl"]
        )

        if resolver.ip != ip:
            logger.info(f"{resolver} ip changed updating {ip=} ...")
            resolver.update(ip)
            logger.info(f"{resolver} updated")
        else:
            logger.info(f"{resolver} ip unchanged pass.")


def run():
    with open('conf/conf.json', 'r', encoding='utf-8') as fp:
        config = json.load(fp)

    ip4, ip6 = get_current_ip(), get_current_ip(ip_version=6)
    if not ip4 and not ip6:
        raise Exception(f"current ip not available: {ip4=} {ip4=}")

    if ip4:
        check_and_update(ip4, "A", config["resolver_infos"])

    if ip6:
        check_and_update(ip6, "AAAA", config["resolver_infos"])
    logger.info(f"will check agin after {config['wait_minute_pre_check']} minute.")
    time.sleep(config["wait_minute_pre_check"] * 60)


if __name__ == '__main__':
    while True:
        try:
            while True:
                run()
        except Exception:
            error = traceback.format_exc()
            logger.error(f"unknown exception: {error}")
            time.sleep(60 * 30)
