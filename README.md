# 403to404checker
A Python script to identify URLs that return a 403 status code on the root path and a 404 status code on the /test path. The script processes a list of target URLs or a single domain, optionally saving matching URLs to an output file.

**Prerequisites:**

- https://github.com/reewardius/bbFuzzing.txt
- Python 3.6+
- Required Python packages: `requests`, `urllib3`:
```
pip install requests urllib3
```
### Example Workflow
The script can be used as part of a larger reconnaissance pipeline:

1. Filter URLs with HTTP 403/401 using `httpx`:

```bash
httpx -l alive_http_services.txt -mc 403,401 -o 40X.txt
```
2. Run 403to404checker:
```bash
python3 403to404checker.py -f 40X.txt -o 404_results.txt
```
3. Fuzz the results using `ffuf`:
```bash
ffuf -u URL/TOP -w 404_results.txt:URL -w top.txt:TOP -ac -mc 200 -o fuzz_results.json -fs 0 && \
python3 delete_falsepositives.py -j fuzz_results.json -o fuzz_output.txt -fp fp_domains.txt
```
