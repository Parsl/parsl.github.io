---
layout: post
author: Ben Clifford
title: Wrapping your workflows in __main__ protection
excerpt: TODO
---

Starting soon, you will probably need to start wrapping the main body of your parsl workflows with a test, if __name__ == "__main__". I'll talk about what I mean first, and then explain why later in this post.

Many people do this already.

and many users get this done for them by a higher level framework.

so I expect that the users that are affected are the users who directly write scripts.


Example code change:

def my_app(x):
  return x+1

parsl.load()
print(my_app(10).result())


becomes:

def my_app(x):
  return x+1

if __name__ == "__main__":
  parsl.load()
  print(my_app(10).result())

Roughly: definitions should live outside the protected block. actions should live inside the protected block.

## Why?

Parsl makes extensive use of the Python `multiprocessing` module, which helps you (or rather, Parsl) run Python 
code in multiple operating system processes: for example, there are processes to support task submission (the
interchange in the high throughput executor, the Work Queue submit process, and several parts of the monitoring
system to manage message routing and database access).

Python contains multiple implementations of the `multiprocessing` primitives (processes, queues, locks, etc)
with each implementation having a different mechanism for starting a new Python process that looks "right".
The options are detailed in the <a href="https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods">multiprocessing section of the Python manual</a>.

The traditional default for Python on Linux has been the `fork` start method, and a lot of Parsl was built assuming
that is the case. <a href="https://github.com/Parsl/parsl/pull/2099">PR #2099</a> made this use more explicit in
the codebase.

Unfortunately, the `fork` start method doesn't work very well in the situations Parsl wants it to, and it is one
of the main causes of "mysterious" hangs in our test system (and probably, then, for users who silently endure
those hangs).

I'm not alone in this opinion: Python will move to a new linux default, `spawn`, with Python 3.14; MacOS has used
`spawn` as a default for a long time and Parsl specifically overrides this to get `fork` behaviour; and Windows
does not support `fork` at all (and this is <a href="https://github.com/Parsl/parsl/issues/1878#issuecomment-1055974563">one of the immediate blockers</a> if you try to use Parsl on Windows).

## Moving Parsl away from `fork` multiprocessing

This has already happened in a couple of places:

PR #2983 switched the High Throughput Executor worker pool to use the spawn context internally; and PR #NNNN starts
the interchange as a new command line process avoiding `multiprocessing` entirely.

Those were the relatively easy pieces.


