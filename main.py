import requests
import configparser


def redeem_codes(game_code, pid, lang_cd, url_get, url_post, codes):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for code in codes:
        params = {
            'gameCode': game_code,
            'couponCode': code,
            'langCd': lang_cd,
            'pid': pid
        }
        response = requests.get(url_get, headers=headers, params=params)
        response_json = response.json()
        error_code = response_json.get('errorCode')

        if error_code == 200:
            print(
                f"\033[92mThe code {code} can be activated, prepare for second request.\033[0m")

            # Make a second POST request
            post_data = {
                'gameCode': game_code,
                'couponCode': code,
                'langCd': lang_cd,
                'pid': pid
            }
            post_response = requests.post(
                url_post, headers=headers, json=post_data)
            post_response_json = post_response.json()
            post_error_code = post_response_json.get('errorCode')

            if post_response.status_code == 200 and post_error_code == 200:
                print(
                    f"\033[92mThe code has been successfully activated and should be visible in your mails.\033[0m")
            else:
                print(
                    f"\033[91mSecond request failed for code {code}. Error code: {post_error_code}\033[0m")

        elif error_code == 24004:
            print(
                f"\033[95mThe code {code} has already been activated.\033[0m")
        elif error_code == 24003:
            print(
                f"\033[91mThe code {code} is expired or doesn't exist.\033[0m")
        elif response.status_code == 400 or response_json.get('httpStatus') == 400:
            print(
                f"\033[93mThe code {code} could not be activated. Error code: {error_code}\033[0m")
        else:
            print(
                f"\033[93mThe code {code} returned an unexpected status ({response.status_code}). Error code: {error_code}\033[0m")

    print("\033[94mAll the codes have been processed.\033[0m")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    game_code = config['DEFAULT']['game_code']
    pid = config['UID']['pid']
    lang_cd = config['DEFAULT']['lang_cd']
    url_get = config['DEFAULT']['url_get']
    url_post = config['DEFAULT']['url_post']
    codes = config['CODES']['codes'].split(', ')

    redeem_codes(game_code, pid, lang_cd, url_get, url_post, codes)
