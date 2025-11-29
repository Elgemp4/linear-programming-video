import click
from click import argument
from numpy.f2py.auxfuncs import isfalse
from pygments.lexer import default

from media_utils import save_as_video
from method.linprog import linprog_compute_a, linprog_compute_b
from method.median import median_compute_a, median_compute_b
import numpy as np


@click.command()
@click.option("--method",
              default="linprog",
              prompt="Select your desired method : ",
              type=click.Choice(["linprog", "median"], case_sensitive=False),
              help="The used method to resolve the problem (solver for linprog or median for median calculations")
@click.option("--refine",
              default=False,
              is_flag=True,
              help="Refine the found a and b")
@argument("file", default="./data/data.mat")
def resolve_problem(method, file, refine):
    import video
    video.load_video(file)  # Call the loading function
    X = video.X
    #save_as_video(X, "./start.mp4")

    if method == "linprog":
        compute_a = linprog_compute_a
        compute_b = linprog_compute_b
    else:
        compute_a = median_compute_a
        compute_b = median_compute_b

    print("Computing b")
    b = compute_b(X)
    print("Computing a")
    a = compute_a(X, b)
    B = np.outer(b, a)
    if refine:
        print("Refining the solution")
        print("Initial error :", np.sum(np.abs(X - np.outer(b, a))))
        ITERATIONS = 5

        for i in range(ITERATIONS):
            b = compute_b(X, a)
            a = compute_a(X, b)
            print("Error after iteration ", i + 1, " ", np.sum(np.abs(X - np.outer(b, a))))

    residuals = X - B
    save_as_video(residuals, "result.mp4")

if __name__ == "__main__":
    resolve_problem()