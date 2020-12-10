# Integer Linear Programming and Heuristics

You can find the problem statement in **project.pdf** in the relative route ./project.pdf.

You can find the project report in **project_report.pdf** in the relative route (./project_report.pdf). It has all the information that we have used to create 
this solution to the project statement and the pseudocode of the different heuristics with its explanation as well.
In addition, you can find there all the metrics, plots and conclusions made.

We have structured the project in three different directories:

* **Generator** (./Generator): contains the files that are needed to create the problem instances that is used by the solvers.
* **Heuristics** (./Heuristics) contains the files needed to solve the problem instances applying different heuristics.
* **OPL** (./OPL) contains the code to use in [IBM ILOG CPLEX](https://https://www.ibm.com/es-es/products/ilog-cplex-optimization-studio) needed for solving the problem instances.

## Generator

This directory contains everything that is needed to create new problem instances.

Although we have provided you some instances, 
you are able to create yours by tunning the parameters specified in the **config.dat** file (./Generator/config/config.dat). There are comments that explain each parameter that you need to define for a proper execution of the code.

Tu run the code you only need to import the project directory in your favourite IDE, configure your python rute and execute it.
Once you have run it, you will see a new file in the **directory output** (./Generator/output) with the new instance/s that you have created.

To solve the instances you need to move them tyo the **data directory**, we are going to explain this directory below.

## Heuristics

This directory contains all the python code that solves the problems instances.

We have implemented three heuristics:

* Greedy constructive algorithm.
* Greedy constructive + a local search procedure.
* GRASP as a meta-heuristic algorithm.

To run each heuristic we have defined a **configuration file**
(./Heuristics/config/config.data) which has all the parameters needed to change between them
and to enable or disable some options. You can find more information in this specific configuration file.

As we mentioned above, to import the problem instances to solve them you have to move them to the **data directory** (./Heuristics/data). 
Once there, you can execute the code in the IDE as usually.

Once you have run the solver, you can find the solution in the **solutions directory** (./Heuristics/solutions).

## OPL

Once you have downloaded and installed [IBM ILOG CPLEX](https://https://www.ibm.com/es-es/products/ilog-cplex-optimization-studio), you can execute the code given in this directory.

If you want to solve a new instance generated, you have to import it by moving to the **opl directory** (./OPL).