import requests
from requests_futures.sessions import FuturesSession
from time import monotonic
import re
import json
from output import output

class userSearchFuturesSession(FuturesSession):
    def request(self, method, url, hooks=None, *args, **kwargs):
        if hooks is None:
            hooks = {}
        start = monotonic()

        def response_time(resp, *args, **kwargs):
            resp.elapsed = monotonic() - start

        if "response" in hooks:
            if isinstance(hooks["response"], list):
                hooks["response"].insert(0, response_time)
            elif callable(hooks["response"]):
                hooks["response"] = [response_time, hooks["response"]]
            else:
                hooks["response"] = [response_time]

        return super(userSearchFuturesSession, self).request(
            method, url, hooks=hooks, *args, **kwargs
        )

def interpolate_string(input_object, username):
    if isinstance(input_object, str):
        return input_object.replace("{}", username)
    elif isinstance(input_object, dict):
        return {k: interpolate_string(v, username) for k, v in input_object.items()}
    elif isinstance(input_object, list):
        return [interpolate_string(i, username) for i in input_object]
    return input_object

def get_response(request_future, error_type, social_network):
    response = None
    error_context = "General Error"
    exception_text = None

    try:
        response = request_future.result()
        if response.status_code:
            error_context = None
    except requests.exceptions.HTTPError as errh:
        error_context = "HTTP Error"
        exception_text = str(errh)
    except requests.exceptions.ProxyError as errp:
        error_context = "Proxy Error"
        exception_text = str(errp)
    except requests.exceptions.ConnectionError as errc:
        error_context = "Error Connecting"
        exception_text = str(errc)
    except requests.exceptions.Timeout as errt:
        error_context = "Timeout Error"
        exception_text = str(errt)
    except requests.exceptions.RequestException as err:
        error_context = "Unknown Error"
        exception_text = str(err)

    return response, error_context, exception_text

def UserNetSearcher(
    username,
    site_data,
    dump_response: bool = False,
    timeout=10,
):
    underlying_session = requests.session()
    max_workers = min(len(site_data), 20)
    session = userSearchFuturesSession(max_workers=max_workers, session=underlying_session)
    results_total = {}

    for social_network, net_info in site_data.items():
        results_site = {"url_main": net_info.get("urlMain")}
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
        }

        if "headers" in net_info:
            headers.update(net_info["headers"])

        url = interpolate_string(net_info["url"], username.replace(' ', '%20'))
        regex_check = net_info.get("regexCheck")

        if regex_check and re.search(regex_check, username) is None:
            results_site["status"] = "ILLEGAL"
            results_site["url_user"] = ""
            results_site["http_status"] = ""
            results_site["response_text"] = ""
        else:
            results_site["url_user"] = url
            url_probe = net_info.get("urlProbe", url)
            request_method = net_info.get("request_method", "GET")
            request_payload = net_info.get("request_payload")

            request = session.get if request_method == "GET" else session.head

            if request_payload is not None:
                request_payload = interpolate_string(request_payload, username)

            future = request(
                url=url_probe,
                headers=headers,
                allow_redirects=True,
                timeout=timeout,
                json=request_payload,
            )
            net_info["request_future"] = future

        results_total[social_network] = results_site

    for social_network, net_info in site_data.items():
        results_site = results_total.get(social_network)
        url = results_site.get("url_user")
        status = results_site.get("status")

        if status is not None:
            continue

        future = net_info["request_future"]
        r, error_text, exception_text = get_response(
            request_future=future, error_type=net_info["errorType"], social_network=social_network
        )

        if r is None:
            results_site["status"] = "UNKNOWN"
            results_site["http_status"] = "N/A"
            results_site["response_text"] = exception_text or "No response received"
            continue  
        http_status = r.status_code if r else None
        if http_status is None:
            results_site["status"] = "UNKNOWN"
            results_site["http_status"] = "N/A"
            results_site["response_text"] = "No response received"
            continue

        error_codes = net_info.get("errorCode", [])

        if not isinstance(error_codes, list):
            error_codes = [error_codes] if error_codes is not None else []
            
        error_msg = net_info.get("errorMsg")
        if error_msg and r is not None:
          if isinstance(error_msg, list):

              if any(msg in r.text for msg in error_msg):
                  results_site["status"] = "NOT_AVAILABLE"  # Usuario no existe
              else:
                  results_site["status"] = "FOUND"
          elif isinstance(error_msg, str):

              if error_msg in r.text:
                  results_site["status"] = "NOT_AVAILABLE"  # Usuario no existe
              else:
                  results_site["status"] = "FOUND"
        else:
            results_site["status"] = "FOUND"
                
        results_site["http_status"] = http_status
        results_site["response_text"] = r.text if dump_response else ""

    return results_total

username = input("\033[1;36mEnter user to search:\n\033[0m")
print("\033[1;33mSearching...\n\033[0m")
with open('data.json', 'r') as archivo:
    site_data = json.load(archivo)
print(output(username,UserNetSearcher(username, site_data)))
