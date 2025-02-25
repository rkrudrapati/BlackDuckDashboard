#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
# 'Authorization': 'Bearer {}'.format(self.token),

base_headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'X-Requested-With': "XMLHttpRequest",
    'Accept': "application/json, text/javascript, */*; q=0.01",
}


csrf_token = ''
auth_token = ''


def get_login_headers():
    login_headers = {
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept - Encoding': "gzip, deflate",
    }
    return login_headers


def get_login_headers_via_api():
    login_headers = {
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    }
    return login_headers


def get_request_headers():
    get_headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'Accept': "application/json",
        'X-CSRF-TOKEN': csrf_token,
        'cookie': auth_token
    }
    return get_headers


def post_request_headers():
    post_headers = {
        # 'Host': '8.8.8.8',
        'Content-Type': "application/json",
        # 'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'X-CSRF-TOKEN': csrf_token,
        'cookie': auth_token
    }
    return post_headers


def download_headers():
    download_headers = {
        'Content-Type': "application/zip",
        'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'cookie': auth_token
    }
    return download_headers


def delete_request_headers():
    delete_headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "en-US,en;q=0.5",
        # 'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'X-CSRF-TOKEN': csrf_token,
        'cookie': auth_token
    }
    return delete_headers


def post_report_headers():
    report_create_headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'X-CSRF-TOKEN': csrf_token,
        'cookie': auth_token
        }
    return report_create_headers


def put_request_headers():
    put_headers = {
        'Content-Type': "application/vnd.blackducksoftware.internal-1+json",
        'X-CSRF-TOKEN': csrf_token,
        'cookie': auth_token
    }
    return put_headers
