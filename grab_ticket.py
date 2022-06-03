from ticket_booker import *


def grab_ticket(chromedriver_path, account, password, account_type, day):
    get_quanrantine_hotel = BookQuanrantineHotel(chromedriver_path=chromedriver_path)
    get_quanrantine_hotel.login(account=account, password=password, account_type=account_type)
    get_quanrantine_hotel.reserve(day=day)


#  get_quanrantine_hotel = BookQuanrantineHotel(
#      chromedriver_path="/home/yyzhong/chromedriver_linux64/chromedriver"
#  )
#  get_quanrantine_hotel.login(account="CC5639520", password="zhong123456", account_type=2)
#  get_quanrantine_hotel.reserve(day=7)

grab_ticket(
    chromedriver_path="/home/yyzhong/chromedriver_linux64/chromedriver",
    account="CC5639520",
    password="zhong123456",
    account_type=2,
    day=7,
)
