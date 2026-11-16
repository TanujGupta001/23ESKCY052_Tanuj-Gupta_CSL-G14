"""
Project      : Brute Force vs Dictionary Attack - Time Comparison Tool
Project Code : CSL-G14
Linked Exp.  : Experiment 3 - Dictionary & Brute Force Attack
Student      : Tanuj Gupta (23ESKCY052)

IMPORTANT (Ethical use):
This script never touches a real account or a live system. It generates a
small set of TEST passwords locally, hashes them with SHA-256 to imitate a
leaked "password database", and then tries to recover those same test
passwords using (a) a Dictionary Attack and (b) a Brute Force Attack. All
activity happens on this machine only, using dummy data, exactly as
required by the lab's Ethical Declaration.

What the script does:
1. Builds a small dictionary (wordlist) of common test passwords.
2. Builds a set of target "test accounts", each with a password of a
   chosen length drawn from a chosen character set, and stores only the
   SHA-256 hash of each password (as a real system would).
3. Cracks every target hash twice - once with a Dictionary Attack and once
   with a Brute Force Attack - recording the time taken, number of
   attempts and whether the attack succeeded.
4. Saves the raw results to results.csv and renders two graphs:
   - time_comparison.png   : time taken by each method per test case
   - success_rate.png      : overall success rate of each method
"""

import csv
import hashlib
import itertools
import string
import time

import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 1. Dummy dictionary (wordlist) - a handful of commonly-used test
#    passwords. None of these belong to a real person or account.
# ----------------------------------------------------------------------
WORDLIST = [
    "password", "123456", "qwerty", "letmein", "admin", "welcome",
    "monkey", "dragon", "master", "sunshine", "princess", "football",
    "baseball", "iloveyou", "trustno1", "abc123", "password1",
    "qwerty123", "000000", "111111", "123123", "root", "toor",
    "changeme", "test", "test123", "guest", "CAB", "cat", "frog",
]


