import cv2
import numpy as np
import matplotlib.pyplot as plt

class Perfusion():
    def __init__(self):
        """|R-B| > DT at lowest color value"""
        self.differenceThreshold = 76

    def algorithm(self, img, coord):
        """Mean of the RGB value of each pixel"""

        if coord != None:
            if coord[0][0] < coord[1][0]:
                img[:int(coord[0][0]), :, :] = 0
                img[int(coord[1][0]):, :, :] = 0
            else:
                img[:int(coord[1][0]):, :, :] = 0
                img[int(coord[0][0]):, :, :] = 0
            if coord[0][1] < coord[1][1]:
                img[:, :int(coord[0][0]), :] = 0
                img[:, int(coord[1][0]):, :] = 0
            else:
                img[:, :int(coord[1][0]):, :] = 0
                img[:, int(coord[0][0]):, :] = 0


        intensity = np.mean(img, axis=2)    # Find intensity

        red = img[:,:,2]
        green = img[:,:,1]
        blue = img[:,:,0]

        boolean = np.abs(red - green) > self.differenceThreshold
        boolean = boolean | np.abs(red - blue) > self.differenceThreshold
        boolean = boolean | np.abs(green - blue) > self.differenceThreshold

        """Thresholded RGB values"""
        perfusion = intensity * boolean

        """Percent Colored Calculation"""
        percent_colored = (np.count_nonzero(boolean))/(np.size(boolean))*100
        # print('Number of True Values: ' + str(np.count_nonzero(boolean)))
        # print('Size: ' + str(np.size(boolean)))
        print('Percent Colored: ' + str(format(percent_colored, '.2f')) + '%')

        """Returns the mean of the Thresholded RGB values"""
        return np.mean(perfusion)

    def video(self, filename):
        vid = cv2.VideoCapture(filename)
        if not vid.isOpened():
            print("Error opening video")
            return None
        perfusions = []
        while vid.isOpened():
            ret, frame = vid.read()
            cv2.imshow('cool', frame)
            if ret:
                perfusion, doop = self.algorithm(frame)
                perfusions.append(perfusion)
                print(perfusion)
            else:
                vid.release()
                return perfusions
        
            if cv2.waitKey(10) & 0xff == ord('q'):
                vid.release()
                return perfusions
            cv2.imshow('doop', np.uint8(doop))

    def image(self, filename, coord = None):
        self.img = cv2.imread(filename)
        return self.algorithm(self.img, coord)

    def changeThreshold(self, differenceThreshold):
        self.differenceThreshold = differenceThreshold

    def rgb(self, x, y):
        return self.img[y, x, 2], self.img[y, x, 1], self.img[y, x, 0]
        


if __name__ == '__main__':
    '''
    img_filename = select_file()
    
    perObj = Perfusion()
    perfusionVal, perfusion, dt = perObj.algorithm(img_filename)

    print(perfusionVal)
    plt.imshow(dt, 'gray')
    plt.show()
    '''
    obj = Perfusion()
    perfusion = obj.image('images/AdeLow.png')
    red, green, blue = obj.rgb(25, 25)
    print(f'{red}, {green}, {blue}')
    