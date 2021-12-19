import sys
import glob
import matplotlib.pyplot as plt
import cv2

def main(img_index, sigma, path_results):


    f, axarr = plt.subplots(2, 4, figsize=(35, 25), sharex=True, sharey=True)

    f.suptitle('Sigma visualization', fontsize=16)



    for i in range(sigma[0], sigma[1], sigma[2]):

        img_data = get_images_files(path_results + "/sigma_" + str(i) + "_")

        imgfile = img_data[img_index]

        print(int(round((i - 1) / 5, 0)) % 4, "A")
        print(int(round((i - 1) / 30, 0)), "B")


        axarr[int(round((i - 1) / 30, 0)), int(round((i - 1) / 5, 0)) % 4].imshow(cv2.imread(imgfile)[:, :, ::-1])
        axarr[int(round((i - 1) / 30, 0)), int(round((i - 1) / 5, 0)) % 4].set_title(" SIGMA = " + str(i))


    plt.show()

    print('done')



def get_images_files(path):

    files = glob.glob(path + '/*.*', recursive=True)

    return sorted(files, key=lambda x : str(x))



if __name__ == '__main__':

    img_index = int(sys.argv[1])

    sigma = (1, 40, 5)

    path_results = "../results/BM3D_gpu"

  

    main(img_index, sigma, path_results)