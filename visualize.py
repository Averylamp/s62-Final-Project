import pickle
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import graphviz

def mine_rate_info(endpoint_block, origin_block, block_information, time_interval):
	endpoint_dt = datetime.fromtimestamp(highest_block[0]['timestamp'])
	origin_dt = datetime.fromtimestamp(block_information[origin_block]['timestamp'])
	block_hash = endpoint_block

	num_buckets = int((endpoint_dt - origin_dt).total_seconds() / time_interval) + 1
	mined_buckets = [0]*num_buckets
	times_list = [origin_dt + timedelta(seconds=x*time_interval) for x in range(0, num_buckets)]
	assert len(times_list) == len(mined_buckets)

	while block_hash != '':
		block_info = block_information[block_hash]
		timestamp = block_information[block_hash]['timestamp']
		dt = datetime.fromtimestamp(timestamp)
		bucket_ind = int((dt - origin_dt).total_seconds() / time_interval)
		mined_buckets[bucket_ind] += 1

		block_hash = block_info['blockInformation']['previousHash']

	return times_list, mined_buckets

def aggregate_info(mined_buckets):
	num_buckets = len(mined_buckets)
	aggregate_buckets = [0]*num_buckets

	for i in range(num_buckets):
		if i == 0:
			aggregate_buckets[0] = mined_buckets[0]
		else:
			aggregate_buckets[i] = aggregate_buckets[i-1] + mined_buckets[i]
	return aggregate_buckets

def generate_graphviz(block_information):
	g = graphviz.Digraph('G', filename='block_information.gv')
	g.node("origin", "")
	for block_hash in block_information:
		g.node(block_hash, "")
		prev_hash = block_information[block_hash]['blockInformation']['previousHash']
		if prev_hash == '':
			prev_hash = "origin"
		g.edge(prev_hash, block_hash)
	g.view()

block_information = pickle.load(open("block_information.pickle", 'rb'))
highest_block = pickle.load(open("highest_block.pickle", 'rb'))

print("Creating graphviz...")
generate_graphviz(block_information)
print("Done.")

# block height 0: 6c179f21e6f62b629055d8ab40f454ed02e48b68563913473b857d3638e23b28
origin_block = "6c179f21e6f62b629055d8ab40f454ed02e48b68563913473b857d3638e23b28"
endpoint_block = highest_block[0]['blockHash']

time_interval = 60 # seconds

times_list, mined_buckets = mine_rate_info(endpoint_block, origin_block, block_information, time_interval)
aggregate_buckets = aggregate_info(mined_buckets)

print("Plotting data...")
line1, = plt.plot(times_list, mined_buckets, label="blocks mined / {}s".format(time_interval))
line2, = plt.plot(times_list, aggregate_buckets, label="total blocks mined")
plt.legend(handles=[line1, line2])
plt.show()
print("Done")