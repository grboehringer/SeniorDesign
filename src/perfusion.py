import cv2
import numpy as np
import matplotlib.pyplot as plt

class Perfusion():
    def __init__(self):
        self.intensityThreshold = 20

        """|R-B| > DT at lowest color value"""
        self.differenceThreshold = 76

    def algorithm(self, img):
        """Mean of the RGB value of each pixel"""
        intensity = np.mean(img, axis=2)    # Find intensity

        red = img[:,:,2]
        green = img[:,:,1]
        blue = img[:,:,0]


        #dt = np.where(intensity > self.intensityThreshold, self.differenceThreshold / 3, self.differenceThreshold)

        boolean = np.abs(red - green) > self.differenceThreshold
        boolean = boolean | np.abs(red - blue) > self.differenceThreshold
        boolean = boolean | np.abs(green - blue) > self.differenceThreshold

        """Thresholded RGB values"""
        perfusion = intensity * boolean
        print('Intensity: '+ str(intensity))

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

    def changeThreshold(self, intensityThreshold, differenceThreshold):
        self.intensityThreshold = intensityThreshold
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
    