/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#ifndef _SUMA_H_RPCGEN
#define _SUMA_H_RPCGEN

#include <rpc/rpc.h>

#include <pthread.h>

#ifdef __cplusplus
extern "C" {
#endif


struct suma_1_argument {
	int a;
	int b;
};
typedef struct suma_1_argument suma_1_argument;

struct resta_1_argument {
	int a;
	int b;
};
typedef struct resta_1_argument resta_1_argument;

#define SUMAR 99
#define SUMAVER 1

#if defined(__STDC__) || defined(__cplusplus)
#define SUMA 1
extern  enum clnt_stat suma_1(int , int , int *, CLIENT *);
extern  bool_t suma_1_svc(int , int , int *, struct svc_req *);
#define RESTA 2
extern  enum clnt_stat resta_1(int , int , int *, CLIENT *);
extern  bool_t resta_1_svc(int , int , int *, struct svc_req *);
extern int sumar_1_freeresult (SVCXPRT *, xdrproc_t, caddr_t);

#else /* K&R C */
#define SUMA 1
extern  enum clnt_stat suma_1();
extern  bool_t suma_1_svc();
#define RESTA 2
extern  enum clnt_stat resta_1();
extern  bool_t resta_1_svc();
extern int sumar_1_freeresult ();
#endif /* K&R C */

/* the xdr functions */

#if defined(__STDC__) || defined(__cplusplus)
extern  bool_t xdr_suma_1_argument (XDR *, suma_1_argument*);
extern  bool_t xdr_resta_1_argument (XDR *, resta_1_argument*);

#else /* K&R C */
extern bool_t xdr_suma_1_argument ();
extern bool_t xdr_resta_1_argument ();

#endif /* K&R C */

#ifdef __cplusplus
}
#endif

#endif /* !_SUMA_H_RPCGEN */
