---
layout: post
author: Ben Clifford
title: Wrapping your workflows in __main__ protection
excerpt: TODO
---

Starting soon, you will probably need to start wrapping the main body of your parsl workflows with a test, if __name__ == "__main__". I'll talk about what I mean first, and then explain why later in this post.

Many people do this already, and many users get this done for them by a higher level framework.

I expect that the users that are affected are the users who directly write scripts.


Here's an example code change:

Before:

```
def my_app(x):
  return x+1

with parsl.load():
  print(my_app(10).result())
```

becomes:

```
def my_app(x):
  return x+1

if __name__ == "__main__":
  with parsl.load():
    print(my_app(10).result())
```

Roughly speaking: imports and definitions should live outside the protected block. Actions should live inside the protected block.

I opened <a href="https://github.com/Parsl/parsl/issues/3723">issue #3723</a> for discussion of this change a few weeks ago, after generally positive support on Parsl's Slack.

## What will happen if I don't make this change?

As we make non-backward-compatible changes to Parsl, you will start seeing your workflow myteriously starting multiple
times, inside the different helper processes that Parsl starts up.

## Why?

Parsl makes extensive use of the Python `multiprocessing` module, which helps you (or rather, Parsl) run Python 
code in multiple operating system processes: for example, there are processes to support task submission (the
interchange in the high throughput executor and the Work Queue submit process) and several parts of the monitoring
system to manage message routing and database access.

Python contains multiple implementations of the `multiprocessing` primitives (processes, queues, locks, etc)
with each implementation having a different mechanism for starting a new Python process that looks "right".
The options are detailed in the <a href="https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods">multiprocessing section of the Python manual</a>.

The traditional default for Python on Linux has been the `fork` start method, and a lot of Parsl was built assuming
that is the case. <a href="https://github.com/Parsl/parsl/pull/2099">PR #2099</a> made this more explicit in
the codebase.

Unfortunately, the `fork` start method doesn't work very well in the situations Parsl wants it to, and it is one
of the main causes of "mysterious" hangs in our test system (and so probably for users who silently endure
those hangs in the real world.)

I'm not alone in this opinion: Python will move to a new linux default, `spawn`, with Python 3.14; MacOS has used
`spawn` as a default for a long time and Parsl specifically overrides this to get `fork` behaviour; and Windows
does not support `fork` at all (and this is <a href="https://github.com/Parsl/parsl/issues/1878#issuecomment-1055974563">one of the immediate blockers</a> if you try to use Parsl on Windows).

## Moving Parsl away from `fork` multiprocessing

Parsl has already moved away from `fork` multiprocessing in a couple of places:

<a href="https://github.com/Parsl/parsl/pull/2983">PR #2983</a> switched the High Throughput Executor worker pool to use the spawn context internally;
and <a href="https://github.com/Parsl/parsl/pull/2983">PR #3463</a> starts
the interchange as a new command line process avoiding `multiprocessing` entirely.

Those were the relatively easy pieces.

What remains is harder to switch primarily because those processes are in sections of the code that need users to add the
boilerplate `__name__ == "__main__"` test that I talked about at the start of this post.

That requirement comes down to how the different multiprocessing start methods make new processes come into existence.

The `fork` method uses the unix `fork()` to make a quasi-duplicate of the currently running process: for example
that means all of the Python objects in memory and all of the imported modules are duplicated into the new process.
This does not compose well with threads.

A common hang in Parsl is when some thread is logging a message using Python's `logging` module at the point that
some other thread forks a new `multiprocessing` process - the new process launches with a copy of the logging locks,
locked because some code is doing logging. Then any log statement in the new process will hang, waiting for that
logging lock to become unlocked: the thread that was doing logging isn't running in this new process, and it will
never unlock the copy of the lock in this new process.

I've also seen this lock related behaviour at libc level, with name service resolution, and it is a fundamental
architectural property (or flaw) of trying to use multiprocessing and threads at the same time.

Since Python 3.12, Python has raised deprecation warnings when a fork happens in a process which also has
multiple threads - although this has always been a problem, less aggressively reported.

The `spawn` method does not have this behaviour: it starts a fresh Python process and initialises everything from
scratch. So there's a completely new logging system instance, with fresh clean locks. But in order to do that,
everything needs to be reloaded: modules need to be re-imported, and most relevant here, the original
workflow script needs to be reloaded in that new process.

And so, that means when using `spawn`, the original workflow script needs to not always run the workflow: when it
is in the original process, it should run the workflow. When it is loaded in other multiprocessing processes,
it shouldn't run the workflow - instead it should only do imports and definitions.

That's what `if __name__ == "__main__":` asks: are we running in the original process (where you would expect
this code to run) or are we being re-imported elsewhere?

## Conclusion

Add that `if` statement. It won't hurt with `fork` multiprocessing, and it will reduce the surprise as Parsl
moves to `spawn` multiprocessing, something that will probably happen to smash down on our last remaining known
race condition hangs.

