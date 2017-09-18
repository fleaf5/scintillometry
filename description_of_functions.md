#Outline of code#
The following is a rough description of how the decomposition is performed. This explanation is written specifically for the 'yty2' method when padding is used (i.e. when ''pad = 1'')--the process might differ significantly for other methods.

###extract_realData2.py###
* This program takes the observed dynamic spectrum <math>I'(f, t)</math>, and converts it to ''n'' matrices of size ''2m x 2m'', which are the blocks of the matrix corresponding to the conjugate spectrum <math>\widetilde{I}(\tau, f_D)</math>. That is, it constructs the blocks <math>\bar{I}_k</math> which are described in Nilou's report.
* This program saves ''n'' blocks, which are sufficient to construct the entire conjugate spectrum matrix, given that it is block Hermitian Toeplitz.

###run_real_new.py###
This is the main driver for the decomposition. It does the following:
* Initializes MPI (defines variables ''comm'', ''size'' and ''rank''). Here, ''2n'' MPI process are initialized: 1 for each of the ''n'' blocks in the conjugate spectrum matrix saved by ''extract_realData2.py'', and 1 for each of the conjugate transposes of these ''n'' blocks.
* Interprets arguments specified on command line (''n'', ''m'' etc.).
* For each MPI process, creates an instance of the class ''ToeplitzFactorizor''. 
* The for loop at the end of the code executes a single loop for each MPI process (where ''i'' takes on the value 0). This is because we must set ''size = 2n'', which means ''n*(1 + pad)//size = 1'' when ''pad = 1''.
* For each MPI process, 1 of the ''2n'' blocks is selected using the ''addBlock'' function within ''ToeplitzFactorizor''.
* For each MPI process/block, the Toeplitz factorization is performed using the ''fact'' function within ''ToeplitzFactorizor''.
* Setting ''detailedSave'' to True will force the program to save on each iteration (slows code extremely).

###new_factorize_parallel.py###
This script defines the class ''ToeplitzFactorizor'' which has the following attributes:
* ''comm, size, rank, n, m, pad, folder, m, detailedSave, k''
* ''blocks'': an instance of the class ''Blocks'', which is defined in ''GeneratorBlocks.py''.
* ''numOfBlocks''
* ''kCheckpoint''
This script defines the following functions:
* ''addBlock'': Creates an instance of ''Block'', defined in ''GeneratorBlock.py'' for each MPI process. Initializes the arrays A1, A2, and T for the instance of ''Block''. Adds the instance of ''Block'' to the attribute ''blocks'' for the current instance of ''Blocks''.
* ''fact''
* ''__setup_gen'': Sets up generator matrix A.
* ''__set_curr_gen'', ''__temp_Comm'', ''__block_reduc'', ''__new_block_update'', ''__block_update'', ''__aggregate'', ''__seq_reduc'', ''__seq_update'', ''__house_vec''

The code executes as follows:

When each MPI process first defines an instance of ''ToeplitzFactorizor'' from ''run_real_new.py'', the ''__init__'' function does the following:
* Assigns the above attributes and defines the above functions.
* Performs a check to see whether the code has been stopped mid-execution. 
* Assigns ''kCheckpoint'' to the appropriate value (0 if the decomposition is just beginning).
* Creates a checkpoint folder if the decomposition is just beginning.
* Creates a results folder and subfolder for current run if they do not exist.
* Initialize and save the matrix which will store the final result.
* Pause all MPI processes until the rank=0 process finishes creating folders/results.
 After the MPI processes synchronize, ''run_real_new.py'' tells each MPI process to select a block using the ''addBlock'' function defined in ''new_factorize_parallel.py''.
* If resuming from a checkpoint, assign the attributes ''A1'' and ''A2'' for the current instance of ''Block'' using the data in the checkpoint folder. 
* If starting a new run: 
* For MPI processes with ''rank < n'', assign the attribute ''T'' for the current instance of ''Block'' using the data in the processedData folder.
* For MPI process with ''rank >= n'' assign the attributes ''A1'' and ''A2'' for the current instance of ''Block'' using ''m x m'' arrays of zeros.
* Assign a name to the current instance of ''Block''.
* Add the current instance of ''Block'' to the attribute ''blocks'' for the current instance of ''Blocks''. The list ''blocks'' should only contain one instance of ''Block'' in the yty2 method.
The program now performs the factorization as described in Algorithms 3, 4, 5, 8, 15 and 16 of N. Bereux, Linear Algebra and its Applications '''404''', 193 (2005). The easiest way to understand the code is to read that document. Each MPI process executes the ''fact'' function defined in ''new_factorize_parallel.py'', which initiates Algorithm 3.
* Algorithm 4: Set up generator A.
**If starting a new run, call ''__setup_gen()'': 
**The elements of the first (second) column of the generator matrix A are stored in the variables A1 (A2) of each MPI process.
**In contrast to the generator described in N. Bereux, Linear Algebra and its Applications '''404''', 193 (2005), the generator matrix A constructed here is ''n2m x 4m'', and the block in the first row, second column is nonzero.
** Delete the matrix T which was defined for each MPI process with ''rank < n''.
* If ''detailedSave = True'', save A1 for each MPI process.
* The ''rank ='' 1 process creates the generator A(k) for the kth Schur complement.

###GeneratorBlocks.py###
This script defines the class ''Blocks'' which has the following attributes:
* ''blocks'': a list which will be filled with instance(s) of the class ''Block'', which is defined in ''GeneratorBlock.py''.
* ''currPos''
The class ''Blocks'' contains the following functions:
* ''addBlock'': appends an instance of the ''Block'' class defined in ''GeneratorBlock.py'' to the ''blocks'' attribute of the current instance ''ToeplitzFactorizor''.
* ''hasRank'', ''getBlock'', ''numOfWork1'', ''__iter__'', ''next''

###GeneratorBlock.py###
This script defines the class ''Block'' which has the following attributes:
* ''work1'', ''work2'', ''T''
* ''rank'': the rank of the MPI process.
The class ''Block'' contains the following functions:
* ''setT'', ''deleteT'', ''createA'', ''createTemp'', ''createCond'', ''setTemp'', ''getTemp'', ''setTrue'', ''setFalse'', ''getCond'', ''setA1'', ''setA2'', ''setWork1'', ''setWork2'', ''setWork'', ''setName'', ''updateuc'', ''getWork'', ''getWork1'', ''getWork2'', ''getA1'', ''getA2'', ''getT''

###ToeplitzFactorizorExceptions.py###
Contains exceptions.

