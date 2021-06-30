---
layout: post
author: James Corbett (LLNL) and Dong H. Ahn (LLNL)
title: FluxExecutor efficiently integrates Parsl and Flux
---


To provide [ExaWorks](http://parsl-project.org/2021/04/22/ExaWorks.html)'s Software Development Kit (SDK)
with Level-1 interoperability between Parsl and Flux, the ECP ExaWorks team recently integrated Parsl
with Flux through a new Executor class, the
[FluxExecutor](https://parsl.readthedocs.io/en/latest/stubs/parsl.executors.FluxExecutor.html#parsl.executors.FluxExecutor),
for use wherever the Flux resource manager is installed. Groundwork for Parsl's FluxExecutor was laid in
Flux itself with the addition of a lower-level executor for use by all workflow systems.
 
To use the new FluxExecutor, the only prerequisite is that there be an installation of Flux available,
found either in the user's PATH environment variable or in another manually-specified location. See
instructions [here](https://flux-framework.readthedocs.io/en/latest/quickstart.html#building-the-code)
to build Flux on your system.
 
Parsl's FluxExecutor specializes in applications that require a nontrivial resource set (like MPI or
other compute-intensive applications), and collections of applications with highly variable resource
requirements. Flux's sophisticated scheduling will handle those applications logically and efficiently.
 
To allocate resources to a Parsl app, pass a dictionary with one or more of the following keys
to the app as the `parsl_resource_specification` key:
 
* num_tasks: the number of tasks (or processes, if you prefer) to launch, default 1. This option corresponds directly with the number of MPI ranks
* cores_per_task: cores per task/process, default 1
* gpus_per_task: gpus per task/process, default 0
* num_nodes: if > 0, evenly distribute the allocated cores/gpus across N nodes. Does not give the job exclusive access to those nodes; this option only affects distribution.
 
For instance, to allocate 10 MPI ranks to the app `my_app` with 1 GPU per rank,
`fut = my_app(parsl_resource_specification={'tasks': 10, 'gpus_per_task': 1})`.
 
Examples of using Parsl's new FluxExecutor can be found 
[here](https://parsl.readthedocs.io/en/latest/userguide/configuring.html#toss3-llnl).
 
[Flux](https://flux-framework.readthedocs.io/en/latest/) is a next-generation workload manager for
HPC centers. It combines the fully hierarchical resource management with graph-based scheduling to
improve the performance, portability, flexibility and manageability of scheduling and execution of
complex workflows on HPC systems both at the system and user level. It is the plan-of-the record
workload manager for LLNL's
[El Capitan](https://www.llnl.gov/news/llnl-and-hpe-partner-amd-el-capitan-projected-worlds-fastest-supercomputer)
supercomputer when it is deployed in 2023.