def sha256_hash(password: str) -> str:
    """Return the SHA-256 hex digest of a password (how a real system
    would store it, instead of the plain password itself)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ----------------------------------------------------------------------
# 2. Test cases: (label, charset, charset_name, length, real_password)
#    Lengths and character sets are deliberately varied, as required by
#    the project scope.
# ----------------------------------------------------------------------
CHARSET_ABC = "ABC"
CHARSET_LOWER = string.ascii_lowercase                       # 26 chars
CHARSET_LOWER_DIGITS = string.ascii_lowercase + string.digits  # 36 chars
CHARSET_ALNUM = string.ascii_letters + string.digits          # 62 chars

TEST_CASES = [
    # label,              charset,              charset_name,                length, password
    ("T1", CHARSET_ABC,          "ABC (3 chars)",               3, "CAB"),
    ("T2", "abc",                 "abc (3 chars)",               4, "cabc"),
    ("T3", CHARSET_LOWER,         "lower-case (26 chars)",       3, "cat"),
    ("T4", CHARSET_LOWER,         "lower-case (26 chars)",       4, "frog"),
    ("T5", CHARSET_LOWER_DIGITS,  "lower-case + digits (36 chars)", 3, "a1b"),
    ("T6", CHARSET_ALNUM,         "letters + digits (62 chars)", 3, "A1b"),
]


# ----------------------------------------------------------------------
# 3. Attack implementations
# ----------------------------------------------------------------------
def dictionary_attack(target_hash: str, wordlist=WORDLIST):
    """Try every word in the wordlist against the target hash."""
    attempts = 0
    start = time.perf_counter()
    for word in wordlist:
        attempts += 1
        if sha256_hash(word) == target_hash:
            elapsed = time.perf_counter() - start
            return True, attempts, elapsed
    elapsed = time.perf_counter() - start
    return False, attempts, elapsed


def brute_force_attack(target_hash: str, charset: str, max_length: int):
    """Try every combination of `charset`, from length 1 up to
    `max_length`, against the target hash (mirrors the algorithm used in
    Experiment 3(b))."""
    attempts = 0
    start = time.perf_counter()
    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            attempts += 1
            guess = "".join(combo)
            if sha256_hash(guess) == target_hash:
                elapsed = time.perf_counter() - start
                return True, attempts, elapsed
    elapsed = time.perf_counter() - start
    return False, attempts, elapsed


# ----------------------------------------------------------------------
# 4. Run every test case through both attacks and collect results
# ----------------------------------------------------------------------
def run_experiments():
    results = []
    print("=" * 70)
    print(" BRUTE FORCE vs DICTIONARY ATTACK - TIME COMPARISON TOOL")
    print("=" * 70)

    for label, charset, charset_name, length, real_password in TEST_CASES:
        target_hash = sha256_hash(real_password)
        print(f"\n[{label}] charset = {charset_name}, length = {length}")
        print(f"      target hash (SHA-256) = {target_hash[:20]}...")

        d_ok, d_attempts, d_time = dictionary_attack(target_hash)
        status = "FOUND" if d_ok else "NOT FOUND"
        print(f"      Dictionary Attack : {status:9s} | "
              f"attempts={d_attempts:<6d} | time={d_time:.6f}s")

        b_ok, b_attempts, b_time = brute_force_attack(target_hash, charset, length)
        status = "FOUND" if b_ok else "NOT FOUND"
        print(f"      Brute Force Attack: {status:9s} | "
              f"attempts={b_attempts:<6d} | time={b_time:.6f}s")

        results.append({
            "Test": label, "Charset": charset_name, "Length": length,
            "Method": "Dictionary", "Success": d_ok,
            "Attempts": d_attempts, "Time(s)": round(d_time, 6),
        })
        results.append({
            "Test": label, "Charset": charset_name, "Length": length,
            "Method": "Brute Force", "Success": b_ok,
            "Attempts": b_attempts, "Time(s)": round(b_time, 6),
        })

    return results


# ----------------------------------------------------------------------
# 5. Save results + draw graphs
# ----------------------------------------------------------------------
def save_csv(results, path="results.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\nResults saved to {path}")


def plot_time_comparison(results, path="time_comparison.png"):
    labels = sorted(set(r["Test"] for r in results))
    dict_times = [next(r["Time(s)"] for r in results
                        if r["Test"] == lbl and r["Method"] == "Dictionary")
                  for lbl in labels]
    brute_times = [next(r["Time(s)"] for r in results
                         if r["Test"] == lbl and r["Method"] == "Brute Force")
                   for lbl in labels]

    x = range(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([i - width / 2 for i in x], dict_times, width, label="Dictionary Attack")
    ax.bar([i + width / 2 for i in x], brute_times, width, label="Brute Force Attack")
    ax.set_yscale("log")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_xlabel("Test Case")
    ax.set_ylabel("Time taken (seconds, log scale)")
    ax.set_title("Time Taken: Dictionary Attack vs Brute Force Attack")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print(f"Graph saved to {path}")


def plot_success_rate(results, path="success_rate.png"):
    methods = ["Dictionary", "Brute Force"]
    rates = []
    for m in methods:
        subset = [r for r in results if r["Method"] == m]
        success = sum(1 for r in subset if r["Success"])
        rates.append(100.0 * success / len(subset))

    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(methods, rates, color=["#4C72B0", "#DD8452"])
    ax.set_ylim(0, 110)
    ax.set_ylabel("Success rate (%)")
    ax.set_title("Overall Success Rate (6 test cases)")
    for bar, rate in zip(bars, rates):
        ax.text(bar.get_x() + bar.get_width() / 2, rate + 2,
                f"{rate:.0f}%", ha="center", fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print(f"Graph saved to {path}")


if __name__ == "__main__":
    all_results = run_experiments()
    save_csv(all_results)
    plot_time_comparison(all_results)
    plot_success_rate(all_results)
    print("\nDone. See results.csv, time_comparison.png and success_rate.png")
