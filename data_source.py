import json
from json2html import json2html
from typing import Any


def _main():
    web_confing = json.load(open('conf_jun.json'))

    policies = get_policies(web_confing)
    table_policies = convert_to_table(policies)
    table_policies_with_keys = add_keys_to_table(table_policies)

    html_policies = convert_to_html(policies)
    html_table = convert_to_html(table_policies_with_keys)
    csv_table = convert_to_csv(table_policies)

    save_to_file(html_policies, 'policies.html')
    save_to_file(html_table, 'table.html')
    save_to_file(csv_table, 'table.csv')


def get_policies(web_config) -> list[dict[str, Any]]:
    # ключь: имя сетевого интефейса
    # значение: destination address
    addresses = {}
    for addr in web_config["configuration"]["security"]["address-book"][0]["address"]:
        if "ip-prefix" in addr:
            ip = addr["ip-prefix"]
        elif "dns-name" in addr:
            ip = addr["dns-name"][0]["name"]
        elif "range-address" in addr:
            ip = addr["range-address"][0]["name"]
        else:
            raise Exception(f"Получили непредвиденное значение ip: {addr}")
        addresses.update({addr["name"]: ip})

    # ключь: данного словаря являются destination address,
    # значение: список destination ip
    address_set = {}
    for addr in web_config["configuration"]["security"]["address-book"][0]["address-set"]:
        address_set.update({addr["name"]: [d["name"] for d in addr["address"]]})

    policies = []

    policy_12 = (web_config["configuration"]["security"]["policies"]["global"]["policy"][30]["match"])
    policy_12.pop("destination-address-excluded")
    for policy in web_config["configuration"]["security"]["policies"]["global"]["policy"]:
        policy.update(policy.pop("match"))

        policy["then"] = list(policy["then"].keys())[0]
        if "from-zone" not in policy:
            policy.update({"from-zone": "-"})
        if "to-zone" not in policy:
            policy.update({"to-zone": "-"})

        source_addreses = policy["source-address"]
        ips2 = []
        for addr_name in source_addreses:
            if addr_name in address_set:
                names = address_set[addr_name]
                for web_name in names:
                    ips2.append(addresses[web_name])
            else:
                if addr_name in addresses:
                    ips2.append(addresses[addr_name])
                else:
                    ips2.append("any")
            policy.update({"source-ip": ips2})
        destination_addreses = policy["destination-address"]
        ips = []
        for addr_name in destination_addreses:
            if addr_name in address_set:
                names = address_set[addr_name]
                for web_name in names:
                    ips.append(addresses[web_name])
            else:
                if addr_name in addresses:
                    ips.append(addresses[addr_name])
                else:
                    ips.append("any")
            policy.update({"destination-ip": ips})
        policy.update({"source-address": policy.pop("source-address")})
        policy.update({"source-ip": policy.pop("source-ip")})
        policy.update({"destination-address": policy.pop("destination-address")})
        policy.update({"destination-ip": policy.pop("destination-ip")})
        policy.update({"application": policy.pop("application")})
        policy.update({"from-zone": policy.pop("from-zone")})
        policy.update({"to-zone": policy.pop("to-zone")})
        policy.update({"then": policy.pop("then")})

        policies.append(policy)

    return policies


def convert_to_html(data) -> str:
    return json2html.convert(json=data)  # type: ignore


def convert_to_table(data) -> list[list[str]]:
    header = list(data[0].keys())
    table = [header]

    for policy in data:
        row = []

        name = policy["name"]
        source_addrs = policy["source-address"]
        ips2 = policy["source-ip"]
        dest_addrs = policy["destination-address"]
        ips = policy["destination-ip"]
        apps = policy["application"]
        from_zones = policy["from-zone"]
        to_zones = policy["to-zone"]
        then = policy["then"]

        for sa in source_addrs:
            for si in ips2:
                for da in dest_addrs:
                    for ip in ips:
                        for app in apps:
                            for fz in from_zones:
                                for tz in to_zones:
                                    row = [name, sa, si, da, ip, app, fz, tz, then]
                                    table.append(row)

    return table


def convert_to_csv(data: list[list[str]]) -> str:
    return '\n'.join([','.join(row) for row in data])


def add_keys_to_table(table: list[list[str]]):
    header = table.pop(0)
    new_table = []

    for row in table:
        policy = {}
        for title, value in zip(header, row):
            policy.update({title: value})
        new_table.append(policy)

    return new_table


def save_to_file(data: str, path: str) -> None:
    with open(path, 'w') as out:
        out.write(data)


if __name__ == '__main__':
    _main()
