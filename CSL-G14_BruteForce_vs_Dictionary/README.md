# Brute Force vs Dictionary Attack – Time Comparison Tool

**Project Code:** CSL-G14
**Linked Syllabus Experiment:** Experiment 3 – Dictionary & Brute Force Attack (Cyber Security Lab, 7CS4-22)
**Student:** Tanuj Gupta (23ESKCY052)

## 1. What this project does

This tool compares two classic password-guessing techniques — the **Dictionary
Attack** and the **Brute Force Attack** — on a set of locally generated test
password hashes:

1. Builds a small wordlist (30 common test passwords).
2. Defines 6 test cases with varying **character set** (3 / 26 / 36 / 62
   characters) and **password length** (3 or 4).
3. Hashes each test password once with SHA-256 (as a real system would store it).
4. Cracks every hash twice — once with a Dictionary Attack, once with a Brute
   Force Attack — timing each attempt and recording success/failure.
5. Saves the raw results to `results.csv` and renders two graphs:
   - `time_comparison.png` – time taken by each method per test case (log scale)
   - `success_rate.png` – overall success rate of each method

## 2. Ethical note

No real account, password, website or network is touched. Every target
"password" is a dummy string chosen only to demonstrate the algorithms, and it
is hashed with SHA-256 before any attack runs against it — exactly like a real
leaked password database. Everything runs locally on your own machine.

## 3. Requirements

- Python 3.10+ (tested on Python 3.12)
- [matplotlib](https://matplotlib.org/) (the only third-party dependency)

Install the dependency if you don't already have it:

```bash
pip install matplotlib
```

## 4. How to run

```bash
python brute_vs_dictionary.py
```

This prints a live log of every attempt to the console and, once finished,
writes three files into the same folder:

| File | Description |
|---|---|
| `results.csv` | Raw table: test case, charset, length, method, success, attempts, time |
| `time_comparison.png` | Bar chart comparing time taken by each method |
| `success_rate.png` | Bar chart comparing overall success rate |

## 5. Project structure

```
.
├── brute_vs_dictionary.py   # main script (dictionary + brute force attacks)
└── README.md                # this file
```

## 6. Customising the experiment

Open `brute_vs_dictionary.py` and edit:

- `WORDLIST` – the dictionary attack's word list.
- `TEST_CASES` – each entry is `(label, charset, charset_name, length, password)`.
  Add, remove or change entries to try different character sets and lengths.
  Note: brute force time grows as `charset_size ^ length`, so very large
  charsets combined with long lengths can take a long time to finish.

## 7. Sample result (from the bundled run)

| Method | Success rate |
|---|---|
| Dictionary Attack | 50% (3 / 6) — fast, but only finds passwords that are in the wordlist |
| Brute Force Attack | 100% (6 / 6) — always finds the password, but gets much slower as charset/length grow |

This matches the theoretical expectation from Experiment 3: Dictionary attacks
are fast but limited to known words; Brute Force attacks are exhaustive but
scale poorly (`N^L` search space).
