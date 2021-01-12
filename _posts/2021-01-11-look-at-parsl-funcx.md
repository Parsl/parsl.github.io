---
layout: post
author: Dennis Gannon, School of Informatics, Computing and Engineering, Indiana University 
title: A Look at Parsl and Funcx&#58; Two Excellent Parallel Scripting Tools for Clouds and Supercomputers
---


In 2019, Yadu N Babuji, Anna  Woodard, Zhuozhao  Li,  Daniel S. Katz, Ben  Clifford, Rohan  Kumar, Lukasz Lacinski, Ryan Chard,
Justin Michael Joseph Wozniak, Michael  Wilde and Kyle  Chard published a paper in HPDC ’19 entitled
[Parsl: Pervasive Parallel Programming in Python](https://doi.org/10.1145/3307681.3325400).
I have been looking forward to finding the time to dig into it and give it a try.  The time did arrive and, as I started to dig,
I discovered some of this same group, along with Tyler Skluzacek, Anna Woodard, Ben Blaiszik and Ian Foster published
[funcX: A Federated Function Serving Fabric for Science](https://doi.org/10.1145/3369583.3392683) in HPDC ’20. 
In the following paragraphs we look at both and show examples of FuncX running on Kubernetes on Azure and on a
tiny Nvidia Jetson Nano.

## An Overview of Parsl
Parsl is best thought of as a tool for constructing and managing distributed parallel scientific workflows. For example,
suppose you have to do data processing on a collection of files in a remote Kubernetes cluster at the same time manage a
large simulation that will run  in parallel on a supercomputer and finally channel the results to a visualization system.
As sketched in the diagram in Figure 1, you want the main thread of the workflow to be managed from a python Jupyter notebook
session.  Parsl can do this.


<img src="/images/blog/2021-01-11/Picture1.png" width="70%" style="border:0px solid black;">
![](/images/blog/2021-01-11/Picture1.png)

Figure 1.  Hypothetical parallel distributed workflow involving remote resources managed from a Jupyter session on a laptop.
{: style="text-align: center;"}

The list of actual examples of scientific applications studied using Parsl is impressive and it is documented in their 
[case studies](http://parsl-project.org/case_studies.html) page.   They include examples from chemistry, physics, cosmology,
biology and materials science.  

Programming Parsl is based on the concept of futures.   This is an old idea in which function invocations returns immediately
with an object that represents the “future value” that the function will compute.  The calling thread can go about other work
while the function computation takes place in another thread of execution.   The calling thread can later wait for the function
to complete and retrieve the result.  To illustrate this here is an example of a function that computes Pi.   

<img src="/images/blog/2021-01-11/Picture2.png" width="70%" style="border:0px solid black;">

The decoration @python_app indicates that this function will return a future.    We can check to see if the computation is
complete by calling done() on the future object.   When done() returns true we can get the result value with the result() function.
 
<img src="/images/blog/2021-01-11/Picture3.png" width="50%" style="border:0px solid black;">

Parsl will allow functions returning futures to be composed into graphs that can be scheduled and executed in “dataflow” style.
For example if we have to additional functions F(x,y) and G(a,b) that return futures then the graph in Figure 2


