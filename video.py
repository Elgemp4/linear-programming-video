import scipy

frames = 100
width = 232
height = 152
pixels = width * height
X  = None

def load_video(file):
    global X
    mat = scipy.io.loadmat(file)
    X = mat["X"]