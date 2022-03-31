import cv2
import numpy as np
import matplotlib.pyplot as plt

class Perfusion():
    def __init__(self):
        self.intensityThreshold = 20
        self.differenceThreshold = 65

    def algorithm(self, img):
        intensity = np.mean(img, axis=2)    # Find intensity

        red = img[:,:,2]
        green = img[:,:,1]
        blue = img[:,:,0]

        #dt = np.where(intensity > self.intensityThreshold, self.differenceThreshold / 3, self.differenceThreshold)

        boolean = np.abs(red - green) > self.differenceThreshold
        boolean = boolean | np.abs(red - blue) > self.differenceThreshold
        boolean = boolean | np.abs(green - blue) > self.differenceThreshold

        perfusion = intensity * boolean

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

    def image(self, filename):
        self.img = cv2.imread(filename)
        return self.algorithm(self.img)

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
    perfusions = obj.video(0)
    plt.plot(perfusions)
    plt.show()