import glob
import os
import cv2


def main(path, new_ext, old_ext):
    
    files = glob.glob(path + '/**/*.' + old_ext, recursive=True)

    for file in files:

        img = cv2.imread(file)

        new_file = file[:-len(old_ext)] + new_ext

        cv2.imwrite(new_file, img)

        os.remove(file)
        
        print(new_file)



if __name__ == '__main__' :


    path = '../pruebas'

    main(path, 'png', 'jpeg')