B=2e6;

F_s = 10*B;
dur = 40e-6;
f_limit=B/2;
f_c = 0;
f_0 = f_limit;

t = 0:(1/F_s):dur;
m = (2*f_limit)/(dur);

waveform = zeros(size(t));

for idx = 1:length(t)
    waveform(idx) = exp( (1i * 2 * pi) * ( ((f_0 - f_c) * t(idx)) - (0.5 * m * t(idx)^2) ) );
end

% Plotting the waveform
figure;
subplot(3,1,1);
plot(t, real(waveform));
title('Waveform');
xlabel('Time (s)');
ylabel('Amplitude');

% Finding the FFT of the waveform
N = length(t);
frequencies = (-F_s/2):(F_s/N):(F_s/2 - F_s/N);
fft_waveform = fftshift(fft(waveform));

% Plotting the magnitude spectrum
subplot(3,1,2);
plot(frequencies, abs(fft_waveform));
title('FFT of Waveform');
xlabel('Frequency (Hz)');
ylabel('Magnitude');

% Finding the Power Spectral Density (PSD) using pspectrum
subplot(3,1,3);
pspectrum(waveform, F_s, 'spectrogram', 'FrequencyLimits', [-B, B],'Reassign',true);
title('Power Spectral Density (PSD) of Linear Frequency Modulated (LFM) Signal');

%writing file GNURadio
fileID = fopen('DownChirp.txt', 'w');
fprintf(fileID, 'complex(%.6f,%.6f), ', real(waveform), imag(waveform));
fclose(fileID);

%writing file CPP
fileID = fopen('DownChirpCPP.txt', 'w');
fprintf(fileID, 'gr_complex(%.6ff,%.6ff), ', real(waveform), imag(waveform));
fclose(fileID);