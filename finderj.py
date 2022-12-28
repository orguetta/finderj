import argparse
import ssl
import textwrap
import concurrent.futures
import requests
import threading

def find_subdomain(domain, word):
  subdomain = f'https://{word}.{domain}'
  try:

    session = requests.Session()

    session.timeout = 5

    response = session.get(subdomain)
    if response.status_code == 200:

      if domain in response.text:
        print(f'{subdomain} {response.status_code}')
      else:
        pass
    else:
      print(f'{subdomain} {response.status_code}')
  except Exception as e:
    pass
  
def main(domain, wordlist, threads):
  words = wordlist.splitlines()
  with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    for word in words:
      executor.submit(find_subdomain, domain, word)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='finding subdomains',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples:
        finderj.py -d example.com -w <your_wordlist> -t <Number_of_Threads>
        '''))

    parser.add_argument('-d', '--domain', required=True, help='target Domain')
    parser.add_argument('-w', '--wordlist', help='your wordlist')
    parser.add_argument('-t', '--threads', default=15, type=int, help='number of threads. (default=15)')
    args = parser.parse_args()

    with open(args.wordlist) as f:
      wordlist = f.read()
      main(args.domain, wordlist, args.threads)


