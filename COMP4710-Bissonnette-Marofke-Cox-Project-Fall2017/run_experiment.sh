#!/bin/sh	
python scripts/generate_frequent_patterns.py data/vectors_training_1950_2000.txt output/patterns.txt 18.875 1 0

python scripts/generate_assoc_rules.py output/patterns.txt output/rules.txt 0.25

python scripts/test_best_fit.py data/vectors_testing_2001_2015.txt output/rules.txt 1 > output_result.txt
