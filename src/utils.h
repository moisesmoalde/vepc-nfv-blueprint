#ifndef UTILS_H
#define UTILS_H
#define DEBUGG 0

/*			-----------VALUES FOR UE_BINDING-----------
 * 
 * 1 - ALWAYS SYNC IN CONTROL PLANE
 * 2 - SESSION SYNC IN CONTROL PLANE
 * 3 - NO SYNC IN CONTROL PLANE
 * 
 * */

#define UE_BINDING 3   //CHANGE THIS TO CHANGE SYNC MODE IN CONTROL PLANE

#define STATE_LESS 1
#define SESSION_BASED 2
#define UE_BASED 3
#define DATA_TRANSFER 1	 // PERFORM DATA PLANE OPERATION
/*			-----------VALUES FOR NOCACHE-----------
 * 0- SESSION SYNC IN DATA PLANE  
 * 1- ALWAYS SYNC IN DATA PLANE
 * */
#define NOCACHE 0    //CHANGE THIS TO CHANGE SYNC MODE IN DATA PLANE


#define REP 0			//CHANGE THIS TO TURN ON/OFF REPLICATION
#define DSR 0  		//CHANGE THIS TO SWITCH DATA STORE

/*
 *  DSR  0 LEVEL DB
 * 		1 REDIS
 * 		2 RAMCLOUD
 * 		3 MEMCACHED CONFIG 1
 * 		4 MEMCACHED CONFIG 2
 * 		99 FOR RAN AND SINK MODULE
 */
 
 /* TIMEOUT FOR FAULT TOLERANT TIMEOUT */
 
 /* TIMEOUT FOR FAULT TOLERANT TIMEOUT */
 
#define RETRY_LIMIT_FULL 8
#define RETRY_LIMIT_STEP 5
#define RETRY_Interval 4

/* (C++) chrono: high_resolution_clock, microseconds */
#include <chrono>

/* (C++) cout, endl */
#include <iostream> 

/* (C) INT_MAX */
#include <limits.h>

/* (C) pthread_create, pthread_kill */
#include <pthread.h>

/* (C++) STL: queue */
#include <queue>

/* (C++) default_random_engine, exponential_distribution<T> */
#include <random>

/* (C) signal */
#include <signal.h>

/* (C) memset, memmove */
#include <stdio.h>

/* (C) strlen */
#include <string.h>

/* (C++) STL: string */
#include <string>

/* (C++) stringstream */
#include <sstream>

/* (C++) STL: thread */
#include <thread>

/* (C++) STL: unordered map */
#include <unordered_map>

/* (C++) STL: vector */
#include <vector>

using namespace std;


typedef std::chrono::high_resolution_clock CLOCK;
typedef std::chrono::microseconds MICROSECONDS;

#define TRACE(x) if (DEBUGG) { x }

const int MAX_UE_COUNT = 10000;


class Utils {
public:
	void handle_type1_error(int, string);
	void handle_type2_error(int, string);
	char* allocate_str_mem(int);
	uint8_t* allocate_uint8_mem(int);
	void time_check(time_t, double, bool&);
	int max_ele(vector<int> inp);
};

extern Utils g_utils;

#endif /* UTILS_H */
