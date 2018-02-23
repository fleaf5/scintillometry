import sys
import numpy as np

offsetn     = int(sys.argv[1])
offsetm     = int(sys.argv[2])
n           = int(sys.argv[3])
m           = int(sys.argv[4])
meff = 2*m
result_dir="results/gate0_numblock_%s_meff_%s_offsetn_%s_offsetm_%s" %(str(n),str(meff),str(offsetn),str(offsetm)) 
result_path = "results/gate0_numblock_%s_meff_%s_offsetn_%s_offsetm_%s_uc.npy" %(str(n),str(meff),str(offsetn),str(offsetm))

##### Load electric field from deconvolution routine ####
E_tilde_res = np.load(result_path).astype(np.complex128)
E_tilde_res = np.reshape(E_tilde_res, (n,2*m))                  # Reshape the flattened result.
E_tilde_res = np.flipud(E_tilde_res)
E_tilde_res = np.concatenate((E_tilde_res[:,0][:,np.newaxis],np.fliplr(E_tilde_res[:,1:])),axis=1)

## Normalize E(f,t) in the original Doppler frequency range.
E_tilde_res_domain = np.concatenate( (E_tilde_res[:,:E_tilde_res.shape[1]/4], E_tilde_res[:,-E_tilde_res.shape[1]/4:]),axis=1)
E_tilde_res_domain = np.concatenate( (E_tilde_res_domain[:,0][:,np.newaxis], np.fliplr(E_tilde_res_domain[:,1:])) ,axis=1)
Eft_res_domain = np.fft.ifft2(E_tilde_res_domain)
Eft_res_domain = Eft_res_domain/np.sqrt(np.mean(np.absolute(Eft_res_domain)**2))
E_tilde_res_domain = np.fft.fft2(Eft_res_domain)

# E_tilde_res_domain is E(tau, f_D). It has the same size as the input spectrum. It is normalized such that <|E(f,t)|^2>=1. 
np.save(result_dir+"/E_tilde.npy",E_tilde_res_domain)
