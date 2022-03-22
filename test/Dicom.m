%% Read in the header information
% hdr = dicominfo('../dicom/M2OIP8PA');
% [X, cmap, alpha, overlays] = dicomread('../dicom/M2OIP8PA');
%% Cebula's code for displaying a dicom image
info = dicominfo('../dicom/M2OIP8PA');
Y = dicomread(info);
% img1 = (Y(:,:,:,1));
% img2 = (Y(:,:,:,2));
% img3 = (Y(:,:,:,3));
% img4 = (Y(:,:,:,4));
% img5 = (Y(:,:,:,5));
% img6 = (Y(:,:,:,6));
% img7 = (Y(:,:,:,7));
% img8 = (Y(:,:,:,8));
for i = 1:8
img = (Y(:,:,:,i));
test(img,78);
end
% multi = cat(3,img1,img2,img3,img4,img5,img6,img7,img8);
% figure(1);
% imshow(Y(:,:,:,1),[0,255])
% montage({img1, img2, img3, img4, img5, img6, img7, img8})
% figure(2)
% montage(Y)
% figure(3)
% imshow(img1)
%% How I was able to display an image
% image = '../dicom/M2OIP8PA';
% figure(1)
% imshow(image,'DisplayRange',[])
%% implementing our algorythm
