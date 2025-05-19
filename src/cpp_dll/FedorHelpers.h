/**
 * FedorHelpers.h
 * 
 * Header file for the FEDOR OpenHoldem Helper DLL.
 * This DLL provides functions to assist the FEDOR.ppl OpenPPL profile,
 * particularly for board abstraction and action sequence tracking.
 */

#ifndef FEDOR_HELPERS_H
#define FEDOR_HELPERS_H

// Required for DLL export
#ifdef __cplusplus
#define EXPORT extern "C" __declspec(dllexport)
#else
#define EXPORT __declspec(dllexport)
#endif

/**
 * Example function declarations for the helper DLL.
 * These will need to be implemented in FedorHelpers.cpp.
 */

/**
 * Gets the board bucket ID for the current board texture.
 * This uses the k-means clustering from the board abstraction research.
 * 
 * @param street Current street (1=preflop, 2=flop, 3=turn, 4=river)
 * @return Board bucket ID (0 for preflop, clustering ID for postflop)
 */
EXPORT double __stdcall GetBoardBucketID(double street);

/**
 * Gets the effective stack category for a given player.
 * Categories are based on the project's stack size ranges:
 * 1: 2-5bb, 2: 6-10bb, 3: 11-15bb, 4: 16-20bb, 5: 21-25bb, 6: 26-30bb
 * 
 * @param chair Player chair ID (0-9) or -1 for hero
 * @return Stack category (1-6)
 */
EXPORT double __stdcall GetEffStackCategory(double chair);

/**
 * Gets the stack-to-pot ratio (SPR) category for a given player.
 * Categories are based on the project's SPR cutoffs:
 * 1: SPR < 1, 2: 1 ≤ SPR < 2, 3: 2 ≤ SPR < 3, etc.
 * 
 * @param chair Player chair ID (0-9) or -1 for hero
 * @return SPR category
 */
EXPORT double __stdcall GetSPRCategory(double chair);

/**
 * Gets a compact hash/ID for the current action sequence on this street.
 * This allows the PPL to differentiate between different betting sequences.
 * 
 * @param street Current street (1=preflop, 2=flop, 3=turn, 4=river)
 * @return Action sequence hash/ID
 */
EXPORT double __stdcall GetActionSequenceHash(double street);

#endif // FEDOR_HELPERS_H 