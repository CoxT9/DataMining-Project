COMP 4710 Course Project README.

This document briefly outlines the required steps to execute the attached scripts for marking and auditing purposes.

The Hurricane Trajectory Model WARD-HTP itself is run with the shell script 'run_experiment.sh'. run_experiment executes AprioriAll, generates association rules and tests the model against testing data as described in the results section of the accompanying paper.

In its current form, the code for WARD-HTP is configured to reproduce the best case results documented in the paper. To change the model paramaters, you can:

- change the training data by specifying the file path in run_experiments line 2
- change the min support by changing the float in run_experiments line 2
- change the weighting style (weighted or unweighted data) by flipping the first bit in run_experiments line 2 (1: weighted 0: non-weighted)
- change the weighting strategy (year or index weighting) by flipping the second bit (0: year-based 1: index-based)
- change minconf by changing the float in run_experiments line 4
- change the testing data by changing the file path in run_experiments line 6
- change the distance formula by line 255 of test_best_fit.py (use getHaversineDistance or getEuclideanDistance)
- change the ratio computation by flipping the bit in run_experiments line 6 (0: worst case ratio 1: best case ratio)

The results of the model will be written to a text file as specified by run_experiments.sh. The final result of the model execution (correctness ratio) will be sent to the bottom of the file.

Execute ./run_experiment.sh in a terminal to kick off WARD-HTP. Depending on the inputs used, the model may run for a few minutes. Python 2.7 must be installed to execute the model correctly.

Project submitted 12-08-2017. By Jasmin Bissonnette, Caden Marofke and Taylor Cox.
