%Create textures
k = [4:3:35];
for i = 1:10;
    template=zeros(345);
    template(1:k(i):end,:) = 1;%rows
    template(2:k(i):end,:) = 1;%rows
    %template(:,1:k(i):end) = 1;%columns
    %template(:,2:k(i):end) = 1;%columns
    txtrs{i}=template;
end
save('txtrs.mat','txtrs')


kp=[10    13    16    19    22    25];
for i = 1:6;
    template=zeros(345);
    template(1:kp(i):end,:) = 1;%rows
    template(2:kp(i):end,:) = 1;%rows
    %template(:,1:k(i):end) = 1;%columns
    %template(:,2:k(i):end) = 1;%columns
    txtrs_patient{i}=template;
end
save('txtrs_patient.mat','txtrs_patient')

