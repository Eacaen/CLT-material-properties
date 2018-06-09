
Introduction
====================

| |CN|ENG|   |
|---|----|-----|-----|
|1|`复合材料层合板计算`|[Composite Material Calculation with CLT][CLT]| [Introduction](#composite-material-calculation-with-clt)|`read the program introduction for more details ` [Here](/doc/pro_introduction.pdf)  

[Running requirements](#running-requirements) | [Installation](#installation) | [License](#license) 

<img align="right"  width="400" height="300"  src="fig/Composite_3d.png" data-canonical-src="fig/Composite_3d.png" />

********************************
##### Project code for Mechanics of Composite Structure IN NPU,PARTLY FINISH.
##### ALL RIGHT RESERVED

********************************
#### see the blade design used the composite materials
__composite-blade-design__ 

[Blog Introduction](https://eacaen.github.io/python/2017/10/17/composite-blade-design.html)

[Github source](https://github.com/Eacaen/composite-blade-design)

********************************

## Project goals:
- Use the fibre and matrix or given data to define the composite lamina and then layup the laminate.
- Use the *Classical Lamination Theory* to  calculate the stress&strain distribution in each layer.
- Choose suitable *Failure Criteria* to check the strength of laminate at given load.
- Show accurate calculate information of results, display figures of  stress&strain distribution; show the failure steps of chosen layer.

## Data flow of the Project
<img src="fig/dataflow.png" data-canonical-src="fig/dataflow.png" />

## Task achieved:
- [x] Use CLT to calculate  stresses and strains distribution in lamina & laminate in local and global coordinate systems
- [x] Elastic modulus  calculate  for  lamina with [mixture of law , VDI2014 , Chamis model .....]
- [x] Global elastic modulus  calculate  for  __laminate__ 
- [x] Failure criteria [Tsai-Wu, Tsai-Hill, Hoffman, Max stress&strain ...]
- [x] Display the figures and report accurate results
- [x] Puck failure criteria
- [x] Can choose failure criteria in step analysis by pass the name of the *failure criteria*
- [x] Add progress bar in step analysis, more cleaner 
- [ ] Thermal & moisture effects on CLT calculations
- [ ] Database for Fibre and Matrix, laminate materials 
- [ ] ...

## Brief intro
### Coordinate System
 * xy is the Global System for __laminate__
 * 12 is the Local system for __lamina__


<img src="fig/laminate_COS.png" data-canonical-src="fig/laminate_COS.png" /><img  src="fig/lammmm.png" data-canonical-src="png/lammmm.png" />




### Composite Material Calculation with CLT
* The main package is a Python composite materials calculation package.
The calculation of laminate stress, strain and failure Criterion based on the Classical Lamination Theory ([CLT](https://en.wikipedia.org/wiki/Composite_laminates)).  

	- You can define the lamina's fibre and matrix's parameters like the Elastic moduli
	![](http://latex.codecogs.com/gif.latex?E_{1},E_{2}),
	 Shear moduli ![](http://latex.codecogs.com/gif.latex?G) and strength, then  in the next step, you can define lamina's layer angle and thickness directly or combined by fibre/matrix.
		
	- Use the ***Laminate class*** to get the matrix such as ![A,B,D,Q](http://latex.codecogs.com/gif.latex?A,B,D,Q,\\bar{Q}).

	- Use the ***Load class*** and load force and moment to the laminate to calculate the stress ![](http://latex.codecogs.com/gif.latex?\\sigma) and stain ![](http://latex.codecogs.com/gif.latex?\\epsilon) of each lamina.

	- Use the ***Failure_Cirterion class*** and you can choose different theories to check witch lamina failure or not.

* The *laminate_Tools.py* can help to plot the stress and strain distribution in the laminate in the COS(xy or 12), print the results in _Excel_ formate  and save it in _Excel_.


<img width="400" height="300" src="fig/strain_dis1.png" data-canonical-src="fig/strain_dis1.png" /><img width="400" height="300" src="fig/stress_dis.png" data-canonical-src="fig/stress_dis.png" />



<img  width="400" height="300"  src="fig/strain_dis.png" data-canonical-src="fig/strain_dis.png" /><img  width="400" height="300" src="fig/result.png" data-canonical-src="fig/result.png" />

## Run failure analysis
Run  failure analysis by adding load step by step , use *laminate_step_failure.py* can  plot the Load Factor vs  the strain development of the chosen laminate, at the same time, it can mark the First Ply Failure and Last Ply Failure.

  > It may take some more time to run the process
 
 
<img  width="400" height="300" src="fig/failstep.png" data-canonical-src="fig/failstep.png" /><img  width="400" height="300" src="fig/failureStep.png" data-canonical-src="fig/failureStep.png" />


*****************************************************
### Running requirements
	Python > v2.7
	Numpy
	Scipy
	Sympy
	matplotlib

### Installation         
>Copy the source files in the local directory and add the PATH in the system or copy the files to the Python's "site-packages" folder.  
>Copy the source file in you own file and develop the new function by yourself.

### License
#### Project code for Mechanics of Composite Structure IN NPU,PARTLY FINISH.
#### ALL RIGHT RESERVE

*****************************************************

#### Debugs log

- [x] The __fibre__ and __fiber__  mixed used, can not enter *fibre failure* mode.
- [x] Run the load in a large enough scales to get the failure step curve, how to how to distinguish the lamina has failed?
- [ ] how to distinguish the lamina has failed? the matrix of fiber failure. The test example shows the fuzzy answer.

---------------------------------------------------------
[CLT]:https://github.com/Eacaen/CLT-material-properties  "CLT"
 
