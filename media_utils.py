import matplotlib.pyplot as plt
import numpy as np

from video import width, height

def extractImage(X, j):
  return X[:,j]


def displayImage(img):
  array_1d = np.array(img)
  array_2d = array_1d.reshape(width, height)

  plt.axes().set_axis_off()
  plt.imshow(array_2d.T, cmap='gray_r')
  plt.show()


def save_as_video(video, video_name):
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    fig, ax = plt.subplots()
    ax.set_axis_off()

    def get_formatted_data(frame_index):
        img = extractImage(video, frame_index)
        array_1d = np.array(img)
        array_2d = array_1d.reshape(width, height)
        return array_2d.T

    first_frame = get_formatted_data(0)
    vmin, vmax = np.min(video), np.max(video)

    im = ax.imshow(first_frame, cmap='gray_r', animated=True, vmin=vmin, vmax=vmax)
    title = ax.set_title("Frame 0")

    def update(i):
        data = get_formatted_data(i)

        im.set_data(data)
        title.set_text(f"Frame {i}")

        return [im, title]

    print("Génération de la vidéo...")

    ani = animation.FuncAnimation(fig, update, frames=100, interval=100, blit=True)

    # Sauvegarde
    ani.save(video_name, writer='ffmpeg', fps=20)

    plt.close(fig)  # Ferme la fenêtre pour ne pas bloquer