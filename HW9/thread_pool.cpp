#include "thread_pool.h"

void* func(void* arg);

void thpool_init(ThreadPool* pool, size_t threads_nm) {
	pthread_mutex_init(&pool->mutex, NULL);
	pthread_cond_init(&pool->cond, NULL);
	
	pool->status = CONTINIUE;
	
	pool->thread.resize(threads_nm);
	for (size_t i = 0; i < threads_nm; i++)
		pthread_create(&pool->thread[i], NULL, func, pool);
}

void thpool_submit(ThreadPool* pool, Task* task) {
	pthread_mutex_init(&task->mutex, NULL);
	pthread_cond_init(&task->cond, NULL);
	
	pthread_mutex_lock(&task->mutex);
	task->status = CONTINIUE;
	pthread_mutex_unlock(&task->mutex);
	
	pthread_mutex_lock(&pool->mutex);
	pool->task_queue.push(task);
	pthread_cond_signal(&pool->cond);	
	pthread_mutex_unlock(&pool->mutex);
}

void thpool_wait(Task* task) {
	pthread_mutex_lock(&task->mutex);
	while (task->status == CONTINIUE)
		pthread_cond_wait(&task->cond, &task->mutex);
	pthread_mutex_unlock(&task->mutex);
}

void thpool_finit(ThreadPool* pool) {

	pthread_mutex_lock(&pool->mutex);
	pool->status = FINISH;
	pthread_mutex_unlock(&pool->mutex);
	
	pthread_mutex_lock(&pool->mutex);
	pthread_cond_broadcast(&pool->cond);
	pthread_mutex_unlock(&pool->mutex);
	
	for (size_t i = 0; i < pool->thread.size(); i++)
		pthread_join(pool->thread[i], NULL);
			
	pthread_cond_destroy(&pool->cond);
	pthread_mutex_destroy(&pool->mutex);
}

void* func(void* arg) {
	ThreadPool* pool = (ThreadPool*) arg;
	while(1) {
		pthread_mutex_lock(&pool->mutex);
		while (pool->task_queue.empty() && pool->status == CONTINIUE)
			pthread_cond_wait(&pool->cond, &pool->mutex);
			
		if (pool->task_queue.size()) {
			Task* task = pool->task_queue.front();
			pool->task_queue.pop();
			
			pthread_mutex_unlock(&pool->mutex);
			task->f(task->arg);
			pthread_mutex_lock(&task->mutex);
			
			task->status = FINISH;
			
			pthread_cond_broadcast(&task->cond);
			pthread_mutex_unlock(&task->mutex);
			pthread_mutex_destroy(&task->mutex);
			pthread_cond_destroy(&task->cond);
		} else if (pool->task_queue.empty() && pool->status == FINISH) {
			pthread_mutex_unlock(&pool->mutex);
			break;
		} else 
			pthread_mutex_unlock(&pool->mutex);		
	}
	return 0;	
}
	
