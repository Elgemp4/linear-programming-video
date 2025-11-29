from multiprocessing import Pool
from os import cpu_count

from scipy.optimize import linprog
from scipy.sparse import coo_matrix

from video import frames, pixels


def linprog_compute_b(X, a=None):
    if a is None:
        a = [1.0] * frames

    b = [1.0] * pixels

    percentage = -1
    # Frames + 1 variables de décision (b et une variable par image (tj))
    c = [1] * (frames + 1)
    # Mise de b à zéro (b ne participe pas dans l objectif)
    c[0] = 0

    A_ub = [[0] * (frames + 1) for _ in range(2 * frames)]

    bounds = [[None, None] for _ in range(frames + 1)]

    for j in range(frames):
        A_ub[j * 2][0] = -1
        A_ub[j * 2][j + 1] = -1

        A_ub[j * 2 + 1][0] = 1
        A_ub[j * 2 + 1][j + 1] = -1

    for i in range(pixels):
        prev = percentage
        percentage = round((i / pixels) * 100.0)
        if (percentage != prev):
            #clear_output()
            print(f"{percentage}%")

        # Création de la matrice de décision pour pour frames + 1 variables avec 2 * frames contraintes
        b_ub = [0] * (2 * frames)
        for j in range(frames):
            # Deux b par tj
            b_ub[j * 2] = -X[i, j]
            b_ub[j * 2 + 1] = X[i, j]

        model = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)
        b[i] = model.x[0]

    return b

def solve_for_frame(X, c, A_ub_sparse, bounds, j):
    # Création de b_ub (dépend de j)
    b_ub = [0] * (2*pixels)
    for i in range(pixels):
        b_ub[i*2] = -X[i,j]
        b_ub[i*2+1] = X[i,j]

    model = linprog(c=c, A_ub=A_ub_sparse, b_ub=b_ub, bounds=bounds, method='highs')

    if model.success:
        print(f"Frame {j} terminée.")
        return model.x[0]
    else:
        print(f"ERREUR sur frame {j}: {model.message}")
        return 0 # ou None

def linprog_compute_a(X, b):
    a = [1.0] * frames

    percentage = -1

    # Frames + 1 variables de décision (aj et une variable par pixel (tj))
    c = [1] * (pixels + 1)
    # Mise de a à zéro (a ne participe pas dans l objectif)
    c[0] = 0
    A_ub_data = []
    A_ub_rows = []
    A_ub_cols = []

    def insertIntoA_ub(row, col, data):
        A_ub_data.append(data)
        A_ub_rows.append(row)
        A_ub_cols.append(col)

    print("insert a_ub")
    for i in range(pixels):
        insertIntoA_ub(i * 2, 0, -b[i])
        insertIntoA_ub(i * 2, i + 1, -1)

        insertIntoA_ub(i * 2 + 1, 0, b[i])
        insertIntoA_ub(i * 2 + 1, i + 1, -1)
    print("prepared")

    bounds = [[None, None]]
    bounds.extend([[0, None] for _ in range(pixels)])

    A_ub_sparse = coo_matrix((A_ub_data, (A_ub_rows, A_ub_cols)), shape=(2 * pixels, pixels + 1))
    print("created a_ub")
    frame_indices = list(range(frames))

    # Créez un "Pool" de workers (autant que de cœurs CPU)
    num_cores = cpu_count()
    print(f"Lancement des calculs sur {num_cores} coeurs...")
    arg_list = [(X, c, A_ub_sparse, bounds, j) for j in frame_indices]
    with Pool(processes=num_cores) as pool:
        # pool.map applique la fonction 'solve_for_frame' à chaque élément de 'frame_indices'
        # et retourne les résultats dans l'ordre
        a = pool.starmap(solve_for_frame, arg_list)


    return a