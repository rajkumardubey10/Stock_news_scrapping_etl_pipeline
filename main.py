import threading
import time
import subprocess
import warnings
from bs4 import MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


def run_investing_news():
    subprocess.run(['python', 'investing_news.py'])

def run_moneycontrol_news():
    subprocess.run(['python', 'moneycontrol_news.py'])

def main():
    # Capture start time
    start_time = time.time()

    # Create threads for both tasks
    investing_thread = threading.Thread(target=run_investing_news)
    moneycontrol_thread = threading.Thread(target=run_moneycontrol_news)
    
    # Start both threads
    investing_thread.start()
    moneycontrol_thread.start()

    # Wait for both threads to complete
    investing_thread.join()
    moneycontrol_thread.join()

    # Capture end time
    end_time = time.time()

    # Calculate and print the time taken
    total_time = end_time - start_time
    print(f"Both scripts finished executing. Time taken: {total_time:.2f} seconds.")

if __name__ == "__main__":
    main()
