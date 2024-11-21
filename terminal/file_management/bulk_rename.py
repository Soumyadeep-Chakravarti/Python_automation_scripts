import os
import threading
from math import ceil


def execute_in_threads(total_items, num_threads, worker_func, *worker_args):
    """
    Executes a task across multiple threads.
    """
    threads = []
    items_per_thread = ceil(total_items / num_threads)

    for thread_id in range(num_threads):
        start_index = thread_id * items_per_thread
        end_index = min(start_index + items_per_thread, total_items)

        thread = threading.Thread(
            target=worker_func, args=(start_index, end_index, thread_id, *worker_args)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def rename_files_in_folder(folder, new_name, extension, num_threads=4):
    """
    Renames all files in a folder using a specified pattern.
    """
    if not os.path.isdir(folder):
        raise ValueError(f"'{folder}' is not a valid directory.")

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        raise ValueError(f"No files found in '{folder}' to rename.")

    def rename_worker(start, end, thread_id, files):
        for i in range(start, end):
            old_path = os.path.join(folder, files[i])
            new_filename = f"{new_name}_{thread_id}_{i}.{extension}"
            new_path = os.path.join(folder, new_filename)
            try:
                os.rename(old_path, new_path)
                print(f"Thread-{thread_id}: Renamed '{files[i]}' to '{new_filename}'")
            except Exception as e:
                print(f"Thread-{thread_id}: Error renaming '{files[i]}' - {e}")

    execute_in_threads(len(files), num_threads, rename_worker, files)
    print("File renaming completed!")


def create_files_in_folder(folder, new_name, extension, count, num_threads=4):
    """
    Creates a specified number of files in a folder.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder '{folder}'.")

    def create_worker(start, end, thread_id):
        for i in range(start, end):
            filename = f"{new_name}_{thread_id}_{i}.{extension}"
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, "w") as f:
                    f.write(f"Sample content for {filename}\n")
                print(f"Thread-{thread_id}: Created file '{filename}'")
            except Exception as e:
                print(f"Thread-{thread_id}: Error creating file '{filename}' - {e}")

    execute_in_threads(count, num_threads, create_worker)
    print("File creation completed!")


def main():
    """
    Main function to drive file creation and renaming operations.
    """
    # Configuration
    folder = "./test_folder"
    base_name = "file"
    new_name = "renamed"
    extension = "txt"
    file_count = 20
    num_threads = 4

    # Operations
    try:
        print("Creating files...")
        create_files_in_folder(folder, base_name, extension, file_count, num_threads)

        print("\nRenaming files...")
        rename_files_in_folder(folder, new_name, extension, num_threads)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
