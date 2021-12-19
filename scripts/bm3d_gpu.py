import glob
import subprocess
import time
import os

def get_images_files(path):

    files = glob.glob(path + '/**/*.*', recursive=True)
    return files


def run(sigma, input_image, output_image):

    seconds = time.time()
    bashCommand = ("../ipol_methods/bm3d-gpu/build/bm3d" + " " +
                    input_image  + " " + 
                    output_image + " " +
                    str(sigma)   + " " +
                    "color"
    )


    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print("Seconds = ", time.time() - seconds)	


def main(input_path, output_path, sigma):

    images_files = get_images_files(input_path)

    for image_file in images_files:

        for i in range(sigma[0], sigma[1], 5):
            output_path_sigma = output_path + "/sigma_" + str(i) + "_/"
            if not os.path.exists(output_path_sigma):
                os.makedirs(output_path_sigma)


            output_image = output_path_sigma + image_file[len(input_path):].split('/')[-1]
            print("process image: ", image_file)
            run(i, image_file, output_image)



if __name__ == '__main__':
    input_path = "../dataset"
    input_path = "../pruebas"
    output_path = "../results/BM3D_gpu"
    sigma = (1, 40)

    main(input_path, output_path, sigma)
