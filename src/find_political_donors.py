#!/usr/bin/env python

from numpy import median
import heapq
import sys
import math
import datetime

def checkDate(dateString):
	is_valid_date = None
	try:
	    processed = datetime.datetime.strptime(dateString, '%m%d%Y')
	    is_valid_date = True
	except ValueError:
	    is_valid_date = False
	return is_valid_date

def addToDictAndIncrement(guid, item_dict, increment):
	if guid not in item_dict:
		item_dict[guid] = increment
	else:
		item_dict[guid] += increment

# Using streamMedian function to calculate running median from
# http://www.ardendertat.com/2011/11/03/programming-interview-questions-13-median-of-integer-stream/
class streamMedian:
	def __init__(self):
		self.minHeap, self.maxHeap = [], []
		self.N=0
 
	def insert(self, num):
		if self.N%2==0:
			heapq.heappush(self.maxHeap, -1*num)
			self.N+=1
			if len(self.minHeap)==0:
				return
			if -1*self.maxHeap[0]>self.minHeap[0]:
				toMin=-1*heapq.heappop(self.maxHeap)
				toMax=heapq.heappop(self.minHeap)
				heapq.heappush(self.maxHeap, -1*toMax)
				heapq.heappush(self.minHeap, toMin)
		else:
			toMin=-1*heapq.heappushpop(self.maxHeap, -1*num)
			heapq.heappush(self.minHeap, toMin)
			self.N+=1

	def getMedian(self):
		if self.N%2==0:
			return (-1*self.maxHeap[0]+self.minHeap[0])/2.0
		else:
			return -1*self.maxHeap[0]

def processInput(argv):
	output_median_zip = open(argv[2], 'w')
	output_median_date = open(argv[3], 'w')

	rolling_median_dict, num_trans_dict, total_amt_dict  = {}, {}, {}
	date_median_dict, date_trans_dict, date_amt_dict = {}, {}, {}

	with open(argv[1]) as f:
		for line in f:
			entry = line.split('|')
			cmte_id = entry[0]
			zipcode = entry[10][:5]
			transaction_dt = entry[13]
			transaction_amt = entry[14]
			other_id = entry[15]
			if not other_id and cmte_id and transaction_amt:
				if zipcode and len(zipcode) == 5: 
					guid = '_'.join([cmte_id, zipcode])
					if guid not in rolling_median_dict:
						rolling_median_dict[guid] = streamMedian()
					rolling_median_dict[guid].insert(float(transaction_amt))
					
					rolling_median = rolling_median_dict[guid].getMedian()
					rolling_median = math.ceil(rolling_median) if rolling_median % 1 >= .5 else math.floor(rolling_median)
					
					addToDictAndIncrement(guid, num_trans_dict, 1)
					addToDictAndIncrement(guid, total_amt_dict, float(transaction_amt))

					output_median_zip.write(''.join([cmte_id, '|', zipcode, '|', str(int(rolling_median)),
						'|', str(num_trans_dict[guid]), '|', str(int(total_amt_dict[guid])), '\n']))

				if transaction_dt and checkDate(transaction_dt):
					guid_date = '_'.join([cmte_id,transaction_dt])
					if guid_date not in date_median_dict:
						date_median_dict[guid_date] = [float(transaction_amt)]
					else:
						date_median_dict[guid_date].append(float(transaction_amt))

					addToDictAndIncrement(guid_date, date_trans_dict, 1)
					addToDictAndIncrement(guid_date, date_amt_dict, float(transaction_amt))

	sorting_items = []
	for key in date_median_dict.keys():
		sorting_items.append(key.split('_'))
	sorted_items = sorted(sorted(sorting_items, key = lambda x : x[0]),
		key=lambda x: datetime.datetime.strptime(x[1], '%m%d%Y'), reverse = True)

	for item in sorted_items:
		reformed_key = '_'.join(item)
		calc_date_median = median(date_median_dict[reformed_key])
		calc_date_median = math.ceil(calc_date_median) if calc_date_median % 1 >= .5 else math.floor(calc_date_median)
		
		output_median_date.write(''.join([item[0], '|', item[1], '|', str(int(calc_date_median)), '|',
			str(date_trans_dict[reformed_key]), '|', str(int(date_amt_dict[reformed_key])), '\n']))

	output_median_zip.close()
	output_median_date.close()

def main(argv):
	try:
		if not len(argv) == 4:
			raise ValueError('Invalid user input, please check arguments')
		processInput(argv)
	except ValueError as e:
		print(e)

if __name__ == "__main__":
    main(sys.argv)