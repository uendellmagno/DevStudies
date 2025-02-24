import ntplib


class NTPServer:

    def __init__(self):
        self.time = None
        self.response = None
        self.client = None
        self.ntpservers = {'google': ['time.google.com', 'time1.google.com', 'time2.google.com', 'time3.google.com',
                                      'time4.google.com'],
                           'cloudflare': 'time.cloudflare.com',
                           'facebook': ['time.facebook.com', 'time1.facebook.com', 'time2.facebook.com',
                                        'time3.facebook.com', 'time4.facebook.com', 'time5.facebook.com'],
                           'apple': ['time.apple.com', 'time1.apple.com', 'time2.apple.com', 'time3.apple.com',
                                     'time4.apple.com', 'time5.apple.com', 'time6.apple.com', 'time7.apple.com',
                                     'time.euro.apple.com']}

    def get_time(self):
        self.client = ntplib.NTPClient()

        for key, servers in self.ntpservers.items():
            if isinstance(servers, str):
                servers = [servers]
            for server in servers:
                try:
                    self.response = self.client.request(server)
                    self.time = self.response.tx_time
                except:
                    print(f"couldn't get: {server}")
                    pass
                print(f"server is: {server}\nresponse is: {self.time}")


ntp_server = NTPServer()
ntp_server.get_time()
