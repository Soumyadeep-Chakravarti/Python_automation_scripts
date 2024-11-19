import os
import threading

def rename_files(folder, new_name, extension):
    """
    Function to rename files in a given folder.
    """
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    
    def rename_worker(start, end, thread_id):
        for i in range(start, end):
            old_path = os.path.join(folder, files[i])
            new_filename = f"{new_name}_{thread_id}_{i}.{extension}"
            new_path = os.path.join(folder, new_filename)
            os.rename(old_path, new_path)
            print(f"Thread-{thread_id}: Renamed '{files[i]}' to '{new_filename}'")

    # Divide files among threads
    num_threads = 4  # You can adjust the number of threads
    files_per_thread = len(files) // num_threads
    threads = []

    for thread_id in range(num_threads):
        start_index = thread_id * files_per_thread
        end_index = start_index + files_per_thread
        if thread_id == num_threads - 1:  # Handle remaining files in the last thread
            end_index = len(files)
        thread = threading.Thread(target=rename_worker, args=(start_index, end_index, thread_id))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Renaming completed!")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ").strip()
    new_name = input("Enter the new base name for files: ").strip()
    extension = input("Enter the new file extension (without dot): ").strip()

    if os.path.exists(folder_path):
        rename_files(folder_path, new_name, extension)
    else:
        print("Error: The folder does not exist.")
