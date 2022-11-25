import socket, sys, datetime, time, re
from _thread import start_new_thread

class Proxy:
    def __init__(self):
        self.host = '' # blank for localhost
        self.port = 8080
        self.buffsize = 4096

    # Helper Function to get current time as a Y-M-D H:M:S format.
    def getTimeStampp(self):
        # Get the current time by datetime.
        current = datetime.datetime.now()
        return ("[" + str(current.strftime('%Y-%m-%d %H:%M:%S')) + "]")

    # Add the statements into the file, and make it readable.
    def addRecord(self, msg):
        f = open("log/log.txt", "a+")
        f.write(msg)
        f.write("\n")

        # Trigger server
    def client_server(self):
        string = self.getTimeStampp() + " Proxy Server Running on Port: " + str(self.port)
        self.addRecord(string)
        print(string)

        try:
            sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket
            sck.bind((self.host, self.port)) # associate the socket to host and port
            sck.listen(10) # listenning
            self.addRecord(self.getTimeStampp() + " Start Listening ...")
            print(self.getTimeStampp() + " Start Listening ...")

            while True:
                try:
                    conn, address = sck.accept() # get the connection from client
                    start_new_thread(self.read_request, (conn, self.buffsize)) # create a thread to handle request

                except Exception as e: # cannot get the connection from client
                    self.addRecord(self.getTimeStampp() + " Cannot Establish Connection and Get Error Messages" + str(e))
                    print(self.getTimeStampp() + " Cannot Establish Connection and Get Error Messages" + str(e))
                    sys.exit(1)

        # termination
        except KeyboardInterrupt:
            self.addRecord(self.getTimeStampp() + " Server Interrupted ...")
            print(self.getTimeStampp() + " Server Interrupted ...")
            time.sleep(.5)
        finally:
            self.addRecord(self.getTimeStampp() + " Server Stop...")
            print(self.getTimeStampp() + " Server Stop...")
            sys.exit()

    # Function to read the request data
    def read_request(self, conn, max_buffersize):
        try:
            webserver = 'comp3310.ddns.net'
            port = 80
            hasOpened = False

            request = conn.recv(max_buffersize) # get the request from browser
            Head = request.split(b'\r\n')[0]

            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an another socket to connect to the web server
            new_socket.connect((webserver, port)) # connect to the server
            new_socket.send(request) # send request to web server

            # Stripping method to find if HTTP (GET ...) or HTTPS (CONNECT)
            method = request.split(b' ')[0]

            if method != b'CONNECT': # HTTP Case
                while True:

                    try:
                        eht_count = 0
                        web_data = new_socket.recv(max_buffersize) # receive data from web server

                        # Replace every instance of the word “the” in the body text with the word “eht” in bold
                        web_data= web_data.replace(b'the ', b'<b>eht </b>')
                        web_data = web_data.replace(b'The ', b'<b>eht </b>')

                        if (len(web_data) > 0):
                            # used to only print header once, and don't log other headers
                            if not hasOpened:
                                self.addRecord(self.getTimeStampp() + ' Http Links Connection Established')
                                print(self.getTimeStampp() + ' Http Links Connection Established')
                                self.addRecord(self.getTimeStampp() + ' HTTP Client-request: '+
                                      (Head.split(b' ')[0] + b' ' + Head.split(b' ')[2]).decode('utf-8'))
                                print(self.getTimeStampp() + ' HTTP Client-request: ' +
                                      (Head.split(b' ')[0] + b' ' + Head.split(b' ')[2]).decode('utf-8'))
                                hasOpened = True

                            conn.send(web_data) # send to browser
                            server_status_response = web_data.split(b'\r\n')[0].decode('utf-8')
                            # only print the string that starts with 'HTTP/'
                            if server_status_response.startswith('HTTP/'):
                                self.addRecord(self.getTimeStampp() + ' HTTP Server Server Status Response: ' + server_status_response[9:])
                                print(self.getTimeStampp() + ' HTTP Server Status Response: ' + server_status_response[9:])
                        else:
                            break

                        new_socket.settimeout(0.0)

                        eht_count += len(re.findall(b'<b>eht </b>', web_data))
                        time.sleep(1)
                        if eht_count > 0:
                            self.addRecord(self.getTimeStampp() + ' The number of the text changes now: ' + str(eht_count) + '\n')
                            print(self.getTimeStampp() + ' The number of the text changes now: '+ str(eht_count) + '\n')

                    except Exception as e:
                        pass


            else: # HTTPS Case
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ifrecord = False

                try:
                    # used to only print header once, and don't log other headers
                    if not ifrecord:
                        self.addRecord(self.getTimeStampp() + ' Https Links Connection Established')
                        print(self.getTimeStampp() + ' Https Links Connection Established')
                        self.addRecord(self.getTimeStampp() + ' HTTPS Client-request: '+
                              (Head.split(b' ')[0] + b' ' + Head.split(b' ')[2]).decode('utf-8'))
                        print(self.getTimeStampp() + ' HTTPS Client-request: ' +
                              (Head.split(b' ')[0] + b' ' + Head.split(b' ')[2]).decode('utf-8'))
                        ifrecord = True

                    # If successful, send 200 code response
                    header = request.split(b'\r\n')[0] # e.g. b'CONNECT googleads.g.doubleclick.net:443 HTTP/1.1'
                    url = header.split(b' ')[1] # b'googleads.g.doubleclick.net:443'

                    # Stripping Port and Domain
                    domain = url.split(b':')[0] # b'googleads.g.doubleclick.net'
                    port = int(url.split(b':')[1])  # 443
                    if port == '': port = 80 # if no port found, just use the general 80 port

                    s.connect((domain, port))
                    reply = "HTTP/1.1 200 OK\r\n"
                    reply += "\r\n"
                    conn.sendall(reply.encode())

                    self.addRecord(self.getTimeStampp() + ' HTTPS Server Status Response: ' + reply[9:])
                    print(self.getTimeStampp() + ' HTTPS Server Status Response: ' + reply[9:])

                    conn.setblocking(0)
                    s.settimeout(0.0)

                    while True:
                        try:
                            request = conn.recv(max_buffersize)
                            s.sendall(request)
                        except socket.error as err:
                            pass

                        try:
                            reply = s.recv(max_buffersize)

                            conn.sendall(reply)
                        except socket.error as e:
                            pass

                except socket.error as err:
                    pass

            new_socket.close()
            conn.close()

        except Exception as e:
            return


if __name__ == "__main__":
    server = Proxy()
    server.client_server()
