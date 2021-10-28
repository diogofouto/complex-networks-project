import matplotlib.pyplot as plt
import numpy as np
import random

# util functions

"""
Given a list of opinions, returns a list of every opinion rounded, to get either A or B
"""
def roundOpinions(opList):
	for i in range(len(opList)):
		opList[i] = round(opList[i])

	return opList

"""
Given a list of list of opinions, returns a list of lists where every opinion is flatted
"""
def roundTimestepOpinions(opListList):
	for i in range(len(opListList)):
		opListList[i] = roundOpinions(opListList[i])

	return opListList

def countOpinions(opList):
	opList = roundOpinions(opList)

	A = 0
	B = 0

	for val in opList:
		if(val == 0):
			A += 1
		else:
			B += 1
	return [A,B]

def countAllOpinions(opListList):
	for i in range(len(opListList)):
		opListList[i] = countOpinions(opListList[i])

	return opListList

# graph drawing functions

"""
Draws a graph with the cummulative opinions over time
"""
def drawCumRoundedOpinions(opListList):
	opListList = countAllOpinions(opListList)

	labels = []
	a = []
	b = []
	print(opListList)
	for i in range(len(opListList)):
		a += [opListList[i][0]]
		b += [opListList[i][1]]
		labels += [str(i)]

	x = np.arange(len(labels))  # the label locations
	width = 0.35  # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(x - width/2, a, width, label='Opinion A')
	rects2 = ax.bar(x + width/2, b, width, label='Opinion B')

	ax.set_ylabel('Opinions')
	ax.set_title('Opinions by timestep')
	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	ax.legend()

	fig.tight_layout()

	plt.show()

"""
Given a list of lists with opinions, shows how the polarization in opinions
0-0.25, strongly attatched for A
0.25-0.5, weakly attatched for A
...
"""
def showPolarizationBars(opListList):
	results = {}

	# For each timestep
	for i in range(len(opListList)):
		split = [0,0,0,0,0]

		#for each node i
		for op in opListList[i]:
			if(op < 0.2):
				split[0]  += 1
			elif(op < 0.4 and op >= 0.2):
				split[1] += 1
			elif(op < 0.6 and op >= 0.4):
				split[2] += 1
			elif(op < 0.75 and op >= 0.5):
				split[3] += 1
			else:
				split[4] += 1
			print(op, split)
		print(i)
		results["Timestep "+str(i)] = split

	category_names = ['Strongly attached to A', 'Weakly attached to A', 'Not defined',
				'Weakly attached to B', 'Strongly attached to B']

	labels = list(results.keys())
	data = np.array(list(results.values()))
	data_cum = data.cumsum(axis=1)
	category_colors = plt.get_cmap('RdYlGn')(
	np.linspace(0.15, 0.85, data.shape[1]))

	fig, ax = plt.subplots(figsize=(9.2, 5))
	ax.invert_yaxis()
	ax.xaxis.set_visible(False)
	ax.set_xlim(0, np.sum(data, axis=1).max())

	for i, (colname, color) in enumerate(zip(category_names, category_colors)):
		widths = data[:, i]
		starts = data_cum[:, i] - widths
		rects = ax.barh(labels, widths, left=starts, height=0.5,
						label=colname, color=color)

		r, g, b, _ = color
		text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
		#ax.bar_label(rects, label_type='center', color=text_color)
	ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
			loc='lower left', fontsize='small')
	
	plt.show()

"""
Makes a scatter plot with the current opinions
"""
def plotOpinions(opListList):
	X = []
	Y = []

	for i in range(len(opListList)):
		for val in opListList[i]:
			# X adds a bit of noise, so numbers dont overlap so quickly!
			X.append(i + random.uniform(-0.01, 0.01))
			Y.append(val)
			
	plt.xticks(range(len(opListList)))
	plt.yticks([0,0.25,0.5,0.75,1])
	plt.scatter(X,Y,c=Y,cmap='plasma',vmin=0,vmax=1)
	plt.show()

"""
Plots a single prejudice matrix of format
[[AA,AB],[BA, BB]]
Where each value corresponds to the percieved chance of the other player collaborating 
"""
def plotPrejudice(matrix):
	labels = ['AA', 'AB', 'BA', 'BB']
	means = [matrix[0][0], matrix[0][1], matrix[1][0],matrix[1][1]]

	x = np.arange(len(labels))  # the label locations
	width = 0.35  # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(x - width/2, means, width)

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Percieved chance of the other player collaborating')
	ax.set_title('Percieved chance of the other player collaborating by player and opponent opinion')
	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	ax.legend()

	ax.bar_label(rects1, padding=3)

	fig.tight_layout()

	plt.show()

"""
Same as plot prejudice, but comparing between having the same, and having a different opinion
"""
def plotPrejudiceComparison(matrix):
	labels = ['Same Opinion', 'Different Opinion']
	A_means = [matrix[0][0],matrix[0][1]]
	B_means = [matrix[1][1],matrix[1][0]]

	x = np.arange(len(labels))  # the label locations
	width = 0.35  # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(x - width/2, A_means, width, label='Opinion A')
	rects2 = ax.bar(x + width/2, B_means, width, label='Opinion B')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Percieved chance of the other player collaborating')
	ax.set_title('Percieved chance of the other player collaborating by player and opponent opinion')
	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	ax.legend()

	ax.bar_label(rects1, padding=3)
	ax.bar_label(rects2, padding=3)

	fig.tight_layout()

	plt.show()

"""
Plots the prejudice for every pair (AA, AB...) by timestep. Receives a list of matrices
"""
def plotPrejudiceByTimestep(matrices):
	AA = []
	AB = []
	BA = []
	BB = []

	for matrix in matrices:
		AA.append(matrix[0][0])
		AB.append(matrix[0][1])
		BA.append(matrix[1][0])
		BB.append(matrix[1][1])

	timesteps = [i for i in range(1,len(matrices)+1)]

	fig, ax = plt.subplots()
	ax.plot(timesteps, AA, label="AA")
	ax.plot(timesteps, AB, label="AB")
	ax.plot(timesteps, BA, label="BA")
	ax.plot(timesteps, BB, label="BB")
	ax.legend()

	plt.yticks([i * 0.1 for i in range(11)])

	plt.show()

op1 = [0.2,0.3,0.8,0.9,0.95,0.1]
op2 = [0.4,0.2,0.9,0.5,0.4,0.1]
op3 = [0.6,0.1,0.95,0.3,0.2,0.05]

op = [op1,op2,op3]

prejudice1 = [[0.5,0.5], [0.5,0.5]]
prejudice2 = [[0.4,0.55], [0.52,0.45]]
prejudice3 = [[0.37,0.66], [0.56,0.42]]
prejudice4 = [[0.24,0.7], [0.57,0.4]]
prejudice5 = [[0.1,0.85], [0.52,0.39]]

prejudice = [prejudice1, prejudice2, prejudice3, prejudice4, prejudice5]

plotPrejudiceByTimestep(prejudice)
