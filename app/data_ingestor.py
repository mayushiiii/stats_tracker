import pandas

class DataIngestor:
    def __init__(self, csv_path: str):
        # una din marile probleme ale vietii a fost faptul ca aveam nevoie
        # de dataingestor in task_runner si nu puteam sa o fac sa fie globala
        # pentru ca as fi avut un circular import issue
        # oricum. aici se construieste tabelul in stil dataset(specfic pandas)
        self.dataset = None
        with open(csv_path, 'r', encoding="utf-8") as csv_file:
            self.dataset = pandas.read_csv(csv_file)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an \
overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical \
activity',
            'Percent of adults who report consuming fruit less than \
one time daily',
            'Percent of adults who report consuming vegetables less \
than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of \
moderate-intensity aerobic physical activity or 75 minutes a week \
of vigorous-intensity aerobic activity \
(or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of \
moderate-intensity aerobic physical activity or 75 minutes a week \
of vigorous-intensity aerobic physical activity and engage \
in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of \
moderate-intensity aerobic physical activity or 150 minutes a week\
of vigorous-intensity aerobic activity \
(or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening \
activities on 2 or more days a week',
        ]
