import sqlite3
import http.cookiejar

cookieJar = http.cookiejar

def get_cookies(cj, ff_cookies):
    con = sqlite3.connect(ff_cookies)
    cur = con.cursor()
    cur.execute("SELECT creation_utc, host_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent FROM cookies")
    # for item in cur.fetchall():
    #     c = http.cookiejar.Cookie(0, item[4], item[5],
    #         None, False,
    #         item[0], item[0].startswith('.'), item[0].startswith('.'),
    #         item[1], False,
    #         item[2],
    #         item[3], item[3]=="",
    #         None, None, {})
    #
    #     print(c)
    #     cj.set_cookie(c)
    print([item for item in cur.fetchall()][0])

get_cookies(cookieJar, r"C:\Users\omaro\Downloads\Cookies")
