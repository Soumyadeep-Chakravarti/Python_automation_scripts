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

def create_files(folder, new_name, extension, count):
    """
    Function to create new files in a given folder.
    """
    def create_worker(start, end, thread_id):
        for i in range(start, end):
            filename = f"{new_name}_{thread_id}_{i}.{extension}"
            file_path = os.path.join(folder, filename)
            with open(file_path, 'w') as f:
                f.write(f"Sample content for {filename}\n")
            print(f"Thread-{thread_id}: Created file '{filename}'")

    # Divide file creation among threads
    num_threads = 4  # You can adjust the number of threads
    files_per_thread = count // num_threads
    threads = []

    for thread_id in range(num_threads):
        start_index = thread_id * files_per_thread
        end_index = start_index + files_per_thread
        if thread_id == num_threads - 1:  # Handle remaining files in the last thread
            end_index = count
        thread = threading.Thread(target=create_worker, args=(start_index, end_index, thread_id))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("File creation completed!")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ").strip()
    operation = input("Enter 'rename' to rename files or 'create' to create new files: ").strip().lower()
    new_name = input("Enter the base name for files: ").strip()
    extension = input("Enter the file extension (without dot): ").strip()

    if not os.path.exists(folder_path):
        print("Error: The folder does not exist.")
        exit()

    if operation == "rename":
        rename_files(folder_path, new_name, extension)
    elif operation == "create":
        try:
            count = int(input("Enter the number of files to create: "))
            create_files(folder_path, new_name, extension, count)
        except ValueError:
            print("Error: Invalid number of files.")
    else:
        print("Error: Invalid operation. Use 'rename' or 'create'.")
