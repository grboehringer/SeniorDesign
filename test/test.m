I = imread('../test.jpg');

red = I(:,:,1);
green = I(:,:,2);
blue = I(:,:,3);

differenceThreshold = 80;
intensityThreshold = 80;

intensity = mean(I, 3);

dt = ones(size(red)) * differenceThreshold;
dt(intensity > intensityThreshold) = differenceThreshold / 3; 

boolean = abs(red - green) > dt;
boolean = boolean | abs(red - blue) > dt;
boolean = boolean | abs(blue - green) > dt;

perfusion = intensity .* boolean;

pv = mean(perfusion, 'all')

figure(1)
imshow(uint8(dt))
figure(2)
imshow(uint8(perfusion))
