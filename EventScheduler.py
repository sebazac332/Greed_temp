import heapq
from random import randint
import tkinter as tk
from tkinter import messagebox

#Algorithms
class priorityQueue:
    def __init__(self):
        self.elements = []

    def push(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def pop(self):
        if self.elements:
            return heapq.heappop(self.elements)[1]
        else:
            raise IndexError("pop from empty queue")

    def is_empty(self):
        return len(self.elements) == 0

def maxEmployeesRequired(jobList):
    customerCare = []
    while not jobList.is_empty():
        call = jobList.pop()
        assigned = False
        for employee in customerCare:
            if employee['end'] <= call['start']:
                assigned = True
                employee['end'] = call['end']
                break

        if not assigned:
            newEmployee = {"end": call['end']}
            customerCare.append(newEmployee)
    return len(customerCare)

def is_id_not_in_list(job_list, target_id):
    for job in job_list:
        if job['id'] == target_id:
            return False
    return True


#Interface
class JobSchedulerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Job Scheduler")

        self.jobList = [{"id":2, "start": 1000, "end": 1075}, {"id":3, "start": 1000, "end": 1100}, {"id":4, "start": 1000, "end": 1200}]
        self.no_workers = -1

        self.label = tk.Label(master, text="Temporary Menu")
        self.label.pack()

        self.insert_job_button = tk.Button(master, text="Insert Job", command=self.insert_job)
        self.insert_job_button.pack()

        self.insert_workers_button = tk.Button(master, text="Insert Workers", command=self.insert_workers)
        self.insert_workers_button.pack()

        self.worker_schedule_button = tk.Button(master, text="Worker Schedule", command=self.worker_schedule)
        self.worker_schedule_button.pack()

        self.calculate_workers_button = tk.Button(master, text="Calculate Required Workers", command=self.calculate_workers)
        self.calculate_workers_button.pack()

        self.show_jobs_button = tk.Button(master, text="Show Job List", command=self.show_jobs)
        self.show_jobs_button.pack()

        self.remove_job_button = tk.Button(master, text="Remove Job", command=self.remove_job)
        self.remove_job_button.pack()

        self.quit_button = tk.Button(master, text="Quit", command=self.master.quit)
        self.quit_button.pack()

    def insert_job(self):
        new_job_window = tk.Toplevel(self.master)
        new_job_window.title("Insert Job")

        start_hour_label = tk.Label(new_job_window, text="Start Hour (HH):")
        start_hour_label.pack()

        start_hour_entry = tk.Entry(new_job_window)
        start_hour_entry.pack()

        start_minute_label = tk.Label(new_job_window, text="Start Minute (MM):")
        start_minute_label.pack()

        start_minute_entry = tk.Entry(new_job_window)
        start_minute_entry.pack()

        end_hour_label = tk.Label(new_job_window, text="End Hour (HH):")
        end_hour_label.pack()

        end_hour_entry = tk.Entry(new_job_window)
        end_hour_entry.pack()

        end_minute_label = tk.Label(new_job_window, text="End Minute (MM):")
        end_minute_label.pack()

        end_minute_entry = tk.Entry(new_job_window)
        end_minute_entry.pack()

        def add_job():
            start_hour = start_hour_entry.get()
            start_minute = start_minute_entry.get()

            end_hour = end_hour_entry.get()
            end_minute = end_minute_entry.get()

            if(int(start_hour)<0 or int(start_hour)>23 or int(start_minute)<0 or int(start_minute)>60):
                messagebox.showinfo("Invalid Input", "Start time is invalid.")
            else:
                if(int(end_hour)<0 or int(end_hour)>23 or int(end_minute)<0 or int(end_minute)>60):
                    messagebox.showinfo("Invalid Input", "End time is invalid.")
                else:
                    # Combine hours and minutes
                    start_time = f"{start_hour.zfill(2)}:{start_minute.zfill(2)}"
                    end_time = f"{end_hour.zfill(2)}:{end_minute.zfill(2)}"

                    # Convert start_time and end_time to integers (you can adjust this as needed)
                    start_t = int(start_time.replace(":", ""))
                    end_t = int(end_time.replace(":", ""))
                    if(end_t < start_t):
                        messagebox.showinfo("Invalid Input", "End time cannot be less than start time.")
                    else:
                        #Create and validate id
                        id_i = randint(0, 999)
                        checkid = is_id_not_in_list(self.jobList, id_i)
                        while not checkid:
                            id_i = randint(0, 999)
                            checkid = is_id_not_in_list(self.jobList, id_i)

                        new_job = {"id": id_i, "start": start_t, "end": end_t}
                        self.jobList.append(new_job)

            new_job_window.destroy()

        add_button = tk.Button(new_job_window, text="Add Job", command=add_job)
        add_button.pack()
        pass

    def insert_workers(self):
        workers_window = tk.Toplevel(self.master)
        workers_window.title("Insert Workers")

        label = tk.Label(workers_window, text="Insert number of workers:")
        label.pack()

        entry = tk.Entry(workers_window)
        entry.pack()

        def submit_workers():
            no_input = entry.get()
            try:
                no_input = int(no_input)
                if no_input < 0:
                    messagebox.showinfo("Invalid Input", "Number of workers can't be less than 0.")
                else:
                    self.no_workers = no_input
                    workers_window.destroy()
            except ValueError:
                messagebox.showinfo("Invalid Input", "Please enter a valid integer.")

        submit_button = tk.Button(workers_window, text="Submit", command=submit_workers)
        submit_button.pack()
        pass

    def worker_schedule(self):
        worker_schedule_window = tk.Toplevel(self.master)
        worker_schedule_window.title("Worker Schedule")

        jobList_c = self.jobList.copy()

        if self.no_workers > 0:
            for x in range(self.no_workers):
                # Interval scheduling
                jobList_c.sort(key=lambda x: (x["end"], x["start"]))
                count = 0
                visited = []
                end = -1
                for job in jobList_c:
                    if end <= job["start"]:
                        end = job["end"]
                        count += 1
                        visited.append(job)
                        jobList_c.remove(job)
                schedule_label = tk.Label(worker_schedule_window, text=f"Worker {x+1} Schedule: {visited}")
                schedule_label.pack()
                if len(visited) == 0:
                    no_jobs_label = tk.Label(worker_schedule_window, text=f"Warning: Worker {x+1} has no jobs")
                    no_jobs_label.pack()
            if len(jobList_c) != 0:
                count_jl = len(jobList_c)
                warning_label = tk.Label(worker_schedule_window, text=f"Warning: There are {count_jl} unassigned jobs left")
                warning_label.pack()
        else:
            no_workers_label = tk.Label(worker_schedule_window, text="Number of workers not defined")
            no_workers_label.pack()
        pass

    def calculate_workers(self):
        # Add your logic to calculate required workers here
        pass

    def show_jobs(self):
        # Add your logic to display job list here
        pass

    def remove_job(self):
        # Add your logic to remove a job by ID here
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = JobSchedulerApp(root)
    root.mainloop()