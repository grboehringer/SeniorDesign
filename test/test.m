
function [pv, perfusion] = test(I, differenceThreshold)
%     I = imread(filename);

    red = I(:,:,1);
    green = I(:,:,2);
    blue = I(:,:,3);

    intensity = mean(I, 3);

    dt = ones(size(red)) * differenceThreshold;
%     dt(intensity > intensityThreshold) = differenceThreshold / 3; 

    boolean = abs(red - green) > dt;
    boolean = boolean | abs(red - blue) > dt;
    boolean = boolean | abs(blue - green) > dt;

    perfusion = intensity .* boolean;

    pv = mean(perfusion, 'all');

    figure
    multi = ({uint8(I), uint8(perfusion)});
    montage(multi);
    title(['Processed Image - Difference Threshold: ',num2str(differenceThreshold), ' Perfusion Value: ' ,num2str(pv)]);
end


