---
layout: post
author: Sophie Bui
title: OSPREY Wins HPCwire Editor's Choice Award for Best HPC Response to Societal Plight
excerpt: OSPREY, an open science platform for robust epidemic analysis that leverages Globus Compute, a unified interface for securely and reliably accessing remote compute resources using a distributed network of Parsl executors to create a Function as a Service (FaaS) platform, was awarded the Editor’s Choice Award at SC24 in Atlanta, Georgia, on November 18, 2024.
---
<img src="/images/blog/2024-11-26/HPCwire-2024-RCA_Banner.png" width="100%" style="border:0px solid black;" alt="A banner graphic with HPCwire Award Logo">
{: style="text-align: center;"}

Each year, <a href="https://www.hpcwire.com/" target="_blank">HPCwire</a> presents its annual <a href="https://www.hpcwire.com/2024-hpcwire-awards%20readers-editors-choice/" target="_blank">Readers’ and Editors’ Choice Awards</a> to celebrate the most significant breakthroughs in high-performance computing (HPC) over the past 12 months. The global HPC community nominated and voted on the awards, with the winners announced and honored during the Supercomputing Conference. These recognitions within the HPC industry honor outstanding achievements and innovations and serve as a mark of excellence in the field.

OSPREY, an open science platform for robust epidemic analysis that leverages <a href="https://parsl-project.org/2024/06/26/parsl-globus-compute.html" target="_blank">Globus Compute</a>, a unified interface for securely and reliably accessing remote compute resources using a distributed network of Parsl executors to create a Function as a Service (FaaS) platform, was awarded the Editor’s Choice Award for “Best HPC Response to Societal Plight” at SC24 in Atlanta, Georgia, on November 18, 2024.

> Being awarded the HPCWire Editor’s Choice Award for our work on OSPREY is of great significance to us. Our work is very important to us, but these recognitions demonstrate that the community also recognizes the importance of our work.
> – Valerie Hayot-Sasson, a postdoctoral scholar at the University of Chicago and ANL.

<img src="/images/blog/2024-11-26/HPCwire-Award-Pic.png" width="100%" style="border:0px solid black;" alt="A photo collage of Kyle Chard and Valerie Hayot-Sasson receiving the HPCwire award from Tom Tabor.">
{: style="text-align: center;"}

OSPREY aims to enhance pandemic response by enabling epidemiological researchers and health officials to utilize HPC resources and facilitates data-driven decision-making to make better and timely public health decisions. Researchers from  Argonne National Lab (ANL)  and the University of Chicago used Globus, <a href="https://emews.org" target="_blank">EMEWS</a> (Extreme-scale Model Exploration with Swift), and the newly developed <a href="https://github.com/NSF-RESUME/aero" target="_blank">AERO</a> (Automated Event-based Research Orchestration) platform to integrate automated workflows, data curation, and epidemiological analyses to facilitate rapid collaboration and development during health crises.

> Our focus with OSPREY has been to develop broadly applicable capabilities to improve decision-making for epidemic response, tying together advanced data, modeling, computing, and automation approaches. This recognition by the HPCwire editors and thought leaders in HPC is both gratifying and helps us further disseminate our open science platform.
> – Jonathan Ozik, a principal computational scientist at ANL and senior scientist at the consortium for Advanced Science and Engineering with Public Health Science affiliation at the University of Chicago.

<a href="https://www.globus.org/news/globus-receives-multiple-honors-in-hpcwire-annual-awards" target="_blank">Read Globus’ press release for more info about this award</a>.

<hr>

## The Creation of OSPREY

COVID-19 had an unprecedented impact on scientific collaboration. The pandemic and its broad response from the scientific community forged new relationships among domain experts, mathematical modelers, and scientific computing specialists. Computationally, however, it revealed critical gaps in researchers’ ability to exploit advanced computing systems. These challenges include accessing scalable computing systems, porting models and workflows to new systems, sharing data of varying sizes, and producing results that others can reproduce and validate.

To address these challenges, a multi-institutional team from ANL, UChicago, and Inria centre at Université Côte d’Azur Sophia Antipolis, came together to draw on their experiences in supporting public health decision-makers during the COVID-19 pandemic and developed OSPREY (Open Science Platform for Robust Epidemic analYsis). OSPREY seeks to lower the barriers to and automate epidemiological model analyses, monitoring, and rapid response on HPC resources. The team published a paper about their work prototyping the open science platform in May 2023, <a href="https://ieeexplore.ieee.org/abstract/document/10196539?casa_token=JYWij7orZnMAAAAA:IWXYvrY9HAAzg4fcgNOwyRhLmFQDbZ2MF2m4iRgBj-hvrc2LMaP0ZWrBZOX_ZXcPkA0Bo0xu-wNP" target="_blank">read it here</a>.

<hr>

## Facilitating Interoperability: Using Workflow Frameworks with OSPREY

OSPREY provides users the ability to automate their analysis workflows. These analyses can be simple single analysis tasks or more complex analysis workflows. The team has used workflow frameworks such as EMEWS, and can interoperate with other workflow frameworks such as Parsl, where the platform facilitates defining complex workflows and automating them through OSPREY capabilities.

Learn more about OSPREY from Jonathan Ozik, a principal computational scientist at Argonne National Laboratory (ANL), and Valerie Hayot-Sasson, a postdoctoral scholar at the University of Chicago and ANL in these past ParslFest talks:

<ul>
  <li><a href="https://youtu.be/1NAaV-FvVQo?si=Znr1gOy8fO52g5wx" target="_blank">OSPREY - Open Science Platform for Robust Epidemic Analysis</a></li>
  <li><a href="https://youtu.be/9R7zeVVhXp8?si=JShqJQu0TJQ7-dHx" target="_blank">Developing Distributed HPC Capabilities of an Open Science Platform for Robust Epidemic Analysis</a></li>
</ul>

<hr>

## OSPREY Highlights
<ul>
  <li><strong>Open Science Approach</strong>: It promotes open access to data, code, and methodologies, allowing researchers from different institutions to collaborate and contribute to epidemic modeling. </li>
  <li><strong>High-Performance Computing Integration</strong>: It aims to leverage powerful computing systems to handle large datasets and complex simulations efficiently, crucial for rapid analysis during outbreaks. </li>
  <li><strong>Automated Workflows</strong>: It strives to automate repetitive tasks in epidemic modeling, including data pre-processing, model calibration, and visualization, minimizing manual intervention. </li>
  <li><strong>Scalability and Flexibility</strong>: It is designed to accommodate diverse epidemic models and data sources, allowing researchers to adapt the platform to different scenarios.</li>
</ul>

## Potential Benefits of Using OSPREY
<ul>
  <li><strong>Faster Response Time</strong>: By streamlining analysis processes, researchers can quickly generate insights to inform public health interventions during outbreaks.</li>
  <li><strong>Improved Reproducibility</strong>: Open access to code and data enhances the transparency and replicability of research findings.</li>
  <li><strong>Collaboration Enhancement</strong>: OSPREY facilitates collaboration between researchers from different disciplines, leading to more comprehensive epidemic modeling. </li>
</ul>

Learn more about OSPREY’s ongoing development in this August 2024 HPCwire interview on “<a href="https://www.globus.org/news/preparing-for-the-next-pandemic" target="_blank">Preparing for the Next Pandemic: Developing an Open Science Platform for Better Decision-Making in Public Health</a>.”

