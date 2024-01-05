"""Является суррогатом другого объекта и контролирует доступ к нему"""


import time


class SalesManager:
    def talk(self) -> None:
        print('Sales manager ready to service you!')


class Proxy:
    def __init__(self) -> None:
        self.busy = False
        self.sales = None

    def talk(self) -> None:
        time.sleep(.1)
        if self.busy:
            print('Sales manager is busy')
        else:
            self.sales = SalesManager()
            self.sales.talk()


class NoTalkProxy(Proxy):
    def talk(self):
        print("Proxy checking for Sales Manager availability")
        time.sleep(.1)
        print(
            "This Sales Manager will not talk to you",
            "whether he/she is busy or not"
        )


if __name__ == '__main__':
    p = Proxy()
    p.talk()
    p.busy = True
    p.talk()
    p = NoTalkProxy()
    p.talk()
    p.busy = True
    p.talk()
