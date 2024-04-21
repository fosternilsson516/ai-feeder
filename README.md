# Excel Viz CLI

## Introduction
Excel Viz CLI is a command-line interface (CLI) tool that allows users to visualize data from CSV files as PNG graphs. Users can specify the path to a CSV file along with certain arguments, and then view the resulting graph by navigating to `localhost:8000` on their browser.

## Prerequisites
Before using Excel Viz CLI, ensure you have the following installed on your system:
- **Docker**: Necessary for running the containerized version of the tool.
- **Web Browser**: Required to view the generated graph on `localhost:8000`.

## Installation
1. **Pull the Docker Image**  
   Pull the latest version of Excel Viz CLI from Docker Hub in command line:
   ```bash
   docker pull fosternilsson/excel_viz_cli:1.2

### Usage

To use the tool, run the following command in your terminal. Replace `full/path/to/file.csv` with the actual path to your CSV file.

    docker run --rm -it -p 8000:8000 -v "full/path/to/file.csv:/data/file_name.csv" fosternilsson/excel_viz_cli:1.2 /data/file_name.csv --count --values --columns

#### Parameters Explained
- `--count` : Specifies the name of the column to perform a count aggregation on.
- `--values` : Determines which rows from the specified column will appear on the x-axis of the graph.
- `--columns` : Other column names in the CSV whose values are to be counted and displayed.

### Viewing the Graph

After running the command, open your web browser and navigate to:
[http://localhost:8000](http://localhost:8000)

