def calculate_determinant(matrix: list[list[complex]]) -> complex:
    if len(matrix) != len(matrix[0]):
        raise ValueError('Your matrix must be of a square type.')

    m_size: int = len(matrix)

    if m_size < 1:
        raise ValueError('Matrix size must be a positive integer.')
    elif m_size == 1:
        return matrix[0][0]
    else:
        mult = 1
        new_det = 0
        for excluded_row in range(m_size):
            new_matrix = []
            for row_num in range(m_size):
                if row_num == excluded_row:
                    continue
                new_matrix.append(matrix[row_num][1:])
            new_det += mult * matrix[excluded_row][0] * calculate_determinant(new_matrix)
            mult *= -1

        return new_det


def solve_linear_system(exp_matrix: list[list[complex]]) -> list[complex | int] | None:
    left_coeffs: list[list[complex]] = []
    right_coeffs: list[complex] = []
    size: int = len(exp_matrix)

    for row in exp_matrix:
        left_coeffs.append(row[:-1])
        right_coeffs.append(row[-1])

    main_det = calculate_determinant(left_coeffs)
    if main_det == 0j:
        return None

    roots: list[complex | int] = []
    for working_column in range(size):
        modified_matrix = []
        for row_num in range(size):
            modified_matrix.append(left_coeffs[row_num].copy())
            modified_matrix[row_num][working_column] = right_coeffs[row_num]

        r: complex | int = calculate_determinant(modified_matrix) / main_det
        if r.imag == 0:
            r = round(r.real, 3)
        else:
            r = complex(round(r.real, 3), round(r.imag, 3))

        roots.append(r)

    return roots


if __name__ == '__main__':
    print(calculate_determinant([[1, complex(2, 2)], [complex(3, 1), complex(4, -11)]]))  # -19j
