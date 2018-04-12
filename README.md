
Introduction
====================

| |CN|ENG|   |
|---|----|-----|-----|
|1|`复合材料层合板计算`|[Composite Material Calculation with CLT][CLT]| [Introduction](#composite-material-calculation-with-clt)|


`read the program introduction for more details ` [Here](/doc/pro_introduction.pdf)  
[Running requirements](#running-requirements) | [Installation](#installation) | [License](#license) 
#### Project code for Mechanics of Composite Structure IN NPU,PARTLY FINISH.
#### ALL RIGHT RESERVED
********************************
## Composite Material Calculation with CLT
* The main package is a Python composite materials calculation package.
The laminate stresses, strain and failure Criterion based on the Classical Lamination Theory ([CLT](https://en.wikipedia.org/wiki/Composite_laminates)).  

	- You can define the lamina's fibre and matrix's parameters like the Elastic moduli
	![](http://latex.codecogs.com/gif.latex?E_{1},E_{2}),
	 Shear moduli ![](http://latex.codecogs.com/gif.latex?G) and strength, then  in the next step, you can define lamina's layer angle and thickness directly or combined by fibre/matrix.
		
	- After define the lamina you can get the matrix such as ![A,B,D,Q](http://latex.codecogs.com/gif.latex?A,B,D,Q,\\bar{Q}) and so on by use the ***Laminate class*** or you can define the laminate directly.

	- Use the ***Load class*** and load the force and moment to the laminate to calculate the stress ![](http://latex.codecogs.com/gif.latex?\\sigma) and stain ![](http://latex.codecogs.com/gif.latex?\\epsilon) of each lamina.

	- Use the ***Failure_Cirterion class*** and you can choose different theories to check witch lamina failure or not.

* The *laminate_plugin.py* can plot the stress and strain distribution in the laminate in the COS(xy or 12), print the results in _Excel_ formate and save it in _Excel_.

	![COS in laminate](https://github.com/Eacaen/CLT-material-properties/blob/master/fig/laminate_COS.png 'COS in laminate')
	![COS in laminate](https://github.com/Eacaen/CLT-material-properties/blob/master/fig/lammmm.png 'COS in laminate')
	![strain distribution in laminate](https://github.com/Eacaen/CLT-material-properties/blob/master/fig/strain_in_web2.png 'COS in laminate')
	![stress distribution in laminate](https://github.com/Eacaen/CLT-material-properties/blob/master/fig/stress_in_web.png 'COS in laminate')

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
---------------------------------------------------------
[CLT]:https://github.com/Eacaen/CLT-material-properties  "CLT"
 
