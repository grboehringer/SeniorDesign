
function [pv, perfusion, dt, intensity] = test(filename, differenceThreshold, intensityThreshold)
    I = imread(filename);

    red = I(:,:,1);
    green = I(:,:,2);
    blue = I(:,:,3);

    intensity = mean(I, 3);

    dt = ones(size(red)) * differenceThreshold;
    dt(intensity > intensityThreshold) = differenceThreshold / 3; 

    boolean = abs(red - green) > dt;
    boolean = boolean | abs(red - blue) > dt;
    boolean = boolean | abs(blue - green) > dt;

    perfusion = intensity .* boolean;

    pv = mean(perfusion, 'all');

    figure(1)
    imshow(I)
    title('Original Image');
    figure(2)
    multi = cat(2,uint8(dt), uint8(perfusion));
    montage(multi);
    title(['Processed Image - Difference Threshold: ',num2str(differenceThreshold),' Intensity Threshold: ',num2str(intensityThreshold)]);
end


