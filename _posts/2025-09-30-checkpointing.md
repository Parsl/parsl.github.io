---
layout: post
author: Ben Clifford
title: Reworking Checkpointing
excerpt: I've been reworking the checkpointing and memoization system
---

Parsl uses three different terms that mean almost (but not
quite) the same - checkpointing, memoization and app caching.
I've been working the code around this for better modularity
(aka better hackability) with some bug
fixing thrown in. This has been ongoing at a slow pace for
a long time but a recent talk at ParslFest 2025 got me paying
attention again and I've begun to merge a stack of pull
requests (available together as <a href="https://github.com/Parsl/parsl/pull/3535">PR #3535</a>)

So first, those three terms you'll see:

* *App caching* - to me, this implies the result might be forgotten and recomputed.

* *Memoization* -  to me, implies algorithmic correctness more than caching in the sense of <a href="">dynamic programming</a> - where things will go *wrong* if the result is not stored.

Parsl isn't trying to make either of the above implications
though: app caching and memoization mean exactly the same
thing in Parsl land, and the difference in phrasing is 
historical and spurious. Indeed, Parsl will run the same
app invocation twice if they're made  around the same time,
and if you're using the TaskVine executor, that can also
deliberately discard results if it decides it would be better
to recompute them.

* *Checkpointing* - to a lot of people, this means that
the entire state of the workflow is saved to disk in a way
that means the workflow can start up from where it left off.

That's broadly the intention of Parsl checkpointing, but
the implementation doesn't look like most people would
expect.

In many workflow systems, including VDS and Swift, 
the two ancestors of Parsl, a workflow is written in its own
language with a runtime that is amenable to this kind of
checkpointing.

Parsl chose to live elsewhere in the design space, using
Python as the runtime, and Python programs as workflows.
That is much less amenable to checkpointing the entire
state of the Python program. Instead, Parsl's checkpointing
system is built on top of the above memoization system,
extended to persist to disk. Restarting a checkpointed
workflow involves running the entire Python workflow code
from scratch, but individual app invocations complete quickly
because they have already been run in previous runs.

This style of checkpointing has a few interesting properties:

* if you modify the workflow to invoke a different collection
of apps, the checkpoint database can still be used if any of
those apps have been executed before - for example, if you
add/remove part of a workflow, but keep the rest the same.

* if your code performs intensive activity as part of the
workflow level Python code (not inside an app), the checkpoint
system won't see this at all: it won't be stored to disk,
and it will be re-done on subsequent workflow invocations.

So with that overview of three things that are almost the
same, what's in my stack of changes?

## Groundwork

First there's the background radiation of minor tidyups that
accompanies any of my visits to a particular piece of the
Parsl codebase, and that gets me the high commit
counts in relation to other Parsl contributors.

Next there is some modularisation: although some of the
memoization code lives in the `parsl.dataflow.memoization` 
module, other parts (especially related to checkpointing)
were put directly into the Data Flow Kernel.

The main motivation for this work is to make memoization
and checkpointing pluggable/hackable to help support a few
different usecases that don't fit into the current
implementation.

The first part of that is to move everything to do with
memoization and checkpointing into one place so that it
can be *unplugged* ready for a replacement. This is currently
split over a number of PRs because it is quite a lot of
code to move, and it isn't all simple copy/paste.

At the same time, this work has brought a known race condition
(<a href="https://github.com/Parsl/parsl/issues/3762">issue #3762</a>, a specialised form of the more broader task completion <a href="https://github.com/Parsl/parsl/issues/1279">issue #1279</a>) to prominence.

This issue harks back to the caching vs memoization
distinction I mentioned above: if a task T has finished
executing, should I expect a re-invocation to *always* be
memoized or merely *maybe*? The test suite assumes *always*
and I think that's the right behaviour. It isn't always the
case - indeed the test suite contains a suspicious
`time.sleep` around here, which suggests that this was
encountered by the test author and deliberately bodged around.

Fixing this is the main internal API ugliness of my work
so far: previously the result of an app was available to
the memoization and checkpointing code via the `AppFuture`
that is also shared with the user workflow. But that's also
the cause of the race condition: the checkpointing code was
getting its code at the "same time" as the user code, when
it is set on the AppFuture. So I have reworked the API
in a few places to pass results around outside of the
user-facing `AppFuture`, and moved memoization calls earlier
in the task competion process, before the user gets to
see the result.

## Configuration

With those changes in place, it's time for a big user-facing
configuration change: instead of specifying a set of
memoization and checkpointing parameters directly in the
`Config` object, the user now specifies a single Memoizer
object and all parameters are specified on that. This looks
the same as the executor, provider, launcher style of
configuration.

## New checkpointing options

With that done, I can do some fun hacking on Memoizer objects, driven by some real world use-cases people have asked for
in the past:

* hooks for deciding which results to checkpoint, and which
to re-use: prior to this work, all exceptions were discarded
(so that a re-run
would retry them rather than treat them as final) and
all results were stored in the checkpoint database. By
subclassing the new `BasicMemoizer` class, you can put in
your own filters to decide what gets stored and what gets
reused.

A usecase for this is something like discovering a bug in
your app code which manifests with certain parameters, so you
want to re-run your whole workflow, but you know some
checkpointed results are still valid.

Another usecase - for checkpointing exceptions - is when you
know the particular exception is "final" so will not go away
by re-running the app. This is roughly the same use case as
pluggable retry handlers (introduced in PR #2068) where you
might regard some exceptions as transient and some as final
in the eyes of the retry system (rather than the checkpoint
system).

* SQLite3-based out-of-memory memo/checkpointing: in the
existing memo and checkpointing system, there are two
stages: an in-memory data structure of every known task and
result; and an on-disk copy of that. Pretty much the
entire checkpoint database also lives in memory for the whole
run. I prototyped an SQLlite3 memoizer that doesn't store any
results in memory: everything lives in an SQLite3 database
with no distinction between *memoization* and *checkpointing*.

## Conclusion

I'm pushing these changes up to the Parsl `master` branch
piece by piece, with a lot of review from Kevin, The fun
stuff won't arrive until the very end, so you'll have to wait
a few weeks - or you can try out the whole stack as it
evolves right now in <a href="https://github.com/Parsl/parsl/pull/3535">PR #3535</a> and I would love some feedback on that!

