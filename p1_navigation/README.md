[//]: # (Image References)

[image1]: https://user-images.githubusercontent.com/10624937/42135619-d90f2f28-7d12-11e8-8823-82b970a54d7e.gif "Trained Agent"

# Project 1: Navigation

> **_NOTE TO REVIEWER:_**  Information required for submission of the project can be found in section [Submission](#Submission) below.

## Introduction

For this project, you will train an agent to navigate (and collect bananas!) in a large, square world.  

![Trained Agent][image1]

A reward of +1 is provided for collecting a yellow banana, and a reward of -1 is provided for collecting a blue banana.  Thus, the goal of your agent is to collect as many yellow bananas as possible while avoiding blue bananas.  

The state space has 37 dimensions and contains the agent's velocity, along with ray-based perception of objects around agent's forward direction.  Given this information, the agent has to learn how to best select actions.  Four discrete actions are available, corresponding to:

- **`0`** - move forward.
- **`1`** - move backward.
- **`2`** - turn left.
- **`3`** - turn right.

The task is episodic, and in order to solve the environment, your agent must get an average score of +13 over 100 consecutive episodes.

## Getting Started

1. Download the environment from one of the links below.  You need only select the environment that matches your operating system:
    - Linux: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Linux.zip)
    - Mac OSX: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana.app.zip)
    - Windows (32-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Windows_x86.zip)
    - Windows (64-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Windows_x86_64.zip)

    (_For Windows users_) Check out [this link](https://support.microsoft.com/en-us/help/827218/how-to-determine-whether-a-computer-is-running-a-32-bit-version-or-64) if you need help with determining if your computer is running a 32-bit version or 64-bit version of the Windows operating system.

    (_For AWS_) If you'd like to train the agent on AWS (and have not [enabled a virtual screen](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-on-Amazon-Web-Service.md)), then please use [this link](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Linux_NoVis.zip) to obtain the environment.

2. Place the file in the DRLND GitHub repository, in the `p1_navigation/` folder, and unzip (or decompress) the file.

## Instructions

Follow the instructions in `Navigation.ipynb` to get started with training your own agent!  

## (Optional) Challenge: Learning from Pixels

After you have successfully completed the project, if you're looking for an additional challenge, you have come to the right place!  In the project, your agent learned from information such as its velocity, along with ray-based perception of objects around its forward direction.  A more challenging task would be to learn directly from pixels!

To solve this harder task, you'll need to download a new Unity environment.  This environment is almost identical to the project environment, where the only difference is that the state is an 84 x 84 RGB image, corresponding to the agent's first-person view.  (**Note**: Udacity students should not submit a project with this new environment.)

You need only select the environment that matches your operating system:

- Linux: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/VisualBanana_Linux.zip)
- Mac OSX: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/VisualBanana.app.zip)
- Windows (32-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/VisualBanana_Windows_x86.zip)
- Windows (64-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/VisualBanana_Windows_x86_64.zip)

Then, place the file in the `p1_navigation/` folder in the DRLND GitHub repository, and unzip (or decompress) the file.  Next, open `Navigation_Pixels.ipynb` and follow the instructions to learn how to use the Python API to control the agent.

(_For AWS_) If you'd like to train the agent on AWS, you must follow the instructions to [set up X Server](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-on-Amazon-Web-Service.md), and then download the environment for the **Linux** operating system above.

## Submission

In this section all required information as per [project rubric](https://review.udacity.com/#!/rubrics/1889/view) is provided.
All files can be found in folder [p1_navigation](https://github.com/toebgen/deep-reinforcement-learning/tree/master/p1_navigation) of the repository.

### Project Details

Most of the details are already described above in section [Introduction](#Introduction).
Here I want to make a few additions to the state space:

As mentioned above, the state space is continuous and consists of 37 dimensions.
To be precise, it consists of 35 dimensions for the ray-based perception of objects around the agent and 2 velocity dimensions.

The perception dimensions contain:
7 rays projecting from the agent at the following angles (and returned back in the same order):
`[20, 90, 160, 45, 135, 70, 110]` where `90` is directly in front of the agent.
Each ray is 5 dimensional itself and is projected into the scene.
It is of the form
`[Yellow Banana, Wall, Blue Banana, Agent, Distance]`.
If a ray hits a detectable object (that can can be `wall`, `agent`, `yellow banana` or `blue banana`), the value at that position in the array is set to `1`.
The `Distance` is a fraction of the ray length.
An example would be:
`[0, 1, 1, 0, 0, 0.2]`, which means that there is a blue banana detected 20% of the distance along the ray with a wall behind it.

The velocity of the agent is two dimensional:
left/right velocity (usually near 0) and forward/backward velocity (0 to 11.2).

### Implementation and Learning Algorithm

Details can be found in the [report](Navigation.html) and [Jupyter notebook](Navigation.ipynb), respectively.

### Dependencies

- Python 3.6
- PyTorch
- Numpy
- Matplotlib
- Specific (Udacity) unity banana environment, based on [Unity Machine Learning Agents (ML-Agents)](https://github.com/Unity-Technologies/ml-agents) v0.4, which can be found in the Udacity classroom
