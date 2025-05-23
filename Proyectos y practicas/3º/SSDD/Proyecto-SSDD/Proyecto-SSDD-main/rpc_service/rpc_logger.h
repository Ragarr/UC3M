/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#ifndef _RPC_LOGGER_H_RPCGEN
#define _RPC_LOGGER_H_RPCGEN

#include <rpc/rpc.h>

#include <pthread.h>

#ifdef __cplusplus
extern "C" {
#endif


#define LOGGER_PROG 1
#define LOGGER_VERS 1

#if defined(__STDC__) || defined(__cplusplus)
#define LOG 1
extern  enum clnt_stat log_1(char *, void *, CLIENT *);
extern  bool_t log_1_svc(char *, void *, struct svc_req *);
extern int logger_prog_1_freeresult (SVCXPRT *, xdrproc_t, caddr_t);

#else /* K&R C */
#define LOG 1
extern  enum clnt_stat log_1();
extern  bool_t log_1_svc();
extern int logger_prog_1_freeresult ();
#endif /* K&R C */

#ifdef __cplusplus
}
#endif

#endif /* !_RPC_LOGGER_H_RPCGEN */
