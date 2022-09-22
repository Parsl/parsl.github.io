---
layout: post
author: Dante D. Sánchez-Gallegos, Alfredo Barron, J. L. Gonzalez-Compean (Cinvestav Tamaulipas)
title: An overlay architecture based on in-memory content delivery for funcX in edge-fog-cloud
---

With the constant production of data, it is required tools for the efficient management of those data through different
infrastructures (e.g., the edge, the fog, or the cloud). To this end, we have designed an overlay architecture based on
in-memory content delivery for funcX in edge-fog-cloud. Figure 1 presents the conceptual design of this overlay
architecture, which includes a layer for managing the functions created by funcX. In this layer, the functions can be
organized in the form of patterns. In second layer, the endpoints triggered by each function launched in upper later. 

![Figure 1. Overlay architecture of a storage model for funcX.](https://raw.githubusercontent.com/Parsl/parsl.github.io/master/images/blog/2022-09-22/arch2.jpg)

The data layer implements a CDN based on in-memory storage, which includes a caching storage system. This system is based
on a pool of data containers (see DC in Figure 1), that contains software structures that implement a temporal and hierarchical
storage management to reduces the latency of the push/pull operations to deliver/retrieve data from the cloud storage locations.
The hierarchical storage strategy divides the available storage resources in the data container in three levels:

* First level: local memory (RAM).
* Second level: local storage (filesystem).
* Third level: cloud storage by using the CDN.

In this sense, the data produced by a function is cached in the local memory as first option. Two caching policies are available
in the data containers to add/remove data to/from each level of the hierarchical storage: last frequently used (LFU) and last
recently used (LRU).

In all cases, the endpoints deliver or retrieve data to/from the first level of the data container (memory). When this space is
full, the data container starts to use the level 2 (a volume in host hard disk in the data container), which preserves data
until, in deferred manner, an event at the functional level is started to sent data to the cloud.
