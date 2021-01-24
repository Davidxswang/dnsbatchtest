
DNS Batch Test Tool
==================================================

This tool is based on **Babak Farrokhi**'s project [dnsdiag](https://github.com/farrokhi/dnsdiag). The main purpose of this tool is to do a batch test on the target machine to see which DNS server(s) might be better. The usage is simple, but the result is powerful.

# installation

You can checkout this git repo and run:

```shell script
git clone https://github.com/Davidxswang/dnsbatchtest
cd dnsbatchtest
pip3 install -r requirements.txt
```

# batchtest

batchtest is based on dnseval. It sends arbitrary DNS queries to multiple DNS servers using multiple hosts. Because the well-known reason in China, trying multiple hosts is helpful. All DNS servers are located in China. But you may change the host list and server list, which are contained in [dns.txt](dns.txt) and [hosts.txt](hosts.txt). Usages:

```shell script
python batchtest.py
```

# dnseval
dnseval is a bulk ping utility that sends an arbitrary DNS query to a give list
of DNS servers. This script is meant for comparing response time of multiple
DNS servers at once. Usage:

```shell script
python dnseval.py -t A -f dns.txt -c10 yahoo.com
```

### Author

Part of the code is from the [dnsdiag](https://github.com/farrokhi/dnsdiag) project by Babak Farrokhi, which is licensed by a BSD-2-Clause license. Refer to the [LICENSE](LICENSE).

The change made on the [dnsdiag](https://github.com/farrokhi/dnsdiag) project is by Xuesong Wang, which is also licensed by a BSD-2-Clause license. Refer to [batchtest.py](batchtest.py).

### License

dnsbatchtest is released under a [BSD-2-Clause license](LICENSE).
