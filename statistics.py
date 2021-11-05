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

	fig, ax = plt.subplots(figsize=(8, 5))
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
def plotAvgBeliefByTimestep(beliefs_by_attempt):
	fig, ax = plt.subplots(figsize=(8, 5))
	a_beliefs = []
	b_beliefs = []

	a_plots = ()
	b_plots = ()

	for attempt in beliefs_by_attempt:
		avg_a_beliefs_in_attempt = []
		avg_b_beliefs_in_attempt = []
		for timestep in attempt:
			a_beliefs_in_timestep = []	
			b_beliefs_in_timestep = []

			for belief in timestep:
				if belief <= 0.5:
					a_beliefs_in_timestep.append(belief)
				else:
					b_beliefs_in_timestep.append(belief)

			avg_a_belief_in_timestep = np.array(a_beliefs_in_timestep).mean(axis=0)
			avg_b_belief_in_timestep = np.array(b_beliefs_in_timestep).mean(axis=0)

			avg_a_beliefs_in_attempt.append(avg_a_belief_in_timestep)
			avg_b_beliefs_in_attempt.append(avg_b_belief_in_timestep)

		a_beliefs.append(avg_a_beliefs_in_attempt)
		b_beliefs.append(avg_b_beliefs_in_attempt)

		p1, = ax.plot(avg_a_beliefs_in_attempt, color='cornflowerblue')
		p2, = ax.plot(avg_b_beliefs_in_attempt, color='mediumseagreen')

		a_plots += (p1,)
		b_plots += (p2,)

	#print(a_beliefs)

	avg_a_beliefs = np.array(a_beliefs).mean(axis=0)
	avg_b_beliefs = np.array(b_beliefs).mean(axis=0)

	avg_a_plt, = ax.plot(avg_a_beliefs, color='black', linestyle='dashed')
	avg_b_plt, = ax.plot(avg_b_beliefs, color='red', linestyle='dashed')

	plt.title("Average beliefs of the two tags by timestep (attempts = {})".format(len(beliefs_by_attempt)))
	plt.legend([a_plots, b_plots, avg_a_plt, avg_b_plt], 
					["Avg. A Belief / Attempt", "Avg. B Belief / Attempt", "Avg. A Belief", "Avg. B Belief"])
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
Plots the group bias for every pair (AA, AB...) by timestep, for every attempt.
Receives a list of attempts, which containe the group bias by timestep.
"""
def plotBiasesByTimestep(biases_by_attempt):
	fig, ax = plt.subplots(figsize=(8, 5))
	aa_plots = ()
	ab_plots = ()
	ba_plots = ()
	bb_plots = ()

	all_aa = []
	all_ab = []
	all_ba = []
	all_bb = []

	timesteps = [i for i in range(len(biases_by_attempt[0]))]

	for attempt in biases_by_attempt:
		aa = []
		ab = []
		ba = []
		bb = []

		for matrix in attempt:
			aa.append(matrix[0][0])
			ab.append(matrix[0][1])
			bb.append(matrix[1][0])
			ba.append(matrix[1][1])

		all_aa.append(aa)
		all_ab.append(ab)
		all_ba.append(ba)
		all_bb.append(bb)

		p1, = ax.plot(timesteps, aa, color='darkslateblue')
		p2, = ax.plot(timesteps, ab, color='mediumslateblue')
		p3, = ax.plot(timesteps, ba, color='crimson')
		p4, = ax.plot(timesteps, bb, color='red')

		aa_plots += (p1,)
		ab_plots += (p2,)
		ba_plots += (p3,)
		bb_plots += (p4,)

	mean_aa = np.array(all_aa).mean(axis=0)
	mean_ab = np.array(all_ab).mean(axis=0)
	mean_ba = np.array(all_ba).mean(axis=0)
	mean_bb = np.array(all_bb).mean(axis=0)

	avg_aa, = ax.plot(timesteps, mean_aa, color='yellow', linestyle='dashed')
	avg_ab, = ax.plot(timesteps, mean_ab, color='magenta', linestyle='dashed')
	avg_ba, = ax.plot(timesteps, mean_ba, color='orange', linestyle='dashed')
	avg_bb, = ax.plot(timesteps, mean_bb, color='lawngreen', linestyle='dashed')

	ax.legend([aa_plots, ab_plots, ba_plots, bb_plots, avg_aa, avg_ab, avg_ba, avg_bb], 
					['AA', 'AB', 'BA', 'BB', 'Avg. AA', 'Avg. AB', 'Avg. BA', 'Avg. BB'])

	plt.title("Group bias between tags by timestep (attempts = {})".format(len(biases_by_attempt)))
	
	plt.yticks([i * 0.1 for i in range(11)])
	plt.show()

def plot_players_by_tag_by_timestep(beliefs_by_attempt):
	fig, ax = plt.subplots(figsize=(8, 5))
	a_beliefs = []
	b_beliefs = []

	a_plots = ()
	b_plots = ()

	for attempt in beliefs_by_attempt:
		a_beliefs_in_attempt = []
		b_beliefs_in_attempt = []
		for timestep in attempt:
			a_beliefs_in_timestep = 0
			b_beliefs_in_timestep = 0

			for belief in timestep:
				if belief <= 0.5:
					a_beliefs_in_timestep += 1
				else:
					b_beliefs_in_timestep += 1

			a_beliefs_in_attempt.append(a_beliefs_in_timestep)
			b_beliefs_in_attempt.append(b_beliefs_in_timestep)

		a_beliefs.append(a_beliefs_in_attempt)
		b_beliefs.append(b_beliefs_in_attempt)

		p1, = ax.plot(a_beliefs_in_attempt, color='cornflowerblue')
		p2, = ax.plot(b_beliefs_in_attempt, color='mediumseagreen')

		a_plots += (p1,)
		b_plots += (p2,)

	#print(a_beliefs)

	avg_a_beliefs = np.array(a_beliefs).mean(axis=0)
	avg_b_beliefs = np.array(b_beliefs).mean(axis=0)

	avg_a_plt, = ax.plot(avg_a_beliefs, color='black', linestyle='dashed')
	avg_b_plt, = ax.plot(avg_b_beliefs, color='red', linestyle='dashed')

	plt.title("Average beliefs of the two tags by timestep (attempts = {})".format(len(beliefs_by_attempt)))
	plt.legend([a_plots, b_plots, avg_a_plt, avg_b_plt], 
					["Players with Belief A", "Players with Belief B",
						"Avg. Nr. of Players w/ Belief A",
							"Avg. Nr. of Players w/ Belief B"])
	plt.show()
