def calcular_operaciones(A, B, C, D):
    # 1. (A*B) + (C*D)
    op1 = (A * B) + (C * D)
    print(f"1. (A*B) + (C*D) = {op1}")

    # 2. (A*B) - (C*D)
    op2 = (A * B) - (C * D)
    print(f"2. (A*B) - (C*D) = {op2}")

    # 3. (A*C) + (B*D)
    op3 = (A * C) + (B * D)
    print(f"3. (A*C) + (B*D) = {op3}")

    # 4. (A*C) - (B*D)
    op4 = (A * C) - (B * D)
    print(f"4. (A*C) - (B*D) = {op4}")

    # 5. (A*D) + (C*B)
    op5 = (A * D) + (C * B)
    print(f"5. (A*D) + (C*B) = {op5}")

    # 6. (A*D) - (C*B)
    op6 = (A * D) - (C * B)
    print(f"6. (A*D) - (C*B) = {op6}")

    # 7. (C*D) - (A*B)
    op7 = (C * D) - (A * B)
    print(f"7. (C*D) - (A*B) = {op7}")

    # 8. (B*D) - (A*C)
    op8 = (B * D) - (A * C)
    print(f"8. (B*D) - (A*C) = {op8}")

    # 9. (C*B) - (A*D)
    op9 = (C * B) - (A * D)
    print(f"9. (C*B) - (A*D) = {op9}")

    # 10. A^B (en Python se escribe A**B)
    op10 = A**B
    print(f"10. A^B = {op10}")

    # 11. -(A^B)
    op11 = -(A**B)
    print(f"11. -(A^B) = {op11}")

    # 12. A^2 - B^2
    op12 = (A**2) - (B**2)
    print(f"12. A^2 - B^2 = {op12}")

    # 13. A^2 - C^2
    op13 = (A**2) - (C**2)
    print(f"13. A^2 - C^2 = {op13}")

    # 14. A^2 - D^2
    op14 = (A**2) - (D**2)
    print(f"14. A^2 - D^2 = {op14}")

    # 15. B^2 - A^2
    op15 = (B**2) - (A**2)
    print(f"15. B^2 - A^2 = {op15}")

    # 16. B^2 - C^2
    op16 = (B**2) - (C**2)
    print(f"16. B^2 - C^2 = {op16}")

    # 17. B^2 - D^2
    op17 = (B**2) - (D**2)
    print(f"17. B^2 - D^2 = {op17}")

    # 18. -A
    op18 = -A
    print(f"18. -A = {op18}")

    # 19. A + B + C + D
    op19 = A + B + C + D
    print(f"19. A + B + C + D = {op19}")

    # 20. A - B + C + D
    op20 = A - B + C + D
    print(f"20. A - B + C + D = {op20}")

    # 21. A + B - C + D
    op21 = A + B - C + D
    print(f"21. A + B - C + D = {op21}")

    # 22. A + B + C - D
    op22 = A + B + C - D
    print(f"22. A + B + C - D = {op22}")

    # 23. B - A + C + D
    op23 = B - A + C + D
    print(f"23. B - A + C + D = {op23}")

    # 24. 2A + 2B
    op24 = 2*A + 2*B
    print(f"24. 2A + 2B = {op24}")

    # 25. 2A - 2B
    op25 = 2*A - 2*B
    print(f"25. 2A - 2B = {op25}")

    # 26. (2A + 2B) + (C*D)
    op26 = (2*A + 2*B) + (C * D)
    print(f"26. (2A + 2B) + (C*D) = {op26}")

    # 27. (C*D) - (A^2 + 2B)
    op27 = (C * D) - (A**2 + 2*B)
    print(f"27. (C*D) - (A^2 + 2B) = {op27}")

# Ejemplo de uso:
calcular_operaciones(15, 15, 7, 7)