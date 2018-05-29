This is a repository for COMP 4710 - Introduction to Data Mining. Fall 2017.

This repository captures the work completed for the course project. The project undertaken is "Accurate Hurricane Trajectory Prediction"

Accuracy improvement strategies to be evaluated include:
- Best-Rule-Fit function which accounts for absence of matching rule (closest fit)
- Finer-grained trajectory prediction by partitioning regions using KD-Trees

Current state of the workflow:

To execute the Hurricane Prediction Model, complete the following:
- Run apriori_test.py with vectors_training.txt as input and patterns.txt as output
- Run genereate_assoc_rules.py with patterns.txt as input and rules.txt as output
- Run test_best_fit.py with rules.txt and vectors_testing.rxt as input, with stdout as output

In terms of a shell, execute the following:

$ python apriori_test.py vectors_training.txt patterns.txt
$ python generate_assoc_rules.txt patterns.txt rules.txt
$ python test_best_fit.py rules.txt vectors_testing.txt > results.txt

Other scripts in this repository:
- apirori_utils.py: Utility methods and constants

- basic_trajectory_draw.py: A simple script for drawing hurricane trajectories on a map of the atlantic coast.
- find_data_extrema.py: A simple script to find the northernmost, southernmost, easternmost and westernmost points from a given coordinate file.
(use vectors_training.txt or vectors_testing.txt as input for either script)

- generate_coord_vectors.py: A simple script to parse the raw atlantic_storms.csv file into a datafile of storm IDs with their coordinate vectors/trajectories.

Project members: Caden Marofke, Taylor Cox (professor: Dr. C. K. Leung)

If you use any of this work, please cite: Taylor S. Cox, Calvin S.H. Hoi, Carson K. Leung, Caden R. Marofke: An accurate model for hurricane trajectory prediction. IEEE COMPSAC (BIOT) 2018 (6)
