---
layout: post
author: Jamison Kerney (University of California, Berkeley) and Sophie Bui (Parsl)
title: Student Spotlight – Meet Jamison Kerney
excerpt: Jamison Kerney (he/him/his), a recent computer science graduate from the Illinois Institute of Technology, is working on improving Parsl for fine-grained parallelism. Check out this interview blog post to learn more about him and his work with our community.
---
<img src="/images/blog/2024-06-07/JK-PF23.png" width="95%" style="border:0px solid black;" alt="Jamison giving a presentation at ParslFest 2023.">

*Jamison giving a presentation on his project at ParslFest 2023.*
{: style="text-align: center;"}

Meet Jamison Kerney (he/him/his), a recent computer science graduate from the Illinois Institute of Technology (IIT) who is working on improving Parsl for fine-grained parallelism. In this student spotlight, we explore his work, interests, and future plans. 

### What will you do now since graduating from IIT this May?
After my undergraduate, I will continue studying computer science at UC Berkeley, as advised by Scott Shenker and Ion Stoica. Under their direction, I want to focus on operating systems, distributed systems, and programming languages with the intention of creating abstractions that fundamentally change how we interact with these systems. While working on research projects at IIT, I’ve been encouraged to attempt wacky and creative solutions that may or may not work out. I’ve never been bored working on a research project because there is always something to investigate, analyze, or build.

### Who/what inspired you to pursue this path?
I remember the moment I decided academia was the path for me. My mother dropped me off at Fermilab for <a href="https://saturdaymorningphysics.fnal.gov/" target="_blank">Saturday Morning Physics</a>, a free day program where physicists would lecture and give tours. Professor Dan Hooper, a physicist at the University of Chicago, was giving a lecture on particle physics, and I asked about quantum tunneling. Paraphrasing, he said the essence of quantum tunneling is uncertainty, and the implication of that idea in our world is that there is a chance I phase through the wall next to us.

I was totally transfixed. That thought was terrifying, amazing, and awe-inspiring. From that moment on, I knew I wanted a career similar to Professor Hooper. As an undergraduate student, my first research experience with Professor Ioan Raicu and Professor Kyle Chard reinforced my ambitions. Professor Raicu gave me the space to explore my ideas regarding his projects. I found this taste of intellectual life sweet.

<img src="/images/blog/2024-06-07/SMP-2018.png" width="95%" style="border:0px solid black;" alt="Dan Hooper giving a lecture to participants of Fermilab's Saturday Morning Physics Program">

*Dan Hooper giving a lecture at Fermilab's Saturday Morning Physics Program. 📷 Credit: <a href="https://saturdaymorningphysics.fnal.gov/" target="_blank">Fermilab</a>*
{: style="text-align: center;"}

### How did you learn about and get involved with Parsl?
I learned about Parsl by working with Professor Ioan Raicu. He asked a few students from his spring systems programming class to work with him over the summer. He outlined two projects. The first would involve working with Intel OneAPI and figuring out how Intel does fine-grained parallelism. The second involved figuring out how to improve Parsl for fine-grained parallelism. He mentioned that Parsl was written in Python, so I chose it because I believed my familiarity with Python would allow me to make more progress.

### What is your Parsl-related project title and its purpose?
The goal of our work Towards Fine-grained Parallelism in Parallel and Distributed Python Libraries was to improve the throughput of Parsl for tasks that have a short duration. We believe that workflows are trending toward smaller tasks and that it is crucial that Parsl throughput can scale with many small tasks.

### What did you enjoy most about this project? 
I enjoyed diving into the mud of the Python interpreter. I spent a lot of time in this project sorting through symbols in the Python interpreter and tracking tasks through Parsl’s execution pipeline. I felt like a detective, gathering puzzle pieces and trying to put them together. Combined with an intuition of how Parsl worked, I illustrated a picture of where processes and tasks spent their time.

<img src="/images/blog/2024-06-07/SC23-BigDataX.png" width="95%" style="border:0px solid black;" alt="A group photo of students and mentors at SC23.">

*REU students and mentors from IIT attending the IEEE/ACM Supercomputing/SC 2023 conference to present their summer research. 📷 Credit: <a href="http://datasys.cs.iit.edu/grants/BigDataX/">Data-Intensive Distributed Systems Laboratory</a>*
{: style="text-align: center;"}

### Who are your project mentors, and what did you learn from them? 
Professor Ioan Raicu and Kyle Chard were instrumental in helping me learn to do research. I appreciated their ability to sort through what I said. Every week, I would come to them with a bunch of questions and assertions. They gave me good pushback on faulty assertions while guiding me through the questions that came to my head. The most important thing I learned from them was how to jump into a research project, catch up on the literature, and expand on the work of others.

### What are some fun facts about yourself? 
I like to mountain bike and go to different ramen restaurants. I’ve been to 12 so far in Chicago and would love any recommendations, either in Chicago or around the world. 🍜

### What advice would you give to other aspiring students and potential mentors? What are your takeaways from this experience?
Don’t be afraid to get your hands dirty. I spent a lot of time playing with systems I did not fully understand. It’s okay not to fully understand what you're doing as long as you ask questions that guide you in a productive direction. Also, don’t be afraid to break things (in computer science and software, that is), especially in computer science, where most of the things we break can be fixed by typing `git reset --hard`. You gain a lot trying to make things work again because it makes you learn where you are, how you got there, and where you want to go. If you can answer these questions, you can fix anything, and in answering these questions, you also gain a deep understanding of complex systems.

My advice for potential mentors is to help your mentees ask questions that will guide them in a productive direction. This is what Ioan Raicu and Kyle Chard did for me, and I think it is the most important part of the research process.

<img src="/images/blog/2024-06-07/sc23-awards.png" width="95%" style="border:0px solid black;" alt="A photo of Jamison on stage at SC23 for winning 3rd place in the ACM Undergraduate Student Research Competition.">

*Jamison won 3rd place in the ACM Undergraduate Student Research Competition at SC23 for his work on Parsl titled "Supercharging Scientific Serverless: Slashing Cold Starts with Python UniKernels."*  📷 Credit: <a href="http://datasys.cs.iit.edu/grants/BigDataX/">Data-Intensive Distributed Systems Laboratory</a>*
{: style="text-align: center;"}

