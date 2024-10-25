import os
import json
from queue import Queue
from threading import Thread, Event

def solve_task(curr_job, data_ing):
    # elif elif elif elif elif elif ... god i wish there was an easier way to do this (glumesc)
    # obviously se putea mai ok organizat dar nu am timp <3
    # la global_mean e cel mai direct, e doar media Tuturor participantilor pe o intrebare
    # am timeout la un test pe moodle si nu inteleg de ce, mai eficient nu poti scrie asta
    if curr_job[2] == "global_mean":
        tg_group = data_ing.dataset[data_ing.dataset['Question'] == curr_job[0]['question']]
        res = {'global_mean': tg_group['Data_Value'].mean()}
    # states mean = doi pasi. intai iti stabileti target group ul (filtrat in baza
    # question-ului aici)
    # iar apoi folosind groupby ii alegi pe toti din acelasi stat, faci mean cu elementele
    # din campul data_value, sortezi, si il pui ca dictionar pt a l putea pune in json la final
    elif curr_job[2] == "states_mean":
        tg_group = data_ing.dataset[data_ing.dataset['Question'] == curr_job[0]['question']]
        res = tg_group.groupby('LocationDesc')['Data_Value'].mean().sort_values().to_dict()
    # state mean e mai simplu, filtrezi dupa intrebare si stat (= coincide cu inputul)
    # si faci meanul valorilor acelui target group
    elif curr_job[2] == "state_mean":
        tg_group = data_ing.dataset[(data_ing.dataset['Question'] == curr_job[0]['question'])\
            & (data_ing.dataset['LocationDesc'] == curr_job[0]['state'])]
        res = {curr_job[0]['state'] : tg_group['Data_Value'].mean()}
    # pot scrie asta intercalat cu worst5 si am facut asta anterior, dar niste erori anterioare
    # m au lasat cu versiunea asta. dupa ce stabilesti grupul care se incadreaza in intrebarea
    # data, folosesti groupby pt a te asigura ca faci mean ul pt cei din acelasi stat
    # si iei primele/ultimele 5 in fct de tipul intrebarii.
    elif curr_job[2] == "best5":
        tg_group = data_ing.dataset[data_ing.dataset['Question'] == curr_job[0]['question']]
        if curr_job[0]['question'] in data_ing.questions_best_is_min:
            res = tg_group.groupby('LocationDesc')['Data_Value'].mean().nsmallest(5)
        else:
            res = tg_group.groupby('LocationDesc')['Data_Value'].mean().nlargest(5)
        res = res.to_dict()
    # self explanatory avand in vedere ce am zis la best5
    elif curr_job[2] == "worst5":
        tg_group = data_ing.dataset[data_ing.dataset['Question'] == curr_job[0]['question']]
        if curr_job[0]['question'] in data_ing.questions_best_is_min:
            res = tg_group.groupby('LocationDesc')['Data_Value'].mean().nlargest(5)
        else:
            res = tg_group.groupby('LocationDesc')['Data_Value'].mean().nsmallest(5)
        res = res.to_dict()
    # puteam tine minte care e global_mean si state_mean de mai sus si apoi sa calculez doar aici
    # in schimb il recalculez. imi asum astazi.
    elif curr_job[2] == "diff_from_mean":
        tg_group = data_ing.dataset[data_ing.dataset['Question'] == curr_job[0]['question']]
        global_mean = tg_group['Data_Value'].mean()
        state_mean = tg_group.groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=True)
        res = global_mean - state_mean
        res = res.sort_values(ascending=False).to_dict()
    # idem. putin greu de citit din cauza limitei de caractere pylint
    # filtram grupul apoi obtinem cele 2 mean uri ca sa le facem diferenta
    elif curr_job[2] == "state_diff_from_mean":
        tg_group = data_ing.dataset[(data_ing.dataset['Question'] == curr_job[0]['question'])\
            & (data_ing.dataset['LocationDesc'] == curr_job[0]['state'])]

        global_mean = data_ing.dataset[data_ing.dataset['Question']\
            == curr_job[0]['question']]['Data_Value'].mean()

        state_mean = tg_group['Data_Value'].mean()
        res = {curr_job[0]['state'] : global_mean - state_mean}
    # filtrare grup urmata de separarea lui in mai multe grupulete mai mici in fct
    # de categoriile de stratificare si apoi facut medie
    elif curr_job[2] == "mean_by_category":
        tg_group = data_ing.dataset[data_ing.dataset['Question'] == curr_job[0]['question']]
        res = tg_group.groupby(['LocationDesc', 'StratificationCategory1',\
            'Stratification1'])['Data_Value'].mean().to_dict()
    # nu i convine formatul de tuplu asa ca facem string
        res = {str(key): value for key, value in res.items()}
    # ce am zis mai sus dar pe un sg stat
    elif curr_job[2] == "state_mean_by_category":
        tg_group = data_ing.dataset[(data_ing.dataset['Question'] == curr_job[0]['question'])\
            & (data_ing.dataset['LocationDesc'] == curr_job[0]['state'])]
        res = tg_group.groupby(['StratificationCategory1', 'Stratification1'])\
            ['Data_Value'].mean().to_dict()

        res = {str(key): value for key, value in res.items()}
        res = {curr_job[0]["state"]: res}

    return res

class ThreadPool:
    def __init__(self, data_ingestor):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task

        # caut variabila asta in os si daca nu, pun numarul de core uri
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            self.num_threads = os.cpu_count()
        # structuri de baza, relevante sunt queue ul si data_ingestor
        self.graceful_shutdown = Event()
        self.job_queue = Queue()
        self.data_ingestor = data_ingestor

    # aici se pornesc thread urile si li se asigneaza valorile de baza
    def start(self):
        for i in range(self.num_threads):
            thread = TaskRunner(self.job_queue, self.graceful_shutdown, self.data_ingestor)
            thread.name = f"Thread-{i}"
            thread.start()

class TaskRunner(Thread):
    def __init__(self, job_queue, graceful_shutdown, data_ingestor):
        # ne pasa de queue(shared data care trb folosit in mod paralel de
        # catre threaduri), data_ingestor (de unde altundeva extragem datele?)
        super().__init__()
        self.graceful_shutdown = graceful_shutdown
        self.job_queue = job_queue
        self.data_ingestor = data_ingestor

    def run(self):
        while True:

            if not self.job_queue.empty():
                curr_job = self.job_queue.get()
                job_id = curr_job[1]

                res = solve_task(curr_job, self.data_ingestor)

                # Execute the job and save the result to disk
                if not os.path.exists("results"):
                    os.makedirs("results")
                # daca scriu json.dumps(solve_task) nu merge DELOC ok :)))))))
                with open(f"results/{job_id}.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(res))

            # Repeat until graceful_shutdown
            if self.graceful_shutdown.is_set():
                print(f"Thread {self.name} is shutting down")
                break
