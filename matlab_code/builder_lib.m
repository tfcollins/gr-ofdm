
function builder_lib()


cfg = coder.config('dll');
cfg.TargetLang='C++';
% cfg.GenCodeOnly = true;
result = codegen('-config','cfg','EADF_Estimate','-o','libEADF_Estimate.so');

if result.summary.passed
    system('cd ../include;rm EADF_Estimate.h  EADF_Estimate_types.h  rt_defines.h  rt_nonfinite.h  rtwtypes.h;cd ../matlab_code;');

    system(['cp ',pwd,'/codegen/dll/EADF_Estimate/libEADF_Estimate.so ../lib/']);
    
    system(['cp ',pwd,'/codegen/dll/EADF_Estimate/EADF_Estimate.h ../include/']);
    system(['cp ',pwd,'/codegen/dll/EADF_Estimate/EADF_Estimate_types.h ../include/']);
    
    system(['cp ',pwd,'/codegen/dll/EADF_Estimate/rtwtypes.h ../include/']);
    system(['cp ',pwd,'/codegen/dll/EADF_Estimate/rt_defines.h ../include/']);
    system(['cp ',pwd,'/codegen/dll/EADF_Estimate/rt_nonfinite.h ../include/']);
    
    %system(['rm -rf ',pwd,'/codegen']);
    
    disp('Build Completed Successfully');
else
    disp('Build failed');
end

end