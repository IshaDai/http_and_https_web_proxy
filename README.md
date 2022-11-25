# Web Proxy
A web-proxy is a simple web-client and web-server wrapped in a single application. It receives requests from one or more
clients (web-browsers) for particular content URLs, and forwards them on to the intended server, then returns the result
to your web-browser in some form. Proxy server in Python can not only handle HTTP/HTTPS requests, but also can provide
logging for debugging purpose.


## Getting Started
Without the use of any external web/http-related libraries, sockets are opened in the standard socket() API way. 


### Usage Approache
Step 1: Download it

Step 2: Configure the proxy settings for your web brower

Step 3: Good to start

**For Firefox:**
* Go to Options, find the `Settings` and choose `Network Settings` tab. Or, you can just type `proxy` in your search bar;
* Then, select `Manual proxy configuration`. Enter `localhost` or `127.0.0.1` into the HTTP Proxy, and enter `8080` for the Port;
* Also, check `Also use this proxy for HTTPS`;
* Finally, click the `OK`.

**For Internet User:**
* Download FireFox and operate the above step


## Built With
* Socket
* Python 3.7


## Description and Bugs
Works well for HTTPS websites, for example, users can do google search (i.e. type `www.google.com` into the search bar) 
or search other https website (just like users normally use). Besides, you can do multiple web browsing simultaneously.

Moreover, it works for HTTP website link; however, a small part of HTTP pages cannot be displayed properly. For instance,
`http://www.parksaustralia.gov.au/botanic-gardens/plan/cafe.html`. Still not fix this bug. To get access to the website,
`http://comp3310.ddns.net/`, you can just type `localhost:8080` or `comp3310.ddns.net`.


## Author

Luqiao Dai


## Reference 
1. https://docs.python.org/3/library/stdtypes.html
2. https://www.runoob.com/html/html-basic.html
3. https://blog.csdn.net/u011522841/article/details/105277700/ 
4. https://cgg.mff.cuni.cz/gitlab/martinm/aproxy/-/raw/090d41bc0fa72e8a828f5937537c39b407115a42/proxy_server.py
5. https://reverland.github.io/python/2014/01/29/python/
