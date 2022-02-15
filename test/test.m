I = imread('../test.jpg');

red = I(:,:,1);
green = I(:,:,2);
blue = I(:,:,3);

differenceThreshold = 20;
intensityThreshold = 8;

intensity = mean(I, 3);

dt = ones(size(red)) * differenceThreshold;
dt(intensity > intensityThreshold) = differenceThreshold / 3; 

boolean = abs(red - green) > dt;
boolean = boolean | abs(red - blue) > dt;
boolean = boolean | abs(blue - green) > dt;

perfusion = intensity .* boolean;

imshow(uint8(perfusion))
