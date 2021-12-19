import glob
import subprocess


def get_images_files(path):

    files = glob.glob(path + '/**/*.*', recursive=True)
    return files


def run(sigma, input_image, output_image):
    
    bashCommand = "../ipol_methods/nlmp_1.2/NLMeansP" + " " + input_image + " " + str(sigma) + " " + "0" + " " + input_image + " " + output_image
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
    output_path = "../results/nlmp"
    sigma = 20

    main(input_path, output_path, sigma)
