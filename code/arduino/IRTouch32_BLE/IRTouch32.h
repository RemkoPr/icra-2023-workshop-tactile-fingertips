#ifndef _IRTOUCH32_H_
#define _IRTOUCH32_H_

#include <map>

#define NUM_MUXS               4
#define NUM_DATA_VALUES        32
#define MUX_IRTOUCH32_S0	D6
#define MUX_IRTOUCH32_S1	D7
#define MUX_IRTOUCH32_S2	D8

int read_pins[4] = {A0, A1, A2, A3};

int measure_idx_to_grid_idx[NUM_DATA_VALUES] = {
//		MUX1	MUX2	MUX3	MUX4
/*S000*/	6,	13,	18,	28,
/*S001*/	7,	14,	20,	29,
/*S010*/	8,	15,	19,	30,
/*S011*/	4,	12,	23,	27,
/*S100*/	3,	11,	22,	31,
/*S101*/	0,	5,	17,	24,
/*S110*/	2,	10,	21,	26,
/*S111*/	1,	9,	16,	25
};

void selectIRTouchMuxOut(uint8_t outNr) {
  // outNr = 0..7, following the 74HC4051PW,118 datasheet
	if( outNr > 7 ) {
		return;
	}
	if ( outNr & 0b001 ) { digitalWrite(MUX_IRTOUCH32_S0, HIGH); } else { digitalWrite(MUX_IRTOUCH32_S0, LOW); }
	if ( outNr & 0b010 ) { digitalWrite(MUX_IRTOUCH32_S1, HIGH); } else { digitalWrite(MUX_IRTOUCH32_S1, LOW); }
	if ( outNr & 0b100 ) { digitalWrite(MUX_IRTOUCH32_S2, HIGH); } else { digitalWrite(MUX_IRTOUCH32_S2, LOW); }
}

#endif /* _IRTOUCH32_H_ */
