files = ls('processed_*');
files = strsplit(files);

l = 'processed_run_p';

data = struct;

for f = 1:length(files)
    
    if strcmp(files{f},'')
        continue
    end
    
    fn = files{f}(length(l):end-4);
    if strcmp(fn(1),'p')
        offset = str2num(fn(2:end));
    else
        offset = -str2num(fn(2:end));        
    end
    true_doa = atan(offset/26.5);

    
    data(f).doa = importfile(files{f});
    data(f).true_doa = true_doa*180/pi;

end


%% MSE

for f = 1:length(data)
   
    angles(f) = data(f).true_doa;
    
    doa = data(f).doa;
    doa(isnan(doa)) = [];
    doa(abs(doa)>mean(abs(doa))*(10)) = [];
    data(f).doa = doa;
    
    doa_mse(f) = mean(abs(doa - data(f).true_doa));
    vars(f) = var(doa);
end

[~,I] = sort(angles);

eadfmse = doa_mse;

%% Plot
stem(angles(I)+90,eadfmse(I),'bo');
hold on;
stem(angle,doa_mse,'rs');
stem(angle,rootm_m,'g*');
errorbar(angles(I)+90,eadfmse(I),vars(I),'bo');
xlabel('Angle (Degrees)');
ylabel('Absolute Error (Degrees)');
title('EADF-FFT DoA')
grid on;

%[angle, doa_mse, rootm_m, rootm_vars,m_vars] = eval_files;
errorbar(angle,doa_mse,m_vars,'rs');
errorbar(angle,rootm_m,rootm_vars,'g*');
hold off;
legend('EADF-FFT','MuSIC','RootMuSIC');





