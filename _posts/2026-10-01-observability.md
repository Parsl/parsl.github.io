---
layout: post
author: Ben Clifford
title: Parsl Observability
excerpt: The past and future of observability in Parsl
---

When Parsl started, observability wasn't really on the radar - by that, I mean we didn't really intend for users to look inside Parsl and see and understand what was happening there. You submit your tasks, let Parsl do its magic, and your results pop out in <code>Future.result()</code>.

But users *do* want to look inside and understand what is happening: has my 12h task been running for the last 6 hours or is it waiting for some dependency to complete?

We've ended up with two observability approaches, which are (for me) frustratingly complementary: a structured monitoring system (mainly configured via the <code>monitoring=MonitoringHub(...)</code> configuration option; and text based logging, configured (if at all) by ad-hoc parameters.

In this post, I'll talk about the history of these two systems and my slow work to combine them into a single more coherent approach.

# Structure of Parsl observability

I'm going to split the Parsl observability story into four (often overlapping) stages:

1. What information to collect and from which components to collect it?

2. How that information is coveyed to where you are going to analyse it

3. How you model and query that collected data

4. How you analyse and present it

These are all big problem spaces in themselves. Parsl isn't going to provide a universal solution and should not be trying to,  so I'll be pushing on a modular/plug in style.


# Monitoring and logging

In this section, I'll try to describe the existing monitoring and logging approaches divided into those four stages.

Monitoring started as a summer project prototype from the early times when we didn't regard observability as a primary feature, but it was intended to be user facing.

