---
layout: post
author: Joint work with Sean Wilkinson, Tyler Skluzacek, Rafael Ferriera da Silva (NCCS and OLCF, ORNL)
title: Parsl at OLCF
---

In this blog post, we discuss three developments surrounding Parsl at OLCF. 

First, the setup, management, and support of the Parsl software module on the Summit supercomputer. Second,
an ongoing project where we are using Parsl to bridge the gap between Quantum Computing and HPC. Third,
another ongoing project where we are developing a distributed task orchestration system and are in the process
of designing a Parsl plugin.

In January 2022, we analyzed the usage data on Summit login nodes that we have been collecting hourly since
January 1, 2020. While looking at the workflow systems usage in this data, we found that Parsl is one of the
top five workflow systems used on Summit.

<img src="/images/blog/2022-09-30/Picture1.png" width="75%" style="border:0px solid black;">
{: style="text-align: center;"}

More information about our analysis and the data itself may be found in our
[ICCS'22 paper](https://www.ornl.gov/publication/unveiling-user-behavior-summit-login-nodes-user) and the
[associated published data](https://www.osti.gov/biblio/1866372).

After looking into the results of this analysis, we approached the core OLCF admin team and requested them
to let us make Parsl and other workflow systems available to all Summit users as modules. The request was approved.

OLCF admins created `/sw/summit/workflows` and let us install Parsl there. Parsl is installed as a conda
package that is based on the pre-installed Anaconda module on Summit. A module definition was written and
the module was set up for Parsl.

One question we would like to ask the community is: Is this the right approach to make Parsl available to
the users of a cluster? Are there any best practices surrounding this topic that we should be aware of to
make using Parsl more effective? Please reach out to us at [km0@ornl.gov](mailto:km0@ornl.gov).

Alongside the installation and setup, we put together [documentation](https://docs.olcf.ornl.gov/software/workflows/parsl.html)
and gave a tutorial / training talk about using workflows at OLCF resources. The talk video and slides are
[available](https://vimeo.com/730109850).

In another development, earlier in 2022, we applied for and were awarded a small allocation on the ORNL
Quantum Computing User Program (QCUP). The objective of this project is to combine the classical HPC and
Quantum Computing using the workflows paradigm as a bridge.

One idea we explored is to make HPC generate input data and send this data along with quantum algorithms,
implemented as python-qiskit programs, to the remote quantum systems, run them there and obtain the
results back -- with all the steps coordinated with Parsl. We have some early success on this work that was
performed jointly with summer intern student Samuel Bieberich.

<img src="/images/blog/2022-09-30/Picture2.png" width="75%" style="border:0px solid black;">
{: style="text-align: center;"}

The [linked Github repo](https://github.com/Sam-Bieberich/HPC-QC-Workflows) has more info and code.

Last but not least is ongoing work where we are developing a distributed task orchestration system
that can seamlessly orchestrate science campaigns, initially across the OLCF systems and ultimately
across the DOE complex. We call it Zambeze. 

For Zambeze, we plan to reuse existing solutions where possible as a plugin-based architecture and
are currently developing a Parsl plugin for handling user-submitted workflows.

<img src="/images/blog/2022-09-30/Picture3.png" width="75%" style="border:0px solid black;">
{: style="text-align: center;"}

Acknowledgements: This work is supported by UT-Battelle, LLC, under contract DE-AC05-00OR22725 with the 
US Department of Energy (DOE) and the Exascale Computing Project (17-SC-20-SC), a collaborative effort
of the U.S. DOE Office of Science and the NNSA.

