#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import random
from taller_3.solucion_dinamica import top_down, bottom_up

# Permitir recursiones más profundas en top_down
sys.setrecursionlimit(10000)

def generate_sequence(n, seed=None):
    if seed is not None:
        random.seed(seed)
    return [random.randint(1, 100) for _ in range(n)]

def measure_time(seq, func):
    start = time.perf_counter_ns()
    func(seq)
    end = time.perf_counter_ns()
    return end - start

def run_experiments(min_n, max_n, step_n, output_file):
    with open(output_file, 'w') as f:
        f.write("n,top_down_ns,bottom_up_ns\n")
        for n in range(min_n, max_n + 1, step_n):
            seq = generate_sequence(n, seed=42)
            # Top‑Down (puede rebasar el límite de recursión)
            try:
                td_time = measure_time(seq, top_down)
                td_str = str(td_time)
            except RecursionError:
                td_str = ""
            # Bottom‑Up
            bu_time = measure_time(seq, bottom_up)
            bu_str = str(bu_time)
            # Escribir línea CSV
            f.write(f"{n},{td_str},{bu_str}\n")
            # Mostrar por consola
            td_disp = td_str if td_str else "ERR"
            print(f"n={n:4d} → TopDown: {td_disp:>8} ns, BottomUp: {bu_str:>8} ns")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python main.py min_n max_n step_n output_file")
        sys.exit(1)
    min_n       = int(sys.argv[1])
    max_n       = int(sys.argv[2])
    step_n      = int(sys.argv[3])
    output_file = sys.argv[4]
    run_experiments(min_n, max_n, step_n, output_file)