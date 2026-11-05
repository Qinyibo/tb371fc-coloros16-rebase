#ifndef TB371FC_SCHEDULER_POWER_H
#define TB371FC_SCHEDULER_POWER_H
/* 1=interactive, 0=noninteractive, -1=unavailable; failure never enables boost. */
int tb371fc_is_interactive(void);
#endif
