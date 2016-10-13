/*
 * EADF_Estimate.h
 *
 * Code generation for function 'EADF_Estimate'
 *
 */

#ifndef __EADF_ESTIMATE_H__
#define __EADF_ESTIMATE_H__

/* Include files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "EADF_Estimate_types.h"

/* Function Declarations */
extern void EADF_Estimate(const creal_T hlk[4], double *est_azim, double
  *est_elev);
extern void EADF_Estimate_free();
extern void EADF_Estimate_init();
extern void antennaCal_not_empty_init();

#endif

/* End of code generation (EADF_Estimate.h) */
