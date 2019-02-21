# csc724-k8s
CSC724 Course Project on K8s scheduler



Commit message guidelines:

##########################################################################
1. First line identifies Task number and task name (less than 80 chars).
2. Next you define the problem (If applicable).
3. Describe the fix/changes.å
4. Describe the testing (If applicable or just say not tested yet).
5. Enlist the to-do tasks for this issue. (If applicable. You may choose
to say it's in progress)
##########################################################################

eg:

Issue #2: Kernel panic/sefgault when iterating over the threads

Reason: struct p_container had a member variable tracking the threads
(struct list_head *tasks). The head for this list was allocated on
the stack in add_container() method.
When iterating over the thread linked list in show_all_tasks() this
lead to illegal memory access when the head node was dereferenced
resulting into indeterminate behavior.

Fix: changed the member variable within p_container to
p_cont_thread*  (task_head) which keeps track of the list.
Head of the list is dynamically allocated in add_thread() method now
instead of statically allocating in add_container.
Also modified show_all_tasks() reflecting the changes made within p_container.

Non Functional changes:
Corrected indentation and placing of "{" curly braces in the code.

Testing:
1> Tested with 61 threads and 10 containers.
2> Also stress tested by running:
for i in {1..100}; do ./benchmark/benchmark 10 2 3 5 4 6 5 7 9 8 12; done

TODO:: Verify concurrency issues.
