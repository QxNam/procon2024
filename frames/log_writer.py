import threading
import queue

def log_writer(click_queue):
    with open("click_log_threaded.txt", "a") as log_file:
        while True:
            row, col = click_queue.get()
            if row is None and col is None:
                break
            log_file.write(f"Clicked at (row: {row}, col: {col})\n")
            log_file.flush()
            click_queue.task_done()

def start_log_writer():
    click_queue = queue.Queue()
    log_thread = threading.Thread(target=log_writer, args=(click_queue,), daemon=True)
    log_thread.start()
    return log_thread, click_queue

def stop_log_writer(log_thread, click_queue):
    click_queue.put((None, None))
    log_thread.join()
