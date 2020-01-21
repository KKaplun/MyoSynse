N = 10^7;
[b,a] = butter(3,[0.1 0.13],'bandpass');

x1 = randn(1,N)+sqrt(-1)*randn(1,N);
x2 = randn(1,N)+sqrt(-1)*randn(1,N);

A = randn(2,2)+sqrt(-1)*randn(2,2);

z = A*filter(b,a,[x1;x2]')';

z1 = z(1,:);
z2 = z(2,:);

S12 = mean(z1.*conj(z2));
S11 = mean(z1.*conj(z1));
S22 = mean(z2.*conj(z2));

coh = S12/sqrt(S11*S22);
imcoh = imag(coh);

laggedcoh = imcoh/sqrt(1-real(coh)^2);

wPLI = mean(imag(z1.*conj(z2)))/mean(abs(imag(z1.*conj(z2))))
wPLI_ = 2*laggedcoh/(1+laggedcoh^2)

PLI = mean(sign(imag(z1.*conj(z2))));
