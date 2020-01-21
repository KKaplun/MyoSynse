% combinations
load('D:\work\HSE\инвазивные интерфейсы\ActiveTouchM-master') %combinations
%create 6 sets of random combinations
random_Comb_i=Comb(randperm(size(Comb,1)),:); 
vt=reshape(1:180,30,6);
for i = 1:6
    random_Comb{i}=random_Comb_i(vt(:,i),:);
end
save('random_Comb.mat','random_Comb')