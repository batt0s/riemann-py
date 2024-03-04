# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:26:18 2024

@author: kerem (batt0s)
"""

from flask import Flask
from flask import render_template, request
from uuid import uuid4
from integral import riemann_alt_gorsel, riemann_ust_gorsel, NotInDomainError

app = Flask("riemann", static_folder="img/")

@app.route("/")
def index():
    if request.method != "GET":
        return "Method Not Allowed", 405
    
    args = request.args
    f = args.get("f", None)
    a = args.get("a", None)
    b = args.get("b", None)
    N = args.get("N", None)
    if None in [f, a, b, N]:
        return render_template("index.html")
    N = int(N)

    id = uuid4()
    
    try:
        alt_path = riemann_alt_gorsel(f, a, b, N, f"img/alt_{id}.png")
        ust_path = riemann_ust_gorsel(f, a, b, N, f"img/ust_{id}.png")
    except NotInDomainError:
        return render_template("index.html",
                               error="Verilen fonksiyon verilen aralıkta tanımlı değil.")
    
    hostname = request.host_url
    alt_url = hostname + alt_path
    ust_url = hostname + ust_path
    
    return render_template("index.html", alt_url=alt_url, ust_url=ust_url)
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="port number")
    args = parser.parse_args()
    app.run(debug=True, port=args.port)
    