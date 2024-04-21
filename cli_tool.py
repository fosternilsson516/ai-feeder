import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

import threading

def load_csv(csv_file):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(csv_file)

def count_and_graph(df, x_col_name, values, count_col_names):
    """Generate a bar graph based on counts of specified values in a column, across other specified columns."""
    # Prepare data: Calculate the non-null counts for each value for each specified column
    counts = {
        col_name: {
            value: df[df[x_col_name] == value][col_name].notnull().sum()
            for value in values
        } for col_name in count_col_names
    }

    # Create subplots
    fig, ax = plt.subplots()
    bar_width = 0.1
    num_values = len(values)
    positions = range(len(values))  # Base positions for the values

    # Plot each column as a group of bars, one for each value
    for i, col_name in enumerate(count_col_names):
        bar_positions = [pos + i * bar_width for pos in positions]
        bar_heights = [counts[col_name][value] for value in values]
        ax.bar(bar_positions, bar_heights, width=bar_width, label=f'Column: {col_name}')

    # Set X-axis labels and ticks to be centered for each group of bars
    ax.set_xticks([pos + bar_width * (len(count_col_names) - 1) / 2 for pos in positions])
    ax.set_xticklabels(values)
    ax.set_xlabel('Values')
    ax.set_ylabel('Counts')
    ax.set_title('Counts of non-null values for each value across specified columns')
    ax.legend(title='Columns')
    plt.savefig('output/plot.png')  # Save the plot as a PNG file
    plt.close()

def parse_args():
    parser = argparse.ArgumentParser(description='Data manipulation tool')
    parser.add_argument('csv_file', type=str, help='CSV file path')
    parser.add_argument('--count', help='Column index to apply count', type=str)
    parser.add_argument('--values', nargs='+', help='List of values to count')
    parser.add_argument('--columns', nargs='+', help='List of columns to consider for counting', type=str)
    return parser.parse_args()

def run_server():
    port = 8000
    directory = "output"
    os.chdir(directory)  # Change to the 'output' directory

    class CustomHandler(SimpleHTTPRequestHandler):
        """HTTP Handler that serves files from the given directory."""
    
    httpd = HTTPServer(("", port), CustomHandler)
    print(f"Serving at port {port}. Navigate to http://localhost:{port}/plot.png to view the plot.")

    # Function to run the server in a separate thread
    def server_thread():
        httpd.serve_forever()
    
    # Start the server thread
    thread = threading.Thread(target=server_thread)
    thread.daemon = True  # This makes the thread exit when the main program does
    thread.start()

    # Wait for user input to shutdown
    input("Press Enter to stop the server and exit.\n")
    httpd.shutdown()  # Shutdown the server
    thread.join() 
    

def main():
    args = parse_args()
    df = load_csv(args.csv_file)
    if args.count and args.values and args.columns:
        count_and_graph(df, args.count, args.values, args.columns)
    run_server()

if __name__ == '__main__':
    main()        