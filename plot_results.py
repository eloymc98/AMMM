import numpy as np
import matplotlib.pyplot as plt

# Creating a numpy array
X = np.array([83.53, 0.60787606, 0.56355, 0.52685404, 161.22519922, 43, 160.5706632])
Y = np.array([0, (180 - 172) / 172, (176 - 172) / 172, (176 - 172) / 172, 0, 0, 0]) * 100

plt.xlabel('Time (seconds)')
plt.ylabel('Obj. value difference (%)')
plt.plot(X[0], Y[0], 'bs', color='blue', label='CPLEX', markersize=12)
plt.plot(X[1], Y[1], 'ro', label='Greedy', color='red', markersize=12)
plt.plot(X[2], Y[2], 'ro', label='Greedy + LS (First)', color='brown', markersize=12)
plt.plot([X[3]], Y[3], 'ro', label='Greedy + LS (Best)', color='green', markersize=12)
plt.plot(X[4], Y[4], 'ro', label='GRASP', color='black', markersize=12)
plt.plot(X[5], Y[5], 'ro', label='GRASP + LS (First)', color='pink', markersize=12)
plt.plot(X[6], Y[6], 'ro', label='GRASP + LS (Best)', color='violet', markersize=12)
plt.legend()
plt.savefig('plots/performance0.png')
plt.show()
#######################
X = np.array([247.82, 6.1330142, 6.13849497, 4.53772783, 150.2052989, 242.9250381, 279.083453])
Y = np.array([0, (183 - 157) / 157, (179 - 157) / 157, (179 - 157) / 157, (179 - 157) / 157, (192 - 157) / 157, (194 - 157) / 157]) * 100

plt.xlabel('Time (seconds)')
plt.ylabel('Obj. value difference (%)')
plt.plot(X[0], Y[0], 'bs', color='blue', label='CPLEX', markersize=12)
plt.plot(X[1], Y[1], 'ro', label='Greedy', color='red', markersize=12)
plt.plot(X[2], Y[2], 'ro', label='Greedy + LS (First)', color='brown', markersize=12)
plt.plot([X[3]], Y[3], 'ro', label='Greedy + LS (Best)', color='green', markersize=12)
plt.plot(X[4], Y[4], 'ro', label='GRASP', color='black', markersize=12)
plt.plot(X[5], Y[5], 'ro', label='GRASP + LS (First)', color='pink', markersize=12)
plt.plot(X[6], Y[6], 'ro', label='GRASP + LS (Best)', color='violet', markersize=12)
plt.legend()
plt.savefig('plots/performance1.png')
plt.show()

########################
X = np.array([344.53, 0.72352099, 0.75220394, 0.77671599, 7.54188013, 2.10909414, 1.93550706])
Y = np.array([0, (339 - 272) / 272, (339 - 272) / 272, (317 - 272) / 272, (292 - 272) / 272, (292 - 272) / 272, (292 - 272) / 272]) * 100

plt.xlabel('Time (seconds)')
plt.ylabel('Obj. value difference (%)')
plt.plot(X[0], Y[0], 'bs', color='blue', label='CPLEX', markersize=12)
plt.plot(X[1], Y[1], 'ro', label='Greedy', color='red', markersize=12)
plt.plot(X[2], Y[2], 'ro', label='Greedy + LS (First)', color='brown', markersize=12)
plt.plot([X[3]], Y[3], 'ro', label='Greedy + LS (Best)', color='green', markersize=12)
plt.plot(X[4], Y[4], 'ro', label='GRASP', color='black', markersize=12)
plt.plot(X[5], Y[5], 'ro', label='GRASP + LS (First)', color='pink', markersize=12)
plt.plot(X[6], Y[6], 'ro', label='GRASP + LS (Best)', color='violet', markersize=12)
plt.legend()
plt.savefig('plots/performance2.png')
plt.show()

########################
X = np.array([822.54, 16.2120938, 14.08670282, 17.13206673, 81.23526192, 21.24188709, 21.86853886])
Y = np.array([0, (502 - 335) / 335, (346 - 335) / 335, (346 - 335) / 335, (453 - 335) / 335, (346 - 335) / 335, (335 - 335) / 335]) * 100

plt.xlabel('Time (seconds)')
plt.ylabel('Obj. value difference (%)')
plt.plot(X[0], Y[0], 'bs', color='blue', label='CPLEX', markersize=12)
plt.plot(X[1], Y[1], 'ro', label='Greedy', color='red', markersize=12)
plt.plot(X[2], Y[2], 'ro', label='Greedy + LS (First)', color='brown', markersize=12)
plt.plot([X[3]], Y[3], 'ro', label='Greedy + LS (Best)', color='green', markersize=12)
plt.plot(X[4], Y[4], 'ro', label='GRASP', color='black', markersize=12)
plt.plot(X[5], Y[5], 'ro', label='GRASP + LS (First)', color='pink', markersize=12)
plt.plot(X[6], Y[6], 'ro', label='GRASP + LS (Best)', color='violet', markersize=12)
plt.legend()
plt.savefig('plots/performance3.png')
plt.show()

########################
X = np.array([1354, 15.9951348, 15.43929505, 22.12564182, 40.32106233, 115.57565212, 165.2543807])
Y = np.array([0, (163 - 160) / 160, (163 - 160) / 160, (163 - 160) / 160, (174 - 160) / 160, (163 - 160) / 160, (163 - 160) / 160]) * 100

plt.xlabel('Time (seconds)')
plt.ylabel('Obj. value difference (%)')
plt.plot(X[0], Y[0], 'bs', color='blue', label='CPLEX', markersize=12)
plt.plot(X[1], Y[1], 'ro', label='Greedy', color='red', markersize=12)
plt.plot(X[2], Y[2], 'ro', label='Greedy + LS (First)', color='brown', markersize=12)
plt.plot([X[3]], Y[3], 'ro', label='Greedy + LS (Best)', color='green', markersize=12)
plt.plot(X[4], Y[4], 'ro', label='GRASP', color='black', markersize=12)
plt.plot(X[5], Y[5], 'ro', label='GRASP + LS (First)', color='pink', markersize=12)
plt.plot(X[6], Y[6], 'ro', label='GRASP + LS (Best)', color='violet', markersize=12)
plt.legend()
plt.savefig('plots/performance4.png')
plt.show()