In contrast, logging (built around Python's standard logging system) came with a vibe of "these logs are for Parsl developers to look at when Parsl is broken", an almost guilty feeling.

## What information to collect?

<b>Monitoring:</b> Monitoring was targeted at making a very structured database giving a relatively small amount of coarse-grained information about Parsl-level entities, primarily tasks. Most status information comes from reports within the DFK and tightly coupled classes on the submit side: is a task completed? has a block of workers been submitted? A resource-monitoring wrapper can run around each task and collects on-worker start/end time (the <code>running</code> and <code>running_ended</code> task states that the DFK never knows about), and can ask the operating system for CPU and memory usage.

<b>Logging:</b> This has a history as a schemaless spew of Parsl-developer-oriented debugging information. Log entries arose mostly as whatever seemed useful at the time and are human-oriented. Each separate process (of which Parsl has many) logged into different files.


## How information is conveyed where it needs to go

<b>Monitoring:</b> The repository for all Parsl monitoring information is an SQLite database, populated by one database manager process per workflow. Monitoring information about a workflow heads towards that process:

For submit-side information (from the main workflow process and the HTEX interchange), local TCP sockets are used using the ZMQ message protocol - the same protocol used for HighThroughputExecutor tasks and results.

For over-the-network information from worker nodes, initially monitoring messages were sent over a simple UDP protocol. This had a few weaknesses because of unreliability: a dropped UDP packet means lost information, and lost information leads to complexity when trying to live-reshape that information to fit into a strong relational/SQL schema. So around PR #3892 monitoring got a new feature, the ability to plug in different <code>MonitoringRadio</code> implementations. There are two alternatives to UDP here: for <code>HighThroughputExecutor</code> users, the <code>HTEXRadio</code> uses the normal result return network channels, and monitoring information is as reliable as returning results from a task; for other executors, the <code>FilesystemRadio</code> uses a <a href="https://en.wikipedia.org/wiki/Maildir">maildir</a> style message-per-file over a shared file system, using the network file system as the network layer. This also gives a high level of reliability but does generates a lot of filesystem metadata traffic, something that traditionally has not been appreciated by HPC shared filesystems.

<b>Logging:</b> Logs from each process or component go into files. Those files are usually in the shared run directory, and so the network file system provides the network transport.


## How to model and query data

<b>Monitoring:</b>Everything goes into an sqlite database on the submit side, and there is <a href="https://en.wikipedia.org/wiki/SQL#History">an extremely mature query language, SQL</a> available to make queries, along with lots of language tooling to help you pull results into Python (for example).

<b>Logging:</b> tl;dr: You're on your own. Good luck!

The log files were originally intended for manual reading by humans. Any mechanical processing of log data usually starts with an ad-hoc parser to pull information out of log messages. This is extremely fragile.

There is a lot of information in log files, far more than in the monitoring database, and so people (myself included) keep doing this. As an example I've wanted in the past, think: a histogram of time between task submission to the DFK, and the task arriving at the htex interchange.


## How to analyse and present data

<b>Monitoring:</b>There's a much-neglected web user interface, <code>parsl-visualize</code>, which can show a few analyses from the monitoring database. 

As many Parsl users are very data-processing literate, it is also common for users to make simple SQL queries against the database and process the results in Python, often plotting with matplotlib.

<b>Logging:</b>The story here is basically a continuation of the above-described fragile parsing approach. Do whatever works for right now, it will break as soon as we tweak the log messages.


# A few use cases that aren't well supported

As research-oriented software, people often want to do interesting or strange things to/with Parsl.

This is non-exhaustive list of such things to help get a feel for what I think we shouldn't directly implement in Parsl but that seems interesting.

<a href="https://cctools.readthedocs.io/en/latest/work_queue/">Work Queue</a>, the engine behind the <code>WorkQueueExecutor</code> is written in C and makes some of its logs available in a nicely formatted space-separated format defined by the Work Queue developers. It isn't going to be adapted to be able to use some Python/Parsl logging system, but we have had useful results correlating those logs with main Parsl logs.</p>

I've worked on the edges of two projects, <a href="https://chronolog.dev/">Chronolog</a> and <a href="https://diaspora-project.github.io/">Diaspora Octopus</a>, which put serious effort into moving events across the network - both of these we've looked at wiring into Parsl.

There are always people wanting to do something with provenance. Most recently, in the Academy implementation of observability, Valesca Moura worked on getting data into Flowcept (see <a href="https://parsl-project.org/parslfest/2026/moura-provenance.pdf">ParslFest slides</a> and I think that work transfers pretty directly into something that could be done with Parsl.

Application projects often implement science-specific workflow systems that delegate a lot of execution work to Parsl. Those systems have their own notion of task, which isn't exactly the same as a Parsl task (in the same way that a Work Queue level task isn't the same as a Parsl-level task) but which users would like to consider alongside each other.


# Where I see Parsl observability going

Broadly I've been building on the log based approach, bringing in useful features from monitoring: more structured data, more expectation of consistency, more expectation of pluggability/hackability.

I think that looks something like:

## What data to collect and where

In Python code, Parsl (and other Python components) log using the built-in <code>logging</code> module. Each log message can be annotated with structured data, which can be written out alongside the human readable component. 

So I've been making log messages contain more structured data. For example, PR #4153 adds structured data to the log message that describes how a particular task is running a particular named app, and some of this structured log data is now tested by the automated test suite as a real part of the user facing API.

As mentioned, other components don't write using the Python API but it is reasonable to push on them being parseable. Work Queue is a good example here of something that already does structured logging in its own way.


## How information is conveyed

Log files on a networked filesystem are a fine start to this. In Python-land, the <code>logging</code> module supports configurable log handlers to send log data elsewhere. I've already added mechanisms specify that configuration across the various Python processes that Parsl launches (the LogConfig abstraction, in PR #4091 onwards), and implemented a JSON-in-file configuration which makes downstream machine processing easier (the tradeoff is less human readability in a simple text viewer)

This configuration abstraction should help support Diaspora, Chronolog, Flowcept-style use cases too.

Other components like Work Queue already output logs to files, and although they can't directly benefit from the new LogConfig mechanism, there is potential for parsing that data at-source rather than at-destination later on and sending over arbitrary Python loggers.


## How information is processed

Moving to a log/event format doesn't dictate a particular storage mechanism. The lazy default is keeping records per-line on the filesystem and doing interesting stuff like joining/indexing at the analysis stage. For most Parsl runs that I've encountered, there are few enough log lines that loading everything into a process memory for analysis works ok.

There is opportunity for experimentation though. For example, I've also tried querying logs from a database using SQLite's JSON handling, and done some work on relational operators in Python for key-value style events.

One big difference here compared to the kind of observability you'll find in the web/phone app applications crowd is that there are far more experimental pieces added in that do not buy into a coherent observability story. Application based observability will usually expect every component to be add hierarchical context onto every log message from an invoking application. In the bolt-pieces-together world of Parsl, that isn't a reasonable expectation, and so analysis must expect to be doing something a bit more like relational joins between log files (for example, to relate a Parsl task in a Parsl log file with a Work Queue task in a Work Queue log file).

## How information is presented

As a short term concrete motivating example, I worked on implementing something like <code>parsl-visualize</code>, additionally incorporating analyses that have been done elsewhere (for example, block load graphs used to analyse scaling in efficiency, and task duration histograms often desired by experimental physicists).


# Conclusion

So that's the direction I've been pushing. This work is more a lifestyle or vibe, than a particular single end product or configurable feature - logging is the prototypical "cross cutting concern" when building modular applications. What I hope to do is rather than conduct ad-hoc analyses so much in the future, to instead be able to implement those analyses as someting reusable and documentable and shareable; and to help a bunch of future research projects do interesting workflow stuff without needing to hack up Parsl core so much.

