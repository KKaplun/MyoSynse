fes=FES('COM1',38400,0)%Fes connected -> set to 0 
prepPulseTrainSingle(fes,1,0.5,30,1,0)
%Prepare a train of pulses for a specific channel.
            %INPUT: fes
            %INPUT: Channel number: Between 1 and 8
            %INPUT: mA: Between 0 and 125
            %INPUT: pulsewidth: Between 0 and 500
            %INPUT: Pulse number: Between 1 and 16
            %INPUT: Delay: 0 and 32768 [ms]
for i=1:6
execPulseTrainGlobal(fes)
pause(0.5)%executes prepared train (or single pulse)
end


