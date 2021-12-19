import glob
import subprocess


def get_images_files(path):

    files = glob.glob(path + '/**/*.*', recursive=True)
    return files


def run(sigma, input_image, output_image):

    bashCommand = ("../ipol_methods/bm3d/build/bm3d" + " " +
                    input_image  + " " + 
                    str(sigma)   + " " +
                    output_image + " " +
                    "-useSD_wien -tau_2d_hard bior -tau_2d_wien dct -color_space opp"
    )


    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def main(input_path, output_path, sigma):

    images_files = get_images_files(input_path)

    for image_file in images_files:
        output_image = output_path + image_file[len(input_path):]
        print("process image: ", image_file)
        run(sigma, image_file, output_image)



if __name__ == '__main__':
    input_path = "../dataset"
    output_path = "../results/BM3D"
    sigma = 20

    main(input_path, output_path, sigma)
