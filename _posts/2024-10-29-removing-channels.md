---
layout: post
author: Ben Clifford
title: Removing Channels
excerpt: In November 2024, Parsl's little used Channel abstraction is going away. Here are some details.
---

Since the beginning, Parsl has had facilities for executing code elsewhere: for example, the High Throughput Executor helps you run tasks on different nodes within a supercomputer. Beyond that, the <em>channel</em> abstraction was aimed at getting the High Throughput Executor (and its predecessors) running on some remote site - to support use cases such as running a workflow on two supercomputers at once or running your workflow on your desktop PC with tasks executing on a supercomputer backend.

This multisite behaviour is complicated, and the channels ignore most of the complications, instead focusing on a tiny piece of the problem: how to run a batch job submission on a remote site. This goes back decades: for example, the Globus Toolkit GRAM component, from largely the same groups as Parsl and released in the late 1990s, had the same focus. In part, because Parsl doesn't do a good job (or any job, in some cases) with the other complications, not many people run multisite workloads.

More recently, the groups that might have pushed on Parsl's remote execution have put their energy into developing <a href="https://www.globus.org/compute">Globus Compute</a> and imagining the way forward as Parsl submitting tasks into Globus Compute. Yadu gave a talk on the most recent work (<a href="https://youtu.be/6TFTzIdWwUg">video</a>, <a href="https://parsl-project.org/parslfest/2024/Babuji-Yadu_PF24-Channels-and-GCE.pdf">slides</a>) at <a href="https://parsl-project.org/parslfest/parslfest2024.html">ParslFest 2024</a>, and Reid wrote this blog post about <a href="https://parsl-project.org/2024/06/26/parsl-globus-compute.html">earlier techniques</a>.

So with a strong abandonware vibe around channels, and with that code tangled throughout the codebase complicating understanding and maintenance, I advocated for the removal of channels in <a href="https://github.com/Parsl/parsl/issues/3515">GitHub issue #3515</a>. This is scheduled for the 7th of November, 2024 - a week in the future, at the time of writing.

So, how does this affect you? For most users, the changes will be minimal. tl;dr: If your Parsl configuration has a line `channel=LocalChannel()`, then remove it.

### What's Being Removed

Some components are being removed outright: all of the SSH-based channels that facilitate launching batch jobs (and, so, High Throughput Executor worker pools) over SSH, and the Ad-hoc Provider, which aims to support low-end clusters that have no resource manager and which only works when there are channels available to each worker node.

For running remotely on other sites, the rough consensus amongst core Parsl people is that you should have Parsl submit tasks into Globus Compute - see the links to Yadu's talks and Reid's blog post above.

For running on a cluster with no resource manager, our suggestion is to bite the bullet and install a resource manager: Parsl should not be trying to be a lightweight or fake resource manager. The most tested resource manager is <a href="https://slurm.schedmd.com/documentation.html">Slurm</a>. The Slurm provider is even tested in our automated tests (after Nick Tyler's contribution <a href="https://github.com/Parsl/parsl/pull/3606">in September</a>).

Some users start HTEX worker pools themselves manually, without using Parsl's channel or provider mechanism to do so. These changes don't affect that: manual worker pools remains as moderately-supported as always.

### Obscure Changes

The aim of this work is to remove the channel abstraction entirely. That includes the `LocalChannel`, which most Parsl configurations use (often implicitly) - which involves removing a few smaller features (that I think no one uses):

The LocalChannel has an `env` parameter which allows the environment to be overridden when executing batch job management commands. In practice, people set the environment before they run their workflow script, and there is no plan to make this more specific environment possible anymore. There is a subtle user-facing change here, even if you aren't setting the `env` parameter to `LocalChannel`: the current `LocalChannel` implementation caches the Unix environment at the time the LocalChannel is instantiated so that if the user workflow changes the environment (for example using <a href="https://docs.python.org/3/library/os.html#os.environ">os.environ</a>), batch job commands run through the `LocalChannel` will not see that. When `LocalChannel` disappears, this cache will also disappear, and batch job commands will see the submit process environment at the point they are executed. For the same reason that I think `env` is not needed, I think this cache removal will not affect normal users. (Let me know if it does!)

Another set of small changes has to do with the distinction between the submit-side script directory (usually `submit_scripts`) and the remote-side script directory. There is state in the `LocalChannel` to let this be specified by the user or computed and stored by Parsl's initialization code, and some providers have options (`move_files`) to configure when scripts will be moved between the two directories. As there is no distinct remote-side anymore, all of this can go away. As with `env`, there is a subtle user facing change (or probably a bug) here: when `LocalChannel` objects are re-used between multiple DFKs in the same process, Parsl will screw up the `script_dir` because there is confusion of whether that is scoped by process or by DFK. A side effect of this channel removal work is that misbehaviour will go away.

### Conceptual Cleanups and Source Code Maintainability

With channels gone, I hope that users will stop trying to use them and being faced with an support response of either awkward silence or "we think you should do something else".

In addition to the completely deleted code (SSH channels, ad-hoc provider), there are a few screenfuls of code removal in Parsl's initialization code and in various provider implementations. These removals should make things a bit easier to understand, and now that providers don't have to be able to operate remotely, opens the way for further simplifications in some cases.

In preparation for November 7th, a handful of tidyups (the ones that shouldn't affect users) have already been merged and released in Parsl 2024.10.28.

### Be Involved

Parsl's provider mechanisms are not well tested - for example our PBS providers are untested and rely either on developers being careful or user reports. So you might try out the prototype of Parsl-without-channels in <a href="https://github.com/Parsl/parsl/pull/3650">pull request #3650</a> in your own environment, and comment there with success or failure stories.

If you'd like us not to remove features that you're using, consider turning on <a href="https://parsl.readthedocs.io/en/stable/userguide/usage_tracking.html">usage statistics collection</a> for all of your workflow runs. We focus our maintenance efforts primarily on what is actively used, so the more information, the better.
