import ast
import csv
import os


def read_scraper_results(file_path):
    """
    Convert the scraper results in `file_path`:
    Return: results array of data
    ```
    "[title1, newtitle1, def1]"
    "[title2, newtitle2, def2]"
    ```
    """
    result_list = []

    try:
        with open(file_path, "r") as file:
            for line in file:
                # Use ast.literal_eval to safely convert each line into a list
                line_list = ast.literal_eval(line.strip())
                result_list.append(line_list)
        return result_list

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def write_list_to_csv(data_list, csv_file_path, title=True):
    """
    Convert python list `data_list` to a csv file `csv_file_path`
    """
    try:
        with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write header row if needed
            if title:
                csv_writer.writerow(["Order", "Title", "New_Title", "Definition"])
            # Write data rows
            for item in data_list:
                csv_writer.writerow(item)
        print(f"CSV file successfully created: {csv_file_path}")

    except Exception as e:
        print(f"Error writing to CSV file: {e}")


def enumerate_list(data_list, start):
    """
    Takes a 2d array and inserts each sub-arrays (index + 1) as the first element of that sub-array.
    ```
    [[a],[b],[c]] -> [[1,a],[2,b],[3,c]]
    ```
    """
    enumerated_list = []

    for i, sublist in enumerate(data_list, start):
        enumerated_sublist = [i] + sublist
        enumerated_list.append(enumerated_sublist)

    return enumerated_list


# Sort the data list using the custom_sort function
def resort_list(data):
    # Define a custom sorting key function
    def custom_sort(item):
        # Return a tuple with 0 or 1 as the first element based on whether the last element is an empty string
        return (1 if item[-1] == "" else 0, item)

    sorted_data = sorted(data, key=custom_sort)

    return sorted_data


def capitalize_title(data):
    for sublist in data:
        sublist[2] = sublist[2].capitalize()


def concatenate_csv(input_file1, input_file2, output_file):
    with open(input_file1, "r", newline="", encoding="utf-8") as file1, open(
        input_file2, "r", newline="", encoding="utf-8"
    ) as file2, open(output_file, "w", newline="", encoding="utf-8") as output:
        # Read the content of the first CSV file
        reader1 = csv.reader(file1)
        data1 = list(reader1)

        # Read the content of the second CSV file and skip the header
        reader2 = csv.reader(file2)
        data2 = list(reader2)[1:]

        # Concatenate the data from both files
        concatenated_data = data1 + data2

        # Write the concatenated data to the output CSV file
        writer = csv.writer(output)
        writer.writerows(concatenated_data)


def count_rows(csv_file_path):
    try:
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            row_count = sum(1 for row in csv_reader)

        return row_count

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
        return 0

    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def read_csv_to_list(csv_file_path):
    try:
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            data_list = list(csv_reader)

        return data_list

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
        return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def split_csv(input_file, output_file_with_definition, output_file_empty_definition):
    try:
        with open(input_file, "r", newline="", encoding="utf-8") as csv_file, open(
            output_file_with_definition, "w", newline="", encoding="utf-8"
        ) as file_with_definition, open(
            output_file_empty_definition, "w", newline="", encoding="utf-8"
        ) as file_empty_definition:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)

            csv_writer_with_definition = csv.writer(file_with_definition)
            csv_writer_empty_definition = csv.writer(file_empty_definition)

            # Write headers to both output files
            csv_writer_with_definition.writerow(header)
            csv_writer_empty_definition.writerow(header)

            for row in csv_reader:
                if row[2]:  # Check if the third element is not empty
                    csv_writer_with_definition.writerow(row)
                else:
                    csv_writer_empty_definition.writerow(row)

        print(
            f"CSV file successfully split into two: {output_file_with_definition}, {output_file_empty_definition}"
        )

    except Exception as e:
        print(f"Error splitting CSV file: {e}")


def sort_csv(input_csv, output_csv):
    try:
        # Read CSV into a list of lists
        with open(input_csv, "r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read and store the header
            data = list(csv_reader)

        # Sort the data based on the first column as integers
        sorted_data = sorted(data, key=lambda x: int(x[0]))

        # Write the sorted data to a new CSV file
        with open(output_csv, "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(header)  # Write the header back
            csv_writer.writerows(sorted_data)

        print(f"CSV file successfully sorted: {output_csv}")

    except Exception as e:
        print(f"Error sorting CSV file: {e}")


def update_csv(idioms_csv, res_txt):
    """
    Takes results and puts them into the main csv file.
    """
    start = count_rows(idioms_csv)
    data = read_scraper_results(res_txt)
    data = enumerate_list(data, start)
    capitalize_title(data)
    write_list_to_csv(data, "recently_added.csv")
    concatenate_csv(idioms_csv, "recently_added.csv", "temp_all_idioms.csv")
    pre_sorted = read_csv_to_list("temp_all_idioms.csv")
    header = pre_sorted.pop(0)
    sorted_list = resort_list(pre_sorted)
    sorted_list.insert(0, header)
    write_list_to_csv(sorted_list, "s.csv", False)
    split_csv("s.csv", "c.csv", "i.csv")
    sort_csv("c.csv", "idioms_complete_sorted.csv")
    sort_csv("i.csv", "idioms_incomplete_sorted.csv")
    sort_csv("s.csv", "idioms.csv")

    try:
        os.remove(
            "s.csv",
        )
        os.remove(
            "c.csv",
        )
        os.remove(
            "i.csv",
        )
        os.remove(
            "temp_all_idioms.csv",
        )
    except OSError as e:
        print(f"Error removing file: {e}")


if __name__ == "__main__":
    # update_csv(main_csv, results)
    update_csv("idioms.csv", "new_results.txt")
