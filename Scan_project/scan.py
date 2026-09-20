import socket
import threading
import csv
import argparse


results = []
lock = threading.Lock()

def scan(ip, port):
    s=socket.socket()
    s.settimeout(0.5)
    try:
        s.connect((ip,port))
        return True
    except:
        return False
    finally:
        s.close()


def scan_and_save(ip, port):
    # 你写：调用 scan，开放就加锁 append 到 results
    if scan(ip, port):
        with lock:
            results.append(port)
            print(f"端口{port}开放")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="端口扫描器")
    parser.add_argument("ip", help="目标IP")
    parser.add_argument("-p", "--ports", default="1-100", help="端口范围，如 1-1000")
    parser.add_argument("-o", "--output", default="result.csv", help="输出CSV文件")
    args = parser.parse_args()

    ip = args.ip
    start, end = args.ports.split("-")  # 按-分割
    start = int(start)
    end = int(end)

    threads = []
    # 你写：创建线程、start、加入列表
    for port in range(start, end + 1):
        t = threading.Thread(target=scan_and_save, args=(ip, port))
        t.start()
        threads.append(t)


    for t in threads:
        t.join()
        # 你写：join
    print("开放端口：", results)

    # 把 results 写进 result.csv
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["端口", "状态"])
        for port in results:
            writer.writerow([port, "开放"])
