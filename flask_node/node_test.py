import threading
from flask import Flask

from flask_node.nodes import Node


slave = Node("slave", port=5020)
master = Node("master", port=5010)

def main():
    threads = [
        threading.Thread(target=slave.run),
        threading.Thread(target=master.run),
    ]

    for t in threads:
        t.start()

if __name__ == "__main__":
    main()
