import requests as rq

# import time as time_

# List not sorted proxy
proxy = r"proxy.txt"
filter_proxy = r"filter_proxy.txt"
# Your url
url = 'http://httpbin.org/ip'


# Open file as list proxy
with open(proxy) as pr, open(filter_proxy, 'w') as fpr:
    for ip in pr.readlines():
        test_pr = {'http': f'http://{ip.strip()}',
                   'https': f'https://{ip.strip()}'}
        # start = time_.perf_counter()
        try:
            resp = rq.get(url, proxies=test_pr, timeout=1)
            print(f'status {ip.strip()}: OK')
            fpr.write(f'{test_pr}\n')
        except:
            print(f'status {ip.strip()}: False')