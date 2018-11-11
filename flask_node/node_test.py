import threading

from flask_node.nodes import Node, SensorNode, ActionNode


node = Node("generic", port=5010)
sensor = SensorNode("sensor", port=5020)
action = ActionNode("action", port=5030)

def main():
    threads = [
        threading.Thread(target=node.run),
        threading.Thread(target=sensor.run),
        threading.Thread(target=action.run),
    ]

    for t in threads:
        t.start()

if __name__ == "__main__":
    main()
