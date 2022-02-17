%Perfusion code translated from Python into MATLAB code
%% Image reading
image = imread('PowerDopplerTest.jpg');
figure(1)
(imshow(image));
figure(2)
gImage = rgb2gray(image);
imshow(gImage);
%% Edge Detection
figure(3)
BW = edge(gImage,'Canny');
imshow(BW);

%% Red detection
figure(4)
% Make mask using R channel
BW1 = imbinarize(image(:,:,1));
% Remove all colors exept red
I2 = image;
I2(repmat(~BW1,1,1,3)) = 255;
% Show the result
imshowpair(image,I2,'montage')
