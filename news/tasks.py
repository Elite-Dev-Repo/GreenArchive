from celery import shared_task

@shared_task
def my_periodic_task():
    # Place your application logic here (e.g., database cleanups, syncing data)
    print("Periodic task executed successfully!")
    return "Done"