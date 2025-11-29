## Installation

The required dependencies are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

## Usage

The application uses a command-line interface (CLI).

### Basic Command

Execute the main script with the desired options and the data file path.

```bash
python main.py [OPTIONS] FILE
```

### Options

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--method` | `linprog` or `median` | `linprog` | Specifies the method used for background/foreground separation. |
| `--refine` | Flag | `False` | Enables iterative refinement of the background ($b$) and illumination ($a$) vectors. |
| `FILE` | Path | `./data/data.mat` | Positional argument: Path to the input video data file (matrix $X$). |

### Examples

1.  **Run with Linear Programming (Default Method):**

    ```bash
    python main.py
    # OR
    python main.py --method linprog ./path/to/my_data.mat
    ```

2.  **Run with Median-based Method:**

    ```bash
    python main.py --method median
    ```

3.  **Run with Iterative Refinement:**

    ```bash
    python main.py --method linprog --refine
    ```

### Output

The program generates a video file named `result.mp4` containing the extracted **foreground** (residuals $F$).