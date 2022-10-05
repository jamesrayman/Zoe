# Zoe

Zoe is a toy language invented for a "programming linguistics puzzle."

In typical linguistics puzzles, you are given a task to accomplish in
some _natural_ language you are not expected to know, such as
translating sentences. Of course, since you aren't expected to know the
language, you are also given some helpful information about the
language, such as some sentences that are already translated for you.
[NACLO] is one source of such puzzles.

[NACLO]: https://nacloweb.org/

So, for this puzzle, you have to complete a task in a _programming_
language you are not expected to know. That language is Zoe, and the
reason you don't know it is that I invented it. You are given a Zoe
interpreter, which you can use to run Zoe programs.

To install the interpreter, open a terminal in this directory and run:

    pip install -e .

After that, you can run Zoe programs like so:

    zoe hello.zoe

If this doesn't work, it's probably because I wrote the interpreter on
Linux with Python 3.8. Note that some of the Zoe programs read input.

Now, here's your task: Write a Zoe program that reads in a positive
integer less than 200 and prints that many rows of Pascal's triangle.
Here is some sample data:

Input:

    1

Output:

    1


Input:

    5

Output:

    1
    1 1
    1 2 1
    1 3 3 1
    1 4 6 4 1


Input:

    10

Output:

    1
    1 1
    1 2 1
    1 3 3 1
    1 4 6 4 1
    1 5 10 10 5 1
    1 6 15 20 15 6 1
    1 7 21 35 35 21 7 1
    1 8 28 56 70 56 28 8 1
    1 9 36 84 126 126 84 36 9 1


You are not allowed to print any extra characters, except for extra
spaces at the end of a line and extra blank lines at the end of the
output.

I am not giving you any documentation for Zoe. You have to learn it
yourself using the resources I give you. Here are the rules:

1. You are allowed to examine and run the sample Zoe programs I have
   given you.
2. You are allowed to write your own Zoe programs and run them.
3. You are not allowed to look at the source code for the interpreter.
   Of course, I can't really enforce this rule, but if you break it,
   you'll have to live with the fact that you are a cheater.

Once you think you've solved the challenge (say your program is in
'pascal.zoe'), then run the following command (it may take a few
seconds to get any output):

    zoe! pascal.zoe

If your program is incorrect, you will be notified of which test case
failed. Otherwise, you will be congratulated for completing the
challenge.

The error handling on the interpreter isn't the best, so I apologize in
advance if you have trouble debugging. (Although, if the errors were too
descriptive, it would make the challenge too easy...)

If you get stuck, the solution is in the `solution/` directory.
