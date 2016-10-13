/*
 * EADF_Estimate_types.h
 *
 * Code generation for function 'EADF_Estimate'
 *
 */

#ifndef __EADF_ESTIMATE_TYPES_H__
#define __EADF_ESTIMATE_TYPES_H__

/* Include files */
#include "rtwtypes.h"

/* Type Definitions */
#include <stdio.h>
#ifndef struct_emxArray__common
#define struct_emxArray__common
struct emxArray__common
{
    void *data;
    int *size;
    int allocatedSize;
    int numDimensions;
    boolean_T canFreeData;
};
#endif /*struct_emxArray__common*/
#ifndef struct_emxArray_creal_T
#define struct_emxArray_creal_T
struct emxArray_creal_T
{
    creal_T *data;
    int *size;
    int allocatedSize;
    int numDimensions;
    boolean_T canFreeData;
};
#endif /*struct_emxArray_creal_T*/
#ifndef struct_emxArray_creal_T_1x4
#define struct_emxArray_creal_T_1x4
struct emxArray_creal_T_1x4
{
    creal_T data[4];
    int size[2];
};
#endif /*struct_emxArray_creal_T_1x4*/

#endif
/* End of code generation (EADF_Estimate_types.h) */
