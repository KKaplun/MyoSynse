function MotionFcn_patient_cortical(FigH, EventData)
%CORTICAL CONTROLLER
get(FigH, 'CurrentPoint');

%get current position within the figure
p = get(get(FigH, 'CurrentAxes'), 'CurrentPoint');

% get the bitmap matrix
I = FigH.Children(1).Children(1).CData;

%get FES device handle
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%FES = FigH.UserData.FES;%uncomment fro peripheral stim!!
ser = FigH.UserData.FES; %cortical!
%pass = FigH.UserData.pass; %cortical!
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% check if in bounds
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(size(I,1)>= fix(p(1,2)) & size(I,2)>= fix(p(1,1))...
       & fix(p(1,1))>0 &   fix(p(1,2))>0 ) %uncomment for peripheral
%if(size(I,1)>= fix(p(1,2)) & size(I,2)>= fix(p(1,1))...
%       & fix(p(1,1))>0 &   fix(p(1,2))>0 & pass ) %CORTICAL!
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
    % If within reasonamble lims save current point in the array
    if(FigH.UserData.CallsPerTrial<size(FigH.UserData.Coordinates,1))
        FigH.UserData.CallsPerTrial = FigH.UserData.CallsPerTrial+1;
       FigH.UserData.Coordinates(FigH.UserData.CallsPerTrial,:) = p(1,1:2);
    %disp(FigH.UserData.Coordinates)
    FigH.UserData.Ctime(FigH.UserData.CallsPerTrial,:)=cputime;
    end;
    
    %check if above white line
   if(FigH.Children(1).Children(1).CData( fix(p(1,2)),fix(p(1,1)))>1)
        %sound(sin(0.5*[0:200]),2000);
        if(FigH.UserData.LastStimTime>0)
            dt = etime(clock, FigH.UserData.LastStimTime);
            bMayStim = dt > FigH.UserData.RefractoryPeriod;
        else
            bMayStim = true;
        end;  
        if(FigH.UserData.GreenLight==1 & bMayStim)
           % sound(sin(1.5*[0:200]),2000);
            FigH.UserData.Stims = FigH.UserData.Stims +1;
            %FES.setFreqGlobal(1)
            %FES.setAmpPwidthSingle(1,11,30)
            %pause(0.001)
            %FES.setAmpPwidthSingle(1,0,30)
            %FES.execPulseTrainGlobal() %uncomment for peripheral!!
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %pass = false; %CORTICAL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            fwrite(ser, "8");
            %ser.DataTerminalReady = "on"; %cortical
            %pause(0.045);%cortical
            %ser.DataTerminalReady = "off"; %cortical
            %pass = true; %CORTICAL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %clock
            disp('stim');
            FigH.UserData.LastStimTime = clock;
        else
            %disp('no stim');
        end
        
   end;
end;
   
    

