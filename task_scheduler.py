# Import the schedule library
import schedule

# Define a simple function to schedule
def task():
    print('Task is running!')

# Schedule the task
schedule.every().day.at('10:30').do(task)

while True:
    schedule.run_pending()
