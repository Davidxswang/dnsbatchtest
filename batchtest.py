from dnseval import dnsping
import numpy as np
import pandas as pd

def test_one_host_server(host, server):
    server, r_avg, r_min, r_max, r_stddev, r_lost_percent, flags, ttl, answers = dnsping(host, server, 'A', 2, 5)
    return [server, r_avg, r_min, r_max, r_stddev, r_lost_percent, ttl]


def get_hosts(filename):
    with open(filename) as f:
        hosts = f.readlines()
    for i in range(len(hosts)):
        hosts[i] = hosts[i].strip()
    return hosts


def get_servers(filename):
    with open(filename) as f:
        servers = f.readlines()
    for i in range(len(servers)):
        servers[i] = servers[i].strip()
    return servers


if __name__ == '__main__':
    servers = get_servers('public-servers.txt')
    hosts = get_hosts('hosts.txt')
    result = np.zeros((len(servers), len(hosts)), dtype=float)
    for i, server in enumerate(servers):
        for j, host in enumerate(hosts):
            result[i, j] = test_one_host_server(host, server)[1]
            print(f'Finished server {server} to host {host}: {result[i, j]}')

    table = pd.DataFrame(result, index=servers, columns=hosts)
    table.to_csv('result.csv')