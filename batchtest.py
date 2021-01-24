#!/usr/bin/env python3
#
# Copyright (c) 2021, Xuesong Wang
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from argparse import ArgumentParser

from dnseval import dnsping
import numpy as np
import pandas as pd

__author__ = 'Xuesong Wang (email: snowpine007@outlook.com)'
__license__ = 'BSD-2-Clause'
__version__ = "1.0.0"


def test_one_host_server(host, server, dnsrecord='A', timeout=2, count=5):
    _, r_avg, r_min, r_max, r_stddev, r_lost_percent, flags, ttl, answers = dnsping(host, server, dnsrecord, timeout, count)
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


def get_average_result(servers, hosts, dnsrecord, timeout, count, output, loss, stddev):
    result = np.zeros((len(servers), len(hosts)), dtype=float)
    drop_servers = dict()
    for i, server in enumerate(servers):
        for j, host in enumerate(hosts):
            if server in drop_servers:
                if verbose >= 2:
                    print(
                        f'{i * len(hosts) + j + 1}/{len(servers) * len(hosts)} Skip DNS server {server} due to '
                        f'{drop_servers[server]}.')
                break

            _, r_avg, r_min, r_max, r_stddev, r_lost_percent, ttl = test_one_host_server(host, server, dnsrecord,
                                                                                         timeout, count)
            if r_lost_percent >= loss or r_stddev >= stddev or r_avg == 0:
                drop_servers.update({server: ('loss is too high' if r_lost_percent >= loss else
                                              ('stddev is too high' if r_stddev >= stddev else 'connection failure'))})
                continue

            result[i, j] = r_avg
            if verbose >= 2:
                print(f'{i*len(hosts)+j+1}/{len(servers)*len(hosts)} Average speed by DNS server {server} to host {host}: {result[i, j]:.2f}s')

    table = pd.DataFrame(result, index=servers, columns=hosts)
    table['Average'] = table.mean(axis=1)
    columns = ['Average'] + hosts
    table = table.loc[:, columns]
    table.sort_values(by='Average', ascending=True, inplace=True)

    if drop_servers:
        table.drop(index=list(drop_servers.keys()), inplace=True)
        if verbose >= 1:
            print(
                f'Because some of the hosts are unreachable from the servers below, they are not listed in the final result.')
            print(drop_servers)

    table.to_excel(output)
    print("Based on the test results, the average speed of the DNS servers are:")
    print(table.loc[:, 'Average'])


if __name__ == '__main__':
    parser = ArgumentParser(prog='dnsbatchtest', description='run a DNS server batch test using a host list')
    parser.add_argument('-s', '--server', default='dns.txt', help='set the file to read the server list from, default: dns.txt')
    parser.add_argument('-H', '--host', default='hosts.txt', help='set the file to read the host list from, default: host.txt')
    parser.add_argument('-r', '--dnsrecord', default='A', help='set the DNS record type, default: "A"')
    parser.add_argument('-t', '--timeout', default=2, type=int, help='set the timeout limit, default: 2')
    parser.add_argument('-c', '--count', default=5, type=int, help='set the number of queries, default: 5')
    parser.add_argument('-V', '--version', action='version', version=f"%(prog)s {__version__}")
    parser.add_argument('-v', '--verbose', action='count', default=0, help='set the verbose level, default:0. When '
                                                                            'set to 0, only print the final result; set to 1, print the drop list if any; set to 2, print the intermediate result.')
    parser.add_argument('-o', '--output', default='result.xlsx', help='set the output file, default: result.xlsx')
    parser.add_argument('-L', '--loss', default=40, type=float, help='set the limit of loss, default: 40. In '
                                                                      'percentile. When loss > LOSS, the DNS server will be excluded from the final result.')
    parser.add_argument('-d', '--stddev', default=10, type=float, help='set the standard deviation limit, '
                                                                       'default: 10. When '
                                                            'stddev > STDDEV, the DNS server will be excluded from the final result.')

    args = parser.parse_args()

    servers = get_servers(args.server)
    hosts = get_hosts(args.host)
    verbose = args.verbose
    output = args.output
    dnsrecord = args.dnsrecord
    timeout = args.timeout
    count = args.count
    loss = args.loss
    stddev = args.stddev

    get_average_result(servers, hosts, dnsrecord, timeout, count, output, loss, stddev)
