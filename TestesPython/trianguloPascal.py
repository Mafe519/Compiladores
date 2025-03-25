def print_pascals_triangle(rows):
    for i in range(rows):
        num = 1
        for j in range(i + 1):
            if j == 0 or j == i:
                print("1", end=" ")
            else:
                num = num * (i - j + 1) // j
                print(num, end=" ")
        print()

# Solicita a quantidade de linhas para o Triângulo de Pascal
rows = int(input("Enter the number of rows: "))
print_pascals_triangle(rows)
