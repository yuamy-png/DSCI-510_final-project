# DSCI 510 Final Project

**Team Members**

* Amy Yu

---

## Project Overview

This project collects, cleans, analyzes, and visualizes data as part of the DSCI 510 final project requirements. The repository follows the structure specified by the course, including separate folders for data, source code, and results.

---

## Repository Structure

```
DSCI-510_final-project/
├── README.md
├── requirements.txt
├── project_proposal.pdf
├── data/
│   ├── raw/
│   └── processed/
├── results/
│   ├── article_metrics.csv
│   ├── word_frequency.csv
│   ├── figures/
│   └── final_report.pdf
├── src/
│   ├── get_data.py
│   ├── clean_data.py
│   ├── run_analysis.py
│   ├── visualize_results.py
│   └── utils/
```

---

## Setup Instructions

### 1. Create a Virtual Environment

From the root directory of the project:

```bash
python3 -m venv venv
```

Activate the virtual environment:

* **macOS / Linux**

```bash
source venv/bin/activate
```

* **Windows**

```bash
venv\Scripts\activate
```

---

### 2. Install Required Libraries

With the virtual environment activated, install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Running the Project

All scripts should be run from the **root directory** of the repository.

### 3. Data Collection

Run the data collection script to fetch and save raw data:

```bash
python src/get_data.py
```

Raw data will be saved in:

```
data/raw/
```

---

### 4. Data Cleaning

Run the data cleaning script to process raw data:

```bash
python src/clean_data.py
```

Cleaned data will be saved in:

```
data/processed/
```

---

### 5. Data Analysis

Run the analysis script:

```bash
python src/run_analysis.py
```

This step generates analysis outputs such as CSV files in:

```
results/
```

---

### 6. Data Visualization

Generate visualizations by running:

```bash
python src/visualize_results.py
```

Figures will be saved in:

```
results/figures/
```

---

## Notes

* Ensure the virtual environment is activated before running any scripts.
* All file paths are relative to the project root.
* This repository includes data and results files to comply with course submission requirements.

---

## Contact

For questions regarding this project, please contact: yuamy@usc.edu
