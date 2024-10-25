import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import data_ingestor
from app import task_runner
import pandas as pd

data_ing = data_ingestor.DataIngestor("nutrition_activity_obesity_usa_subset.csv")
print(sys.path)
class TestBest5(unittest.TestCase):
    
    def test_best5(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification"
        }
        result = task_runner.solve_task([data, 1, "best5"], data_ing)
        self.assertEqual(result, {'Vermont': 29.6, 'Wisconsin': 30.3, 'Alaska': 33.1, 'Illinois': 34.45, 'Maryland': 34.46666666666667})


class TestWorst5(unittest.TestCase):
    def test_worst5(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification"
        }
        result = task_runner.solve_task([data, 1, "worst5"], data_ing)
        self.assertEqual(result, {'Utah': 38.9, 'Maryland': 34.46666666666667, 'Illinois': 34.45, 'Alaska': 33.1, 'Wisconsin': 30.3})


class TestGlobalMean(unittest.TestCase):
    def test_global_mean(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification"
        }
        result = task_runner.solve_task([data, 1, "global_mean"], data_ing)
        self.assertEqual(result, {'global_mean': 33.800000000000004})
            
class TestStateMean(unittest.TestCase):
    def test_state_mean(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification",
            "state": "Vermont"
        }
        result = task_runner.solve_task([data, 1, "state_mean"], data_ing)
        self.assertEqual(result, {'Vermont': 29.6})

class TestStatesMean(unittest.TestCase):
    def test_states_mean(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification"
        }
        result = task_runner.solve_task([data, 1, "states_mean"], data_ing)
        self.assertEqual(result, {'Vermont': 29.6, 'Wisconsin': 30.3, 'Alaska': 33.1, 'Illinois': 34.45, 'Maryland': 34.46666666666667, 'Utah': 38.9})
        
class TestDiffFromMean(unittest.TestCase):
    def test_diff_from_mean(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification"
        }
        result = task_runner.solve_task([data, 1, "diff_from_mean"], data_ing)
        self.assertEqual(result, {'Vermont': 4.200000000000003, 'Wisconsin': 3.5000000000000036, 'Alaska': 0.7000000000000028, 'Illinois': -0.6499999999999986, 'Maryland': -0.6666666666666643, 'Utah': -5.099999999999994})

class TestStateDiffFromMean(unittest.TestCase):
    def test_state_diff_from_mean(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification",
            "state": "Vermont"
        }
        result = task_runner.solve_task([data, 1, "state_diff_from_mean"], data_ing)
        self.assertEqual(result, {'Vermont': 4.200000000000003})
        
class TestMeanByCategory(unittest.TestCase):
    def test_mean_by_category(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification",
        }
        result = task_runner.solve_task([data, 1, "mean_by_category"], data_ing)
        self.assertEqual(result, {"('Alaska', 'Income', '$35,000 - $49,999')": 33.1, "('Illinois', 'Education', 'High school graduate')": 32.2, "('Illinois', 'Race/Ethnicity', 'Hispanic')": 36.7, "('Maryland', 'Age (years)', '65 or older')": 41.0, "('Maryland', 'Education', 'Some college or technical school')": 35.3, "('Maryland', 'Race/Ethnicity', '2 or more races')": 27.1, "('Utah', 'Race/Ethnicity', 'Hispanic')": 38.9, "('Vermont', 'Race/Ethnicity', 'Other')": 29.6, "('Wisconsin', 'Age (years)', '35 - 44')": 30.3})

class TestStateMeanByCategory(unittest.TestCase):
    def test_state_mean_by_category(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification",
            "state": "Illinois"
        }
        result = task_runner.solve_task([data, 1, "state_mean_by_category"], data_ing)
        self.assertEqual(result, {'Illinois': {"('Education', 'High school graduate')": 32.2, "('Race/Ethnicity', 'Hispanic')": 36.7}})

if __name__ == '__main__':
    unittest.main()