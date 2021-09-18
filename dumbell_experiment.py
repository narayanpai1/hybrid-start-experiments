from multiprocessing import Process

from nest.engine.exec import exec_subprocess
from nest.topology import *

TEST_DURATION = 10
AQM = "fq_codel" # the default queueing algorithm used in linux
TITLE = "without_hybrid_start"

client_router_latency = "12.5ms"
router_router_latency = "25ms"

client_router_bandwidth = "1000mbit"
bottleneck_bandwidth = "100mbit"

###### TOPOLOGY CREATION ######

# Creating nodes and routers for the dumbbell topology
left_node = Node("left-node")
left_router = Node("left-router")
right_router = Node("right-router")
right_node = Node("right-node")

# Enabling IP forwarding for the routers
left_router.enable_ip_forwarding()
right_router.enable_ip_forwarding()

print("Nodes and routers created")

# Add connections
left_node_connection = connect(left_node, left_router)
right_node_connection = connect(right_node, right_router)
(left_router_connection, right_router_connection) = connect(left_router, right_router)

print("Connections made")

###### ADDRESS ASSIGNMENT ######

# A subnet object to auto generate addresses in the same subnet
# This subnet is used for the left-node and the left-router
left_subnet = Subnet("10.0.0.0/24")

# Assigning addresses to the interfaces
left_node_connection[0].set_address(left_subnet.get_next_addr())
left_node_connection[1].set_address(left_subnet.get_next_addr())

# This subnet is used for the right-node and the right-router
right_subnet = Subnet("10.0.1.0/24")

right_node_connection[0].set_address(right_subnet.get_next_addr())
right_node_connection[1].set_address(right_subnet.get_next_addr())

# This subnet is used for the connections between the two routers
router_subnet = Subnet("10.0.2.0/24")

# Assigning addresses to the connections between the two routers
left_router_connection.set_address(router_subnet.get_next_addr())
right_router_connection.set_address(router_subnet.get_next_addr())

print("Addresses are assigned")

####### ROUTING #######

# If any packet needs to be sent from left-node, send it to left-router
left_node.add_route("DEFAULT", left_node_connection[0])

left_router.add_route(
    left_node_connection[0].get_address(), left_node_connection[1]
)

# If the destination address doesn't match any of the entries
# in the left-router's iptables forward the packet to right-router
left_router.add_route("DEFAULT", left_router_connection)

# If any packet needs to be sent from right-node, send it to right-router
right_node.add_route("DEFAULT", right_node_connection[0])

right_router.add_route(
    right_node_connection[0].get_address(), right_node_connection[1]
)

# If the destination address doesn't match any of the entries
# in the right-router's iptables forward the packet to left-router
right_router.add_route("DEFAULT", right_router_connection)

# Setting up the attributes for all the connections
left_node_connection[0].set_attributes(
    client_router_bandwidth, client_router_latency
)
left_node_connection[1].set_attributes(
    client_router_bandwidth, client_router_latency
)
right_node_connection[0].set_attributes(
    client_router_bandwidth, client_router_latency
)
right_node_connection[1].set_attributes(
    client_router_bandwidth, client_router_latency
)
left_router_connection.set_attributes(
    bottleneck_bandwidth, router_router_latency, AQM
)
right_router_connection.set_attributes(
    bottleneck_bandwidth, router_router_latency, AQM
)

results_dir = "results"

# Start running netserver on the right node
cmd = f"ip netns exec {right_node.id} netserver"
exec_subprocess(cmd)

# Start the flent test
dest_host_addr = right_node_connection[0].address.get_addr(with_subnet=False)

cmd = (
    f"ip netns exec {left_node.id} flent tcp_1up"
    f" --data-dir {results_dir}"
    f" --length {TEST_DURATION}"
    f" --step-size 0.05"
    f" --host {dest_host_addr}"
    f" --delay 0"
    f" --title-extra {TITLE}"
    " --socket-stats"
)
worker = Process(target=exec_subprocess, args=(cmd,))

print("\n🤞 STARTED FLENT EXECUTION 🤞\n")

worker.start()
worker.join()

print("\n🎉 FINISHED FLENT EXECUTION 🎉\n")
