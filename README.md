
# XSS Detection Project

This project is a **Cross-Site Scripting (XSS) vulnerability detection system** using two machine learning models: one Transformer-based and one LSTM-based.

User input is sent to both models.  
If **at least one model** detects a possible XSS attack, the request is **rejected**.

---

## 🔧 Project Structure

| File / Folder         | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `server.py`           | The main Flask server. Run it with `python server.py`.                 |
| `config/`             | Stores settings like port, host, and model file names.                 |
| `config/settings.py`  | Contains variables such as `PORT`, `HOST`, and model paths.            |
| `src/main.html`       | The user interface (UI) of the system.                                 |
| `newwnv/`             | Virtual environment folder for **Windows**.                            |
| `requirements.txt`    | Python dependencies used in the virtual environment.                   |
| `tests/test.txt`      | Contains example XSS payloads like `<svg onload=alert('1')>`.          |
| `dmzo_normal.csv`     | Safe inputs. These inputs do **not** contain XSS.                      |
| `xssed.csv`           | Dangerous inputs. These inputs **contain XSS**.                        |
| `tokenizer.pkl`       | A saved tokenizer used to convert input text into sequences for models.|
| `*.ipynb`             | Jupyter notebooks used to train the models.                            |
| `*.h5`                | Trained model files (LSTM and Transformer).                            |

---

## ⚙️ Running the Project

> ⚠️ This project was developed on **Windows**.
### 0. Installation & Download:
```bash
git clone https://github.com/GTU-CyberAI/xss-detection.git

```

### 1. Activate the virtual environment:

```bash
newwnv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Run the server:

```bash
python server.py         # Windows
python3 server.py        # (on Ubuntu, if dependencies are compatible)
```

---

## How It Works

- User writes input into the webpage.
- The input is sent to the Flask API.
- Two models analyze the input:
  - If **any model** says the input is dangerous → system shows warning.
  - If both models say input is clean → input is shown in the UI.

---

## Requirements

For necessary versions, install required packages with:

```bash
pip install -r requirements.txt
```

---

## Notes

- This project uses `Flask`, `TensorFlow`, and `pickle` for backend processing.
- HTML, CSS, and JavaScript are used for the front-end.
- The tokenizer (`tokenizer.pkl`) is essential for preparing the input for both models.
- It works in http://localhost:5000/ . In order to change the port, check the /config/settings.py
---

Feel free to test the system using the example payloads in `tests/test.txt`.
