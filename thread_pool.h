#pragma once

#include <pthread.h>
#include <vector>
#include <queue>

enum st { FINISH, CONTINIUE };

typedef struct Task {
	void (*f) (void *arg);
	void *arg;
	st status;
	pthread_mutex_t mutex;
	pthread_cond_t cond;
} Task;

typedef struct ThreadPool {
	st status;
	pthread_mutex_t mutex;
	pthread_cond_t cond;
	std::vector <pthread_t> thread;
	std::queue <Task*> task_queue;
} ThreadPool;

void thpool_init(ThreadPool* pool, size_t threads_nm);
void thpool_submit(ThreadPool* pool, Task* task);
void thpool_wait(Task* task);
void thpool_finit(ThreadPool* pool);



