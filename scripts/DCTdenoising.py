import glob
import subprocess
import time

def get_images_files(path):

    files = glob.glob(path + '/**/*.*', recursive=True)
    return files


def run(sigma, input_image, output_image):
    
    seconds = time.time()
    bashCommand = "../ipol_methods/DCTdenoising-master/build/dctdenoising" + " " + str(sigma) + " " + input_image + " " + output_image
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print("Seconds = ", time.time() - seconds)	


def main(input_path, output_path, sigma):

    images_files = get_images_files(input_path)

    for image_file in images_files:
        output_image = output_path + image_file[len(input_path):]
        print("process image: ", image_file)
        run(sigma, image_file, output_image)



if __name__ == '__main__':
    input_path = "../dataset"
    input_path = "../pruebas"
    output_path = "../results/DCTdenoising"
    sigma = 20

    main(input_path, output_path, sigma)
