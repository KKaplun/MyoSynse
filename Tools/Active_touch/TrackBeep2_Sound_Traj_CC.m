%% Active touch main script
%CORTICAL CONTROLLER
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tmp=clock;
c_time=tmp(2:5);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
block=1; %Change block # !!
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
name=strcat('C:\Users\bulga\Desktop\CBI\ActiveTouchM-master\AT_Results\'...
    ,sprintf('EL_test_%g_b',block)...%Change the NAME 
    ,sprintf('_%g',c_time));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%set working directory. It has to contain FES.m and ActiveTouchPattern
WorkingDirectory = 'C:\Users\bulga\Desktop\CBI\ActiveTouchM-master';
%set basic parameters
RefractoryPeriod =0.0001; % refractory period, seconds (we don't need it here)  
NumberOfTrials = 5; %$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%%%
TrialDuration = 2000; % seconds (we don't need it here)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
HideImage = 0; %show or hide image  0 = SHOWS TARGET GRID 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
MaxMotionFcnCallsPerTrial = 5000;
%%%%%%%%%%%%CORTICAL STUFF%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Open Cortical Stiimulator COM port
ser = serial("COM7");
fopen(ser);
% ser.DataTerminalReady = "off";
%%%%%%%%%%%%%%%%CORTICAL STUFF END%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% load ActiveTouchPatternImages and files
cd(WorkingDirectory); 
tmp = imread(strcat(WorkingDirectory ,'/grid2.bmp')); %grid
grid=~tmp;
load(strcat(WorkingDirectory,'/txtrs.mat')); % textures
load(strcat(WorkingDirectory,'/random_Comb.mat')) %pre-created random combinations for subject
for k = 1:length(txtrs)
    tmp =zeros(345,345);
    atp(:,:,k) = ~tmp;
end
for i = 1:size(atp,3)
    atp(:,:,i)=txtrs{i};
end
tmp = imread(strcat(WorkingDirectory ,'/correct.bmp')); %feedback
correct = ~tmp;    
tmp = imread(strcat(WorkingDirectory ,'/wrong.bmp')); %feedback
wrong = ~tmp;    
tmp = imread(strcat(WorkingDirectory ,'/exclamation_mark.bmp'));
exclamation_mark = ~tmp;    

%intialize timer
timer = [];

%create UserData structure as a vehicle to transfer information into the
%MotionFcn callback of the figure called every time the cursor movescomment
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%UserData.FES = fes; % uncomment for peripheral!!!!!!!!
UserData.FES = ser;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
UserData.Timer = timer;
UserData.GreenLight = 0; % if this one is 1 then stimulation will happen otherwise it will be idle.
UserData.LastStimTime = -1; %clock;
UserData.RefractoryPeriod = RefractoryPeriod;
UserData.Stims = 0; %count per-trial stimulations
%UserData.pass = true;
close all
% load the first image and create the figure
FigTaskH = figure;
FigTaskH.UserData = UserData;
FigTaskH_position=[0.0060 0.5329 0.9726 0.4094];
imagesc(exclamation_mark,'Parent', FigTaskH, 'Parent', axes('Parent',FigTaskH));
set(FigTaskH,'units','normalized','Outerposition',FigTaskH_position ,...
    'menubar','none')
set(FigTaskH.Children,'Visible','off');
set(get(FigTaskH.Children,'Title'),'Visible','on');
set(FigTaskH,'color','k')
% create Answers pan
FigAnswerH = figure;
ar = imread(strcat(WorkingDirectory ,'/arrow.bmp'));
ar2 = imread(strcat(WorkingDirectory ,'/arrow.bmp'));
im = [ar(:,1:2:end)*2 ar2(:,1:2:344)*2];
im(:,173)=0;
h = imagesc(im, 'Parent', axes('Parent',FigAnswerH));
cmap = get(FigAnswerH, 'Colormap');
cmap(1,:) = 0;
FigAnswerH_position=[0.0077 0.0906 0.9644 0.4229];
set(FigAnswerH,'Colormap',cmap,'units','normalized','Outerposition',...
    FigAnswerH_position,'menubar','none');
set(FigAnswerH.Children,'Visible','off');
set(get(FigAnswerH.Children,'Title'),'Visible','on');
%set the callback function 
BigZ = zeros(MaxMotionFcnCallsPerTrial,2);
FigTaskH.UserData.Coordinates = BigZ;
FigTaskH.UserData.CallsPerTrial = 0;
set(FigTaskH,'WindowButtonMotionFcn', @MotionFcn_Sound_Traj_CC);
disp('Resize windows, make patient comfortable and press any button')
pause;
cmap = FigTaskH.Colormap;
Response = zeros(NumberOfTrials,3);
R_time = zeros(NumberOfTrials,1);

%generate sound start of each trial
amp=10; 
fs=20500;  % sampling frequency
duration=0.05;
freq=900;
values=0:1/fs:duration;
beep=amp*sin(2*pi* freq*values);
%main loop
for tr = 1:NumberOfTrials
    % reset per trial trajecotry record
    FigTaskH.UserData.Coordinates = BigZ;
    FigTaskH.UserData.CallsPerTrial = 0; 
    FigTaskH.UserData.Stims = 0;
    FigTaskH.Children(1).Children(1).CData = exclamation_mark;
    pause(0.5)
    %generate sound before each trial
    sound(beep);
    %randomize figs
    FigTaskH.UserData.GreenLight = 0;
    FigTaskH.Children(1).Children(1).CData = ...
        grid + [atp(:,1:2:end,random_Comb{block}(tr,1))...
        *2 atp(:,1:2:344,random_Comb{block}(tr,2))*2];
    if(HideImage==true)
       %FigTaskH.Colormap = zeros(size(FigTaskH.Colormap));
        cmap_hide = [0 0 0; 1 1 1;  0 0 0; 1 1 1]; %for lines
       %cmap_hide = [0 0 0; 1 1 1;  0 0 0]; %for squares
        FigTaskH.Colormap = cmap_hide;
    end
    FigTaskH.UserData.GreenLight = 1;
    a=tic;  
    set(0, 'currentfigure', FigAnswerH)
    %set(FigAnswerH, 'WindoButtonDownFcn',  @clicker
          gg = waitforbuttonpress;
          if gg == 0 ;
             ss=toc(a);
             ll =  get(FigAnswerH, 'CurrentPoint');
             x = ll(1,1);
             k_subj =  ll(1)>0.5;
             y = ll(1,2);
          else 
             k_subj = 0;
          end
          Response(tr,:) = [random_Comb{block}(tr,:), k_subj];
          tr
          Response(tr,:)
          R_time(tr,:) = ss;  
          FigTaskH.Colormap = cmap;
          if Response(tr,1)> Response(tr,2) & Response(tr,3)==1 ...
                  | Response(tr,1)< Response(tr,2) & Response(tr,3)==0
              FigTaskH.Children(1).Children(1).CData = correct;
              disp('correct')
          else
              FigTaskH.Children(1).Children(1).CData = wrong;
              disp('incorrect')
          end
          pause(1)
         %save per trial coordinates 
        Coordinates{tr} = FigTaskH.UserData.Coordinates...
            (1:FigTaskH.UserData.CallsPerTrial,:);
        Times{tr}=FigTaskH.UserData.Ctime(1:FigTaskH.UserData.CallsPerTrial,:);
        Stims{tr}=FigTaskH.UserData.Stims;
end
% dlmwrite('results_NS_grid2_10.txt', Response)
% dlmwrite('Rtime_NS_grid2_10.txt', R_time)


% % save trajecories to file
% for tr = 1:length(Coordinates)
%     dlmwrite(['Traj_NS_grid2_tr_10', num2str(tr), '.txt'],Coordinates{tr});
% end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fclose(ser); %CORTICAL!!!!!!!!!!!!!!
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
set(FigTaskH,'WindowButtonMotionFcn', '');
close all
save(name)
clearvars -except fes 


