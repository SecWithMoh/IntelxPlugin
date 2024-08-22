# JSON to SQLite with Command Execution and File Management for IntelX SDK

This Python script is designed as a plugin for the **IntelX SDK**, enabling users to process JSON files, store their contents in an SQLite database, and automate the execution of `intelx.py` commands. This script facilitates the download of data using `systemid` and `bucket` information stored in the database, with built-in file management for handling `.bin` files.

### Workflow Overview:

1. **Initial Search**: 
   - First, perform a search using `intelx.py` and save the raw results into a JSON file. This step gathers the initial dataset from IntelX.
   - Example command:
     ```bash
     python3 intelx.py -search "target.com" -bucket leaks.logs --raw >> results.json
     ```
   - This command will search the **IntelX** database for entries related to `target.com` in the `leaks.logs` bucket and save the results as raw JSON in the `results.json` file.

2. **Process JSON and Store in SQLite**:
   - After obtaining the search results in the JSON file, this script reads the JSON file and dynamically stores its contents in an SQLite database. It automatically creates tables that match the structure of the JSON data and prevents duplicate entries using unique constraints (e.g., `systemid`).

3. **Automated Command Execution**:
   - The script retrieves the stored data from the SQLite database and executes `intelx.py` commands to download the corresponding files. It uses the `systemid` as the `-download` parameter and the `bucket` as the `-bucket` parameter. The user's API key is also passed to the command.

4. **File Management**:
   - After the download, the script moves all files with a `.bin` extension to a specified output directory, keeping your workspace organized.

### Features:
- **Dynamic JSON Parsing**: Reads and processes a JSON file with varying structures, storing the data in an SQLite database. It automatically creates tables with columns matching the JSON fields.
- **Duplicate Prevention**: Uses a unique constraint (e.g., `systemid`) to ensure that duplicate records are not inserted into the database.
- **Command Execution**: Executes `intelx.py` commands based on the data in the SQLite database. The script runs `intelx.py` with the `-download` and `-bucket` parameters retrieved from the database, using the API key provided by the user.
- **File Management**: After executing the command, the script moves all downloaded `.bin` files to a specified output directory.
- **SDK Integration**: The script is designed to work seamlessly with the **IntelX SDK**, automating common tasks such as downloading data from IntelX buckets.
- **User-Friendly Input**: The script prompts the user for necessary inputs, such as the JSON file path, API key, and output directory.

### Usage:
1. **Clone the Repository**:
   ```bash
   git clone IntelxPlugin
   cd IntelxPlugin
   ```

2. **Install Dependencies**:
   This script requires Python 3 and the **IntelX SDK**. Ensure you have the necessary dependencies, such as SQLite and Python’s `json`, `os`, `shutil`, and `subprocess` modules. Install the IntelX SDK if you haven't already:
   ```bash
    pip install "intelx @ git+https://github.com/IntelligenceX/SDK#subdirectory=Python"
   ```
  ```bash
   git clone https://github.com/IntelligenceX/SDK
   cd Python
  pip3 install -e . 
  ```
3. **Run an Initial Search**:
   Use `intelx.py` to perform a search and save the results as JSON. For example:
   ```bash
   python3 intelx.py -search "target.com" -bucket leaks.logs --raw >> results.json
   ```

4. **Run the Script**:
   ```bash
   python3 script.py
   ```
   - Enter the JSON file path (`results.json`) when prompted.
   - Provide your `intelx.py` API key.
   - Specify the output directory for `.bin` files.

5. **Automated Workflow**:
   - The script reads the JSON file, stores the data in an SQLite database, executes the required `intelx.py` commands, and moves `.bin` files to the output directory.

### IntelX SDK Integration:

This plugin automates interactions with the IntelX SDK, making it easier to handle large datasets by streamlining data download and file management processes. By integrating with `intelx.py`, the script simplifies repetitive tasks for users working with IntelX data.

### License:

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**. You are free to modify, distribute, and use the software in accordance with the terms of this license. For more details, please see the [LICENSE](LICENSE) file in this repository.



