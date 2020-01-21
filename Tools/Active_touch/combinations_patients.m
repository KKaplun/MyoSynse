%create 2 sets of random combinations for patients
load('C:\Users\bulga\Desktop\CBI\ActiveTouchM-master\Comb_patients_red') %combinations
random_Comb_patients_i=Comb_patients_red(randperm(size(Comb_patients_red,1)),:); 
pt=reshape(1:60,30,2);
for i = 1:2
    random_Comb_patients{i}=random_Comb_patients_i(pt(:,i),:);
end
save('random_Comb_patients.mat','random_Comb_patients')
%% just permutate 30 trials for Turashev 11.12.19
% Comb_half=Comb(1:90,:)
% inx=Comb_half(:,1)<7 & Comb_half(:,2)<7
% Comb_patients_red = zeros(30,2)
% Comb_patients_red(:,:) = Comb_half(inx,:)
% save('Comb_patients_red.mat','Comb_patients_red')



i = Comb_patients_red(randperm(size(Comb_patients_red,1)),:);
pt = 1:30
random_Comb_patients = cell(1,6)
random_Comb_patients{1}=i
save('random_Comb_patients.mat','random_Comb_patients'); 
