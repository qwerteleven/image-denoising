import glob
import subprocess
import bm3d 
import matplotlib.pyplot as plt
import vs

def get_images_files(path):

    files = glob.glob(path + '/**/*.*', recursive=True)
    return files


def run(sigma, input_image, output_image):
    core = vs.get_core()
    ref = bm3d.Basic(input_image, sigma=[10,7])
    flt = bm3d.Final(input_image, ref, sigma=[10,7])


    plt.imshow(flt)
    plt.show()
    


def main(input_path, output_path, sigma):

    images_files = get_images_files(input_path)

    for image_file in images_files:
        output_image = output_path + image_file[len(input_path):]
        print("process image: ", image_file)
        run(sigma, image_file, output_image)
        break




if __name__ == '__main__':
    input_path = "../dataset"
    output_path = "../results/nlmp"
    sigma = 20

    main(input_path, output_path, sigma)
