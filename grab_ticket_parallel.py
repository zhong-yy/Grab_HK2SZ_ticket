from ticket_booker import *
import multiprocessing as mp
import sys
import os
from os.path import expanduser


def grab_ticket(chromedriver_path, account, password, account_type, day):
    get_quanrantine_hotel = BookQuanrantineHotel(chromedriver_path=chromedriver_path)
    get_quanrantine_hotel.login(account=account, password=password, account_type=account_type)
    get_quanrantine_hotel.reserve(day=day)


def grab_ticket_parallel(num_processes, chromedriver_path, account, password, account_type, day):
    processes = []
    for _ in range(num_processes):
        proc = mp.Process(
            target=grab_ticket,
            args=(chromedriver_path, account, password, account_type, day),
        )
        processes.append(proc)

    for proc in processes:
        print(f"Starting {proc.name}")
        proc.start()
        print(f"{proc.name} started")

    # wait for all processes to complete
    for proc in processes:
        print(f"Is {proc.name} alive? {proc.is_alive()}")
        proc.join()
        print(f"Joining {proc.name} ...")
        print(f"Finished joining {proc.name}")


if __name__ == "__main__":
    day = int(sys.argv[1])
    num_processes = int(sys.argv[2])
    home_dir = expanduser("~")
    print(f"使用{num_processes}个进程，抢第{day}天的票")
    grab_ticket_parallel(
        num_processes=num_processes,
        chromedriver_path=os.path.join(home_dir, "chromedriver_linux64/chromedriver"),
        account="CC5639520",
        password="zhong123456",
        account_type=2,
        day=day,
    )
