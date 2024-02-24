import click
import json
import urllib.parse
import os
import matplotlib.pyplot as plt


@click.command()
@click.argument('coverage')
def main(coverage):
    data = read_coverage(coverage)
    coverage_data_for_graph = []

    # Ensure the correct directory is determined
    determine_directory()

    for file_coverage in data:
        result = parse_file_coverage(file_coverage)
        if result:  # Ensure data was returned
            coverage_data_for_graph.append(result)

    if coverage_data_for_graph:
        generate_coverage_graph(coverage_data_for_graph)
    else:
        print("No data available for graph generation.")


# Global variables for directory name
base_directory_name = 'coverage_files'
directory_name = f'{base_directory_name}1'  # Default to using the first directory


# Function to determine which directory to use
def determine_directory():
    global directory_name
    if os.path.exists(directory_name):
        # If the first directory exists, switch to using the second
        directory_name = f'{base_directory_name}2'


# Call determine_directory at the start of your script to set the directory name
determine_directory()


def save_to_subdirectory(filename, text):
    # Create the directory if it doesn't exist
    os.makedirs(directory_name, exist_ok=True)

    # Combine the directory path with the filename
    filepath = os.path.join(directory_name, filename)

    # Write the text to the file in the directory
    with open(filepath, 'w') as file:
        file.write(text)


def read_coverage(coverage):
    with open(coverage) as f:
        data = json.load(f)
    return data


def to_filename(url):
    path = urllib.parse.urlparse(url).path
    filename = os.path.basename(path)
    return filename


# Update the parse_file_coverage function to use save_to_subdirectory
def parse_file_coverage(file_coverage):
    filename = to_filename(file_coverage['url'])
    if not filename or 'text' not in file_coverage:
        print(f"Skipping: {filename} (no text data)")
        return None  # Ensure to return None to indicate skipping

    ranges = file_coverage['ranges']
    text = file_coverage['text']

    # Calculate total_size as the length of the full text
    total_size = len(text)

    # Initialize an empty string to store used text
    used_text = ''
    for file_range in ranges:
        used_text += text[file_range['start']:file_range['end']]

    # Calculate used_size as the length of the used text
    used_size = len(used_text)

    print('Creating: {0}'.format(filename))
    save_to_subdirectory(filename, used_text)

    # Now returning actual calculated total_size and used_size
    return filename, total_size, used_size


# Save the graph with a unique name, so it doesn't overwrite the previous graph
def save_coverage_graph_with_unique_name(directory, base_filename='coverage_analysis.png', dpi=300):
    filename = base_filename
    file_counter = 1
    # Split the base_filename to insert a number before the extension
    name_part, extension = os.path.splitext(base_filename)

    while os.path.exists(os.path.join(directory, filename)):
        filename = f"{name_part}_{file_counter}{extension}"
        file_counter += 1

    full_path = os.path.join(directory, filename)
    plt.savefig(full_path, dpi=dpi)
    print(f"Graph saved as: {full_path}")  # Optional: print out where the graph was saved


# Graph the data
def generate_coverage_graph(graph_coverage_data=None):
    if graph_coverage_data is None:
        graph_coverage_data = []

    # Sort the data by total size
    graph_coverage_data_sorted = sorted(graph_coverage_data, key=lambda x: x[1], reverse=False)
    filenames, total_sizes, used_sizes = zip(*graph_coverage_data_sorted)
    # unused_sizes = [total - used for total, used in zip(total_sizes, used_sizes)]

    y = range(len(filenames))  # This will be the y-position of the bars

    # Adjust figure size for better readability (wider and taller figure)
    plt.figure(figsize=(10, len(filenames) * 0.5))  # Adjust the figure size as needed

    plt.barh(y, total_sizes, label='Total Size')  # Changed to horizontal bar
    plt.barh(y, used_sizes, label='Used Size')  # Adjust for used sizes on horizontal bar

    plt.ylabel('Files')  # This now refers to the y-axis for filenames
    plt.xlabel('Size (bytes)')  # X-axis will now show size in bytes
    plt.title('Coverage Analysis')
    plt.yticks(y, filenames)  # Set the y-ticks to show filenames without rotation
    plt.legend()

    plt.tight_layout()
    # Replace the plt.savefig call with this function call
    save_coverage_graph_with_unique_name(directory_name)  # assuming directory_name is the directory you want to save in
    plt.show()


if __name__ == '__main__':
    main()
