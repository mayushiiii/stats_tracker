# stats_tracker

Using <a href='https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system'> this dataset </a>  on nutrition, physical activity and obesity in the US, the program is a Python server that uses Flask, handling requests related to the information in the dataset. 

All the data is in a `.csv` file which is read by the server. The file consists of data regarding the US state the stats correspond to and answers to several health related questions:
 * 'Percent of adults who engage in no leisure-time physical activity'
  * 'Percent of adults aged 18 years and older who have obesity'
  * 'Percent of adults aged 18 years and older who have an overweight classification'
  * 'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)'
  * 'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week'
  * 'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)'
  * 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
  * 'Percent of adults who report consuming fruit less than one time daily'
  * 'Percent of adults who report consuming vegetables less than one time daily'
Then the user can send a request, which will be assigned a job id and processed by a **Thread Pool**. 
In order to allow efficient answers in a dataset of this size, the server uses **multithreading** : each thread executes a job out of the job queue and returns the desired result, writing it in the `results/` directory.
___
The possible requests are the following (all for a particular given question out of the ones above):
- `states_mean` : The mean of the registered values in each state
- `state_mean` : The mean of the registered values in a specific state
- `best5` : The top 5 states that have the highest registered value
- `worst5` : The top 5 states that have the lowest registered value
- `global_mean` : The mean of the registered values in all states
- `diff_from_mean` : The difference between `global_mean` and `states_mean` for each state
- `state_diff_from_mean` : The difference between `global_mean` and `state_mean` for a specific state
- `mean_by_category` : The mean of each state for each stratification
- `state_mean_by_category` : The mean of a given state for each stratification
- `graceful_shutdown` : Shuts down the thread pool
- `jobs` : Returns all job id's and their status
- `num_jobs` : Returns all jobs that are still running
- `get_results/<job_id>` : Returns a JSON of the job data, if the job exists
