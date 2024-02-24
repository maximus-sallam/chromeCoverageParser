# chromeCoverageParser
A simple tool to parse Chrome DevTools coverage results, generating files containing only used lines and visualizing coverage analysis through a graph.

## Features
- Parses coverage data from Chrome DevTools' `.json` format.
- Generates files with only the used lines of code based on the coverage analysis.
- Creates a visual graph representing the total and used sizes of files to easily identify coverage opportunities.
- Saves the coverage graph as a high-resolution PNG file, ensuring unique filenames to prevent overwriting previous analyses.

## Prerequisites
Before using this tool, ensure you have the following Python packages installed:
- `matplotlib.pyplot` for generating the coverage graph.
- `click` for handling command-line arguments.

You can install these packages using pip:
```bash
$ pip install matplotlib click
```

## Usage

### Preparing Your Coverage Data
1. Extract the coverage data file (`coverage.json`) from Chrome DevTools. Instructions can be found [here](https://developers.google.com/web/updates/2019/01/devtools#coverage) or you can use any `*.json` file of the same format.

### Running the Parser
2. Run the parser using the command:
```bash
$ python3 parser.py <path_to_coverage.json>
```
Replace `<path_to_coverage.json>` with the path to your downloaded file. The tool will process all the files listed in the `coverage.json` and create new files with only the used lines of code according to the analysis.

### Viewing the Coverage Graph
3. After processing, the tool will generate a graph showing the total and used sizes of the files. This graph helps in visually identifying which files have the most unused code. The graph is saved as a high-resolution PNG image, with each execution saving a new file to prevent overwriting previous results.

## Contributing
Your contributions are welcome! If you have suggestions for improvements or encounter any issues, please feel free to submit an issue or pull request.
