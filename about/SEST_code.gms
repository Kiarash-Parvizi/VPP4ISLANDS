sets
spv  PV scenarios /spv1*spv3/
sw   Wind scenarios /sw1*sw3/
b    buses /b1*b15/
sb   source buses /sb1/
l    lines /l1*l14/
t    hours of day /t1*t24/
h    Number of power section P y Q   /h1*h10/
DG   DG numbers /dg1*dg2/
ES   ES numbers /es1/
FL   Flexible load numbers /fl1*fl3/

alias(b,bb);
alias(t,tt);

TABLE DGData(DG,*)  DG DATA  kW
      Pmax   Pmin   Qmax   Qmin  RU    RD   MUT   MDT   SUC  SDC  GenCost
dg1   600    100    400    0     105   120  2     2     20   20   0.040
dg2   950    200    600    0     175   200  3     3     30   20   0.035
;

TABLE ESData(ES,*)  ES DATA  kW
      Pcap   Emax   SOCmin   SOCmax    Eff    SOCini
es1   100    200    0.1      0.9       0.85   0.5
;

TABLE FLData(FL,*)  Flexible load DATA  kW
      Alpha   LR_pickup   LR_drop    INC
fl1   0.2     20          20         0.035
fl2   0.2     35          35         0.035
fl3   0.2     25          25         0.035
;


Table DGM(dg,b)  DG MAPPING
      b1   b2    b3    b4    b5    b6   b7   b8   b9    b10   b11   b12   b13   b14   b15
dg1   0    0     0     0     0     0    1    0    0     0     0     0     0     0     0
dg2   0    0     0     1     0     0    0    0    0     0     0     0     0     0     0
;

Table ESM(es,b)  ES MAPPING
      b1   b2    b3    b4    b5    b6   b7   b8   b9    b10   b11   b12   b13   b14   b15
es1   0    0     0     0     0     0    0    0    0     0     0     0     1     0     0
;

Table FLM(fl,b)  FL MAPPING
      b1   b2    b3    b4    b5    b6   b7   b8   b9    b10   b11   b12   b13   b14   b15
fl1   0    0     1     0     0     0    0    0    0     0     0     0     0     0     0
fl2   0    0     0     0     0     0    0    1    0     0     0     0     0     0     0
fl3   0    0     0     0     0     0    0    0    0     0     0     0     0     0     1
;

** Network Structure
sets
sourcebuses(sb,b)  Source Buses Definition  /sb1.b1/

lines(b,bb,l)     Line buses
/
b1.b1.l1
b2.b2.(l1,l2,l5,l7)
b3.b3.(l2,l3,l10)
b4.b4.(l3,l4)
b5.b5.l4
b6.b6.(l7,l8,l9)
b7.b7.l8
b8.b8.l9
b9.b9.(l5,l6)
b10.b10.l6
b11.b11.(l11,l10)
b12.b12.(l12,l11)
b13.b13.l12
b14.b14.l13
b15.b15.l14

b1.b2.l1
b2.b3.l2
b3.b4.l3
b4.b5.l4
b2.b9.l5
b9.b10.l6
b2.b6.l7
b6.b7.l8
b6.b8.l9
b3.b11.l10
b11.b12.l11
b12.b13.l12
b4.b14.l13
b4.b15.l14
/

lines1(b,bb,l)     Lines buses
/
b1.b2.l1
b2.b3.l2
b3.b4.l3
b4.b5.l4
b2.b9.l5
b9.b10.l6
b2.b6.l7
b6.b7.l8
b6.b8.l9
b3.b11.l10
b11.b12.l11
b12.b13.l12
b4.b14.l13
b4.b15.l14

b2.b1.l1
b3.b2.l2
b4.b3.l3
b5.b4.l4
b9.b2.l5
b10.b9.l6
b6.b2.l7
b7.b6.l8
b8.b6.l9
b11.b3.l10
b12.b11.l11
b13.b12.l12
b14.b4.l13
b15.b4.l14
/

fbuses(l,b) Lines From Buses
/
l1.b1
l2.b2
l3.b3
l4.b4
l5.b2
l6.b9
l7.b2
l8.b6
l9.b6
l10.b3
l11.b11
l12.b12
l13.b4
l14.b4
/

tbuses(l,b) Lines To Buses
/
l1.b2
l2.b3
l3.b4
l4.b5
l5.b9
l6.b10
l7.b6
l8.b7
l9.b8
l10.b11
l11.b12
l12.b13
l13.b14
l14.b15
/

bus(b,bb)  bus conected to other bus
/
b1.b2
b2.b3
b2.b9
b2.b6
b3.b4
b3.b11
b4.b5
b4.b14
b4.b15
b6.b7
b6.b8
b9.b10
b11.b12
b12.b13

b2.b1
b3.b2
b9.b2
b6.b2
b4.b3
b11.b3
b5.b4
b14.b4
b15.b4
b7.b6
b8.b6
b10.b9
b12.b11
b13.b12
/
;

scalars
Sbase  VA /2300000/
Vbase  volt /11000/
PF     Arccos (0.85) /0.6197/
PVbus  PV bus No. /11/
Wbus   Wind bus No. /14/
PV_Rated    PV Site Capacity (W) /200000/
Wind_Rated  Wind farm Capacity (W) /500000/
Ibase       Current base value
Zbase       Impedance base value
********************************************
VMIN        Minimum value of the grid voltage (pu) /0.95/
VMAX        Maximum value of the grid voltage (pu) /1.05/
VNOM        Nominal voltage of the grid (pu) /1/
VMIN2       Minimum value of the grid voltage square
VMAX2       Maximum value of the grid voltage square
VNOM2       Nominal value of the grid voltage square
;

Ibase=Sbase/(1.732050*Vbase);
Zbase=Vbase/(1.732050*Ibase);
VMIN2=VMIN*VMIN;
VMAX2=VMAX*VMAX;
VNOM2=VNOM*VNOM;

Table   PwPU(sw,t)  (p.u.)
       t1       t2                 t3                 t4                 t5                 t6                 t7                 t8                 t9                 t10                t11                t12                t13                t14                t15                t16                t17                t18                t19                t20                t21                t22                t23                t24
sw1    1.2      1.114470413        1.049428145        0.969070114        0.878368971        0.853306813        0.853107907        0.804574838        0.75206365         0.668722029        0.588165092        0.533863749        0.507210343        0.504425659        0.516757832        0.576628543        0.674888115        0.768970661        0.841173545        0.886126305        0.927498757        0.98677275         1.055793138        1.10114371
sw2    1        0.928725344        0.874523454        0.807558429        0.731974142        0.71108901         0.710923255        0.670479032        0.626719708        0.557268357        0.490137577        0.444886458        0.422675286        0.420354716        0.430631527        0.480523786        0.562406763        0.640808884        0.700977955        0.738438588        0.772915631        0.822310625        0.879827615        0.917619758
sw3    0.8      0.742980275        0.699618763        0.646046743        0.585579314        0.568871208        0.568738604        0.536383226        0.501375767        0.445814686        0.392110061        0.355909166        0.338140229        0.336283773        0.344505221        0.384419029        0.44992541         0.512647108        0.560782364        0.59075087         0.618332505        0.6578485          0.703862092        0.734095806
;

Table   PpvPU(spv,t)  (p.u.)
         t1        t2        t3        t4        t5        t6        t7        t8                 t9                 t10                t11                t12                t13                t14                t15              t16                t17                t18                t19      t20      t21      t22      t23      t24
spv1     0         0         0         0         0         0         0         0.274285636        0.754285499        0.99428543         1.165713953        1.199999657        0.68571409         0.754285499        0.47890272       0.343301045        0.274289064        0.089840546        0        0        0        0        0        0
spv2     0         0         0         0         0         0         0         0.228571363        0.628571249        0.828571192        0.971428294        0.999999714        0.571428408        0.628571249        0.3990856        0.286084204        0.22857422         0.074867121        0        0        0        0        0        0
spv3     0         0         0         0         0         0         0         0.182857091        0.502856999        0.662856953        0.777142635        0.799999771        0.457142727        0.502856999        0.31926848       0.228867363        0.182859376        0.059893697        0        0        0        0        0        0
;

Table   ElectricDemand(b,t)  (kWh)
          t1              t2              t3             t4              t5              t6              t7               t8               t9               t10             t11             t12              t13              t14                        t15                        t16                        t17                        t18                        t19                        t20               t21                        t22                        t23                        t24
b2        44.25882353     40.48676471     38.09779412    36.96617647     37.21764706     38.72647059     41.36691176      43.50441176      50.04264706      38.33595156     55.575          57.58676471      57.83823529      55.82647059                52.55735294                51.04852941                51.67720588                52.05441176                54.06617647                59.85             57.58676471                51.80294118                47.40220588                43.00147059
b3        70.25210084     64.26470588     60.47268908    58.67647059     59.07563025     61.47058824     65.66176471      69.05462185      79.43277311      60.85071676     88.21428571     91.40756303      91.80672269      88.61344538                83.42436975                81.02941176                82.02731092                82.62605042                85.81932773                95                91.40756303                82.22689076                75.24159664                68.25630252
b4        140.5042017     128.5294118     120.9453782    117.3529412     118.1512605     122.9411765     131.3235294      138.1092437      158.8655462      121.7014335     176.4285714     182.8151261      183.6134454      177.2268908                166.8487395                162.0588235                164.0546218                165.2521008                171.6386555                190               182.8151261                164.4537815                150.4831933                136.512605
b5        44.25882353     40.48676471     38.09779412    36.96617647     37.21764706     38.72647059     41.36691176      43.50441176      50.04264706      38.33595156     55.575          57.58676471      57.83823529      55.82647059                52.55735294                51.04852941                51.67720588                52.05441176                54.06617647                59.85             57.58676471                51.80294118                47.40220588                43.00147059
b6        140.5042017     128.5294118     120.9453782    117.3529412     118.1512605     122.9411765     131.3235294      138.1092437      158.8655462      121.7014335     176.4285714     182.8151261      183.6134454      177.2268908                166.8487395                162.0588235                164.0546218                165.2521008                171.6386555                190               182.8151261                164.4537815                150.4831933                136.512605
b7        140.5042017     128.5294118     120.9453782    117.3529412     118.1512605     122.9411765     131.3235294      138.1092437      158.8655462      121.7014335     176.4285714     182.8151261      183.6134454      177.2268908                166.8487395                162.0588235                164.0546218                165.2521008                171.6386555                190               182.8151261                164.4537815                150.4831933                136.512605
b8        70.25210084     64.26470588     60.47268908    58.67647059     59.07563025     61.47058824     65.66176471      69.05462185      79.43277311      60.85071676     88.21428571     91.40756303      91.80672269      88.61344538                83.42436975                81.02941176                82.02731092                82.62605042                85.81932773                95                91.40756303                82.22689076                75.24159664                68.25630252
b9        70.25210084     64.26470588     60.47268908    58.67647059     59.07563025     61.47058824     65.66176471      69.05462185      79.43277311      60.85071676     88.21428571     91.40756303      91.80672269      88.61344538                83.42436975                81.02941176                82.02731092                82.62605042                85.81932773                95                91.40756303                82.22689076                75.24159664                68.25630252
b10       44.25882353     40.48676471     38.09779412    36.96617647     37.21764706     38.72647059     41.36691176      43.50441176      50.04264706      38.33595156     55.575          57.58676471      57.83823529      55.82647059                52.55735294                51.04852941                51.67720588                52.05441176                54.06617647                59.85             57.58676471                51.80294118                47.40220588                43.00147059
b11       140.5042017     128.5294118     120.9453782    117.3529412     118.1512605     122.9411765     131.3235294      138.1092437      158.8655462      121.7014335     176.4285714     182.8151261      183.6134454      177.2268908                166.8487395                162.0588235                164.0546218                165.2521008                171.6386555                190               182.8151261                164.4537815                150.4831933                136.512605
b12       70.25210084     64.26470588     60.47268908    58.67647059     59.07563025     61.47058824     65.66176471      69.05462185      79.43277311      60.85071676     88.21428571     91.40756303      91.80672269      88.61344538                83.42436975                81.02941176                82.02731092                82.62605042                85.81932773                95                91.40756303                82.22689076                75.24159664                68.25630252
b13       44.25882353     40.48676471     38.09779412    36.96617647     37.21764706     38.72647059     41.36691176      43.50441176      50.04264706      38.33595156     55.575          57.58676471      57.83823529      55.82647059                52.55735294                51.04852941                51.67720588                52.05441176                54.06617647                59.85             57.58676471                51.80294118                47.40220588                43.00147059
b14       70.25210084     64.26470588     60.47268908    58.67647059     59.07563025     61.47058824     65.66176471      69.05462185      79.43277311      60.85071676     88.21428571     91.40756303      91.80672269      88.61344538                83.42436975                81.02941176                82.02731092                82.62605042                85.81932773                95                91.40756303                82.22689076                75.24159664                68.25630252
b15       140.5042017     128.5294118     120.9453782    117.3529412     118.1512605     122.9411765     131.3235294      138.1092437      158.8655462      121.7014335     176.4285714     182.8151261      183.6134454      177.2268908                166.8487395                162.0588235                164.0546218                165.2521008                171.6386555                190               182.8151261                164.4537815                150.4831933                136.512605
;

Table
Imax(b,bb)   p.u.

     b1   b2    b3    b4    b5    b6   b7   b8   b9    b10   b11   b12   b13   b14   b15
b1   0    2     0     0     0     0    0    0    0     0     0     0     0     0     0
b2   2    0     1.89  0     0     2    0    0    1.266 0     0     0     0     0     0
b3   0    1.89  0     1.89  0     0    0    0    0     0     1.266 0     0     0     0
b4   0    0     1.89  0     1.266 0    0    0    0     0     0     0     0     1.266 1.266
b5   0    0     0     1.266 0     0    0    0    0     0     0     0     0     0     0
b6   0    2     0     0     0     0    2    2    0     0     0     0     0     0     0
b7   0    0     0     0     0     2    0    0    0     0     0     0     0     0     0
b8   0    0     0     0     0     2    0    0    0     0     0     0     0     0     0
b9   0    1.266 0     0     0     0    0    0    0     1.266 0     0     0     0     0
b10  0    0     0     0     0     0    0    0    1.266 0     0     0     0     0     0
b11  0    0     1.266 0     0     0    0    0    0     0     0     1.266 0     0     0
b12  0    0     0     0     0     0    0    0    0     0     1.266 0     1.266 0     0
b13  0    0     0     0     0     0    0    0    0     0     0     1.266 0     0     0
b14  0    0     0     1.266 0     0    0    0    0     0     0     0     0     0     0
b15  0    0     0     1.266 0     0    0    0    0     0     0     0     0     0     0
;

parameters
Rho_pv(spv)
/
spv1  0.2
spv2  0.6
spv3  0.2
/

Rho_w(sw)
/
sw1  0.2
sw2  0.6
sw3  0.2
/

Rl(l) Resistance of branches (OHM)
/
l1       1.35309
l2       1.17024
l3       0.84111
l4       1.52348
l5       2.01317
l6       1.68671
l7       2.55727
l8       1.08820
l9       1.25143
l10      1.79553
l11      2.44845
l12      2.01317
l13      2.23081
l14      1.19702
/

Xl(l) Reactance of branches  (OHM)
/
l1       1.32349
l2       1.14464
l3       0.82271
l4       1.02760
l5       1.35790
l6       1.13770
l7       1.72490
l8       0.73400
l9       0.84410
l10      1.21110
l11      1.65150
l12      1.35790
l13      1.50470
l14      0.80740
/

PrWh_el(t) Electricity wholesale price (Euro per kWh)
/
t1         0.037
t2         0.03039
t3         0.0272
t4         0.02499
t5         0.025
t6         0.02951
t7         0.04025
t8         0.0425
t9         0.0435
t10        0.0435
t11        0.04411
t12        0.04298
t13        0.04301
t14        0.04168
t15        0.03889
t16        0.04046
t17        0.04111
t18        0.045
t19        0.04468
t20        0.042
t21        0.04215
t22        0.04232
t23        0.042
t24        0.04012
/

Zl(l) Impedance of branches
Zl1(l)
GLine(l)
BLine(l)
YLinemag(l)
YLineang(l)

Yre(b,bb)       real part of Ybus elements
Yim(b,bb)       imaginary part of Ybus elements

Ymag(b,bb)      Ybus elements magnitude
Yang(b,bb)      Ybus elements Angle

Pw(sw,t)          pu amounts of wind generation (pu)
Ppv(spv,t)        pu amounts of pv generation (pu)

Rl1(b,bb)
Xl1(b,bb)
Zl2(b,bb)

PD(b,t)  Active power demand at buses [Pu]
QD(b,t)  Reactive power demand at buses [Pu]

V0_2(b,spv,sw,t)            Initialization of the voltage at node b   [pu]
DELTA_S(b,bb,spv,sw,t)      Variation of aparent power between nodes  [pu]
;

Rl(l)=Rl(l)/Zbase;
Xl(l)=Xl(l)/Zbase;
Zl(l)=sqrt(sqr(Rl(l))+sqr(Xl(l)));
Zl1(l)=sqr(Rl(l))+sqr(Xl(l));

Rl1(b,bb)=sum(l$(lines1(b,bb,l)),Rl(l))$(ord(b) ne ord(bb));
Xl1(b,bb)=sum(l$(lines1(b,bb,l)),Xl(l))$(ord(b) ne ord(bb));
Zl2(b,bb)=sum(l$(lines1(b,bb,l)),Zl1(l))$(ord(b) ne ord(bb));

GLine(l)=Rl(l)/(sqr(Rl(l))+sqr(Xl(l)));
BLine(l)=-Xl(l)/(sqr(Rl(l))+sqr(Xl(l)));
YLinemag(l)=sqrt(sqr(GLine(l))+sqr(BLine(l)));
YLineang(l)=arctan(BLine(l)/GLine(l))$(GLine(l) ne 0)-0.5*3.1416$(GLine(l)=0)+3.1416;

Yre(b,bb)=sum(l$(lines(b,bb,l)),GLine(l))$(ord(b)=ord(bb))-sum(l$(lines(b,bb,l)),GLine(l))$(ord(b) ne ord(bb));
Yim(b,bb)=sum(l$(lines(b,bb,l)),BLine(l))$(ord(b)=ord(bb))-sum(l$(lines(b,bb,l)),BLine(l))$(ord(b) ne ord(bb));
Yre(b,bb)$(ord(b)>ord(bb))=Yre(bb,b);
Yim(b,bb)$(ord(b)>ord(bb))=Yim(bb,b);

Ymag(b,bb)=sqrt(sqr(Yre(b,bb))+sqr(Yim(b,bb)));
Ymag(b,bb)$(ord(b)>ord(bb))=Ymag(bb,b);
Yang(b,bb)=arctan(Yim(b,bb)/Yre(b,bb))$(Yre(b,bb) ne 0)-0.5*3.1416$(Yre(b,bb)=0)+3.1416$(ord(b) ne ord(bb));
Yang(b,bb)$(ord(b)>ord(bb))=Yang(bb,b);

Pw(sw,t)=Wind_Rated*PwPU(sw,t)/Sbase;
Ppv(spv,t)=PV_Rated*PpvPU(spv,t)/Sbase;

PD(b,t)=(1000*ElectricDemand(b,t))/sbase;
QD(b,t)=PF*PD(b,t);

V0_2(b,spv,sw,t)=VNOM2;
DELTA_S(b,bb,spv,sw,t)=(VNOM*Imax(b,bb))/card(h);

variable
Fobj        Objective function
F1(spv,sw)
F2(spv,sw)
F3(spv,sw)
F1cost
F2cost
F3cost


Ploss(spv,sw,t)  Network loss at time t and senario s

** Calculations **
Pbuy(t)
Psell(t)
PDG(dg,t)
PChg(es,t)
PDchg(es,t)
SOE_ES(es,t)
PFL(fl,t)
P_pv(t)
P_wind(t)
Pload_final(t)
;

positive variable
Ps_buy(sb,spv,sw,t)   Active power buy from upstream grid [p.u]
Ps_sell(sb,spv,sw,t)  Active power sell from upstream grid [p.u]
Qs_buy(sb,spv,sw,t)   Reactive power imported from source buses [p.u]
Qs_sell(sb,spv,sw,t)  Reactive power exported to source buses [p.u]
P_DG(dg,spv,sw,t)     Active power generated by DGs [p.u]
Q_DG(dg,spv,sw,t)     Reactive power generated by DGs [p.u]
Pflex(fl,spv,sw,t)    Active power of flexible load [p.u]
Qflex(fl,spv,sw,t)    Reactive power of flexible load [p.u]
Pch(es,spv,sw,t)      Charging power of ES [p.u]
PDch(es,spv,sw,t)     Discharging power of ES [p.u]
SOE(es,spv,sw,t)      State of energy of ES [p.u]



V2(b,spv,sw,t)                          Voltage square at each bus
I2(b,bb,spv,sw,t)                       Current square at each branch
P_POS(b,bb,spv,sw,t)                    Positive active power flow
P_NEG(b,bb,spv,sw,t)                    Negative active power flow
Q_POS(b,bb,spv,sw,t)                    Positive reactive power flow
Q_NEG(b,bb,spv,sw,t)                    Negative reactive power flow
DELTA_P(b,bb,h,spv,sw,t)                Active power discretization block
DELTA_Q(b,bb,h,spv,sw,t)                Rective power discretization block
Ploss_b(b,bb,spv,sw,t)                  Power loss at each branch (pu)
;

V2.lo(b,spv,sw,t)=VMIN2;
V2.up(b,spv,sw,t)=VMAX2;
V2.l(b,spv,sw,t)=VNOM2;



binary variables
U_DG(dg,spv,sw,t)   Commitment status of DG units
VSU_DG(dg,spv,sw,t) is equal to 1 when dg is start
VSD_DG(dg,spv,sw,t) is equal to 1 when dg is shutdown
;

Equations
ObjectiveEquation        Total ObjectiveEquation
F1formula(spv,sw)             F1 ==> buy or sell cost from upstream grid
F2formula(spv,sw)             F2 ==> DG generation cost
F3formula(spv,sw)             F3 ==> Incentive payment to flexible loads


**Load Flow Equations**
Pbalance(b,spv,sw,t)          Nodal Active Power balance constraints
Qbalance(b,spv,sw,t)          Nodal ReActive Power balance constraints
Qimport(sb,spv,sw,t)
Qexport(sb,spv,sw,t)
E_BAL_V(b,bb,spv,sw,t)
E_POT_S(b,bb,spv,sw,t)
E_POT_P(b,bb,spv,sw,t)
E_POT_Q(b,bb,spv,sw,t)
E_COTA_DELTA_P(b,bb,h,spv,sw,t)
E_COTA_DELTA_Q(b,bb,h,spv,sw,t)
E_INT_MAX(b,bb,spv,sw,t)
E_L_POT1(b,bb,spv,sw,t)
E_L_POT2(b,bb,spv,sw,t)



**Loss Calculation**
Ploss1(b,bb,spv,sw,t)
P1oss2(spv,sw,t)

** DG Constraints **
ConstraintDG_1(dg,spv,sw,t)
ConstraintDG_2(dg,spv,sw,t)
ConstraintDG_3(dg,spv,sw,t)
ConstraintDG_4(dg,spv,sw,t)
ConstraintDG_5(dg,spv,sw,t)
ConstraintDG_6(dg,spv,sw,t)
ConstraintDG_7(dg,spv,sw,t)
ConstraintDG_8(dg,spv,sw,t)
ConstraintDG_9(dg,spv,sw,t)
ConstraintDG_10(dg,spv,sw,t)
ConstraintDG_11(dg,spv,sw,t)

** ES Constraints **
ConstraintES_1(es,spv,sw,t)
ConstraintES_2(es,spv,sw,t)
ConstraintES_3(es,spv,sw,t)
ConstraintES_4(es,spv,sw,t)
ConstraintES_5(es,spv,sw,t)
ConstraintES_6(es,spv,sw,t)
ConstraintES_7(es,spv,sw,t)

** Flexible load Constraints **
ConstraintFL_1(fl,spv,sw,t)
ConstraintFL_2(fl,spv,sw,t)
ConstraintFL_3(fl,spv,sw,t)
ConstraintFL_4(fl,spv,sw,t)


** Calculations **
calculation1(t)
calculation2(t)
calculation3(dg,t)
calculation4(es,t)
calculation5(es,t)
calculation6(es,t)
calculation7(fl,t)
calculation8(t)
calculation9(t)
calculation10(t)
calculation11
calculation12
calculation13
;

ObjectiveEquation..            Fobj=e=sum((spv,sw),Rho_pv(spv)*Rho_w(sw)*(F1(spv,sw)+F2(spv,sw)+F3(spv,sw)));
F1formula(spv,sw)..            F1(spv,sw)=e=sum((sb,t),(Sbase/1000)*(PrWh_el(t)*(Ps_buy(sb,spv,sw,t)-Ps_sell(sb,spv,sw,t))));
F2formula(spv,sw)..            F2(spv,sw)=e=sum((dg,t),(Sbase/1000)*P_DG(dg,spv,sw,t)*DGData(DG,'GenCost'))+sum((dg,t),DGData(DG,'SUC')*VSU_DG(dg,spv,sw,t))+sum((dg,t),DGData(DG,'SDC')*VSD_DG(dg,spv,sw,t));
F3formula(spv,sw)..            F3(spv,sw)=e=sum((fl,t),(Sbase/1000)*FLData(fl,'INC')*Pflex(fl,spv,sw,t));

*Active Power Balance [W]
Pbalance(b,spv,sw,t)..          sum(sb$(sourcebuses(sb,b)),(Ps_buy(sb,spv,sw,t)-Ps_sell(sb,spv,sw,t)))+(Ppv(spv,t)$(ord(b) eq Pvbus))+(Pw(sw,t)$(ord(b) eq Wbus))+sum(dg$(DGM(dg,b) EQ 1),P_DG(dg,spv,sw,t))+sum(fl$(FLM(fl,b) EQ 1),Pflex(fl,spv,sw,t))+sum(es$(ESM(es,b) EQ 1),(PDch(es,spv,sw,t)-Pch(es,spv,sw,t)))+sum[bb$bus(b,bb) , (P_POS(bb,b,spv,sw,t) - P_NEG(bb,b,spv,sw,t))]-sum[bb$bus(b,bb), (P_POS(b,bb,spv,sw,t) - P_NEG(b,bb,spv,sw,t)) + (Rl1(b,bb)* I2(b,bb,spv,sw,t))]=e=PD(b,t);

*Reactive Power Balance [W]
Qbalance(b,spv,sw,t)..          sum(sb$(sourcebuses(sb,b)),(Qs_buy(sb,spv,sw,t)-Qs_sell(sb,spv,sw,t)))+sum(dg$(DGM(dg,b) EQ 1),Q_DG(dg,spv,sw,t))+sum(fl$(FLM(fl,b) EQ 1),Qflex(fl,spv,sw,t))+sum[bb$bus(b,bb), (Q_POS(bb,b,spv,sw,t) - Q_NEG(bb,b,spv,sw,t))]- sum[bb$bus(b,bb), (Q_POS(b,bb,spv,sw,t) - Q_NEG(b,bb,spv,sw,t)) + (Xl1(b,bb)* I2(b,bb,spv,sw,t))]=e=QD(b,t);


Qimport(sb,spv,sw,t)..Qs_buy(sb,spv,sw,t) =e= PF*Ps_buy(sb,spv,sw,t);
Qexport(sb,spv,sw,t)..Qs_sell(sb,spv,sw,t) =e= PF*Ps_sell(sb,spv,sw,t);

*Node voltage Balance [pu]
E_BAL_V(b,bb,spv,sw,t)$bus(b,bb)..                      V2(b,spv,sw,t) - 2 * [Rl1(b,bb)*(P_POS(b,bb,spv,sw,t)-P_NEG(b,bb,spv,sw,t))+ Xl1(b,bb)*(Q_POS(b,bb,spv,sw,t)-Q_NEG(b,bb,spv,sw,t))]- [Zl2(b,bb)* I2(b,bb,spv,sw,t)] - V2(bb,spv,sw,t)=e=0;

*Linearizaton Balance [W]
E_POT_S(b,bb,spv,sw,t)$bus(b,bb)..                      V0_2(b,spv,sw,t) * I2(b,bb,spv,sw,t) =e= sum[h, (2 * ord(h) - 1)* DELTA_S(b,bb,spv,sw,t) * DELTA_P(b,bb,h,spv,sw,t)] + sum[h, (2*ord(h) - 1) * DELTA_S(b,bb,spv,sw,t) * DELTA_Q(b,bb,h,spv,sw,t)];

*Expression for the linearization block of active power [W]
E_POT_P(b,bb,spv,sw,t)$bus(b,bb)..                      P_POS(b,bb,spv,sw,t) + P_NEG(b,bb,spv,sw,t) =e= sum[h, DELTA_P(b,bb,h,spv,sw,t)];

*Expression for the linearization block of the reactive power [Var]
E_POT_Q(b,bb,spv,sw,t)$bus(b,bb)..                      Q_POS(b,bb,spv,sw,t) + Q_NEG(b,bb,spv,sw,t) =e= sum[h, DELTA_Q(b,bb,h,spv,sw,t)];

E_COTA_DELTA_P(b,bb,h,spv,sw,t)$bus(b,bb)..             DELTA_P(b,bb,h,spv,sw,t) =L= DELTA_S(b,bb,spv,sw,t);

E_COTA_DELTA_Q(b,bb,h,spv,sw,t)$bus(b,bb)..             DELTA_Q(b,bb,h,spv,sw,t) =L=  DELTA_S(b,bb,spv,sw,t);

E_INT_MAX(b,bb,spv,sw,t)$bus(b,bb)..                    I2(b,bb,spv,sw,t) =L= Imax(b,bb)*Imax(b,bb);

*Active power limits for the whole network [W]
E_L_POT1(b,bb,spv,sw,t)$bus(b,bb)..                    P_POS(b,bb,spv,sw,t) + P_NEG(b,bb,spv,sw,t) =L= VNOM *Imax(b,bb);

*Reactive power limits for the whole network [W]
E_L_POT2(b,bb,spv,sw,t)$bus(b,bb)..                    Q_POS(b,bb,spv,sw,t) + Q_NEG(b,bb,spv,sw,t) =L= VNOM *Imax(b,bb);


**Loss Calculation**
Ploss1(b,bb,spv,sw,t)..             Ploss_b(b,bb,spv,sw,t)=e=Rl1(b,bb)*I2(b,bb,spv,sw,t);
P1oss2(spv,sw,t)..                  Ploss(spv,sw,t)=e=sum[(b,bb),(Rl1(b,bb)*I2(b,bb,spv,sw,t))];


**DG Constraints**
ConstraintDG_1(dg,spv,sw,t)..(Sbase/1000)*P_DG(dg,spv,sw,t)=g=DGDATA(dg,'Pmin')*U_DG(dg,spv,sw,t);
ConstraintDG_2(dg,spv,sw,t)..(Sbase/1000)*P_DG(dg,spv,sw,t)=l=DGDATA(dg,'Pmax')*U_DG(dg,spv,sw,t);
ConstraintDG_3(dg,spv,sw,t)..(Sbase/1000)*Q_DG(dg,spv,sw,t)=g=DGDATA(dg,'Qmin')*U_DG(dg,spv,sw,t);
ConstraintDG_4(dg,spv,sw,t)..(Sbase/1000)*Q_DG(dg,spv,sw,t)=l=DGDATA(dg,'Qmax')*U_DG(dg,spv,sw,t);
ConstraintDG_5(dg,spv,sw,t)..(Sbase/1000)*(P_DG(dg,spv,sw,t+1)-P_DG(dg,spv,sw,t))=l=DGDATA(dg,'RU');
ConstraintDG_6(dg,spv,sw,t)..(Sbase/1000)*(P_DG(dg,spv,sw,t)-P_DG(dg,spv,sw,t+1))=l=DGDATA(dg,'RD');
ConstraintDG_7(dg,spv,sw,t)$(ord(t)>1)..U_DG(dg,spv,sw,t)-U_DG(dg,spv,sw,t-1)=e=VSU_DG(dg,spv,sw,t)-VSD_DG(dg,spv,sw,t);
ConstraintDG_8(dg,spv,sw,'t1')..U_DG(dg,spv,sw,'t1')=e=VSU_DG(dg,spv,sw,'t1')-VSD_DG(dg,spv,sw,'t1');
ConstraintDG_9(dg,spv,sw,t)..VSU_DG(dg,spv,sw,t)+VSD_DG(dg,spv,sw,t)=l=1;
ConstraintDG_10(dg,spv,sw,t)$(ord(t)<=24-DGDATA(dg,'MUT') and DGDATA(dg,'MUT')<>0)..DGDATA(dg,'MUT')*(U_DG(dg,spv,sw,t+1)-U_DG(dg,spv,sw,t))+sum(tt$(ord(tt)>=(ord(t)+1) and ord(tt)<=(ord(t)+DGDATA(dg,'MUT'))),(1-U_DG(dg,spv,sw,tt)))=l=DGDATA(dg,'MUT');
ConstraintDG_11(dg,spv,sw,t)$(ord(t)<=24-DGDATA(dg,'MDT') and DGDATA(dg,'MDT')<>0)..DGDATA(dg,'MDT')*(U_DG(dg,spv,sw,t)-U_DG(dg,spv,sw,t+1))+sum(tt$(ord(tt)>=(ord(t)+1) and ord(tt)<=(ord(t)+DGDATA(dg,'MDT'))),U_DG(dg,spv,sw,tt))=l=DGDATA(dg,'MDT');


**ES Constraints**
ConstraintES_1(es,spv,sw,t)..(Sbase/1000)*Pch(es,spv,sw,t)=l=ESDATA(es,'Pcap');
ConstraintES_2(es,spv,sw,t)..(Sbase/1000)*PDch(es,spv,sw,t)=l=ESDATA(es,'Pcap');
ConstraintES_3(es,spv,sw,t)$(ord(t)>1)..SOE(es,spv,sw,t)=e=SOE(es,spv,sw,t-1)+(ESDATA(es,'Eff')*Pch(es,spv,sw,t))-(PDch(es,spv,sw,t)/ESDATA(es,'Eff'));
ConstraintES_4(es,spv,sw,t)$(ord(t)=1)..SOE(es,spv,sw,'t1')=e=(1000*ESData(ES,'Emax')/Sbase)*ESDATA(es,'SOCini')+(ESDATA(es,'Eff')*Pch(es,spv,sw,'t1'))-(PDch(es,spv,sw,'t1')/ESDATA(es,'Eff'));
ConstraintES_5(es,spv,sw,t)..SOE(es,spv,sw,t)=l=ESDATA(es,'SOCmax')*(1000*ESData(ES,'Emax')/Sbase);
ConstraintES_6(es,spv,sw,t)..SOE(es,spv,sw,t)=g=ESDATA(es,'SOCmin')*(1000*ESData(ES,'Emax')/Sbase);
ConstraintES_7(es,spv,sw,'t24')..SOE(es,spv,sw,'t24')=g=ESDATA(es,'SOCini')*(1000*ESData(ES,'Emax')/Sbase);

** Flexible load Constraints **
ConstraintFL_1(fl,spv,sw,t)..Pflex(fl,spv,sw,t)=l=FLDATA(fl,'Alpha')*sum(b,FLM(fl,b)*PD(b,t));
ConstraintFL_2(fl,spv,sw,t)..(Sbase/1000)*(Pflex(fl,spv,sw,t+1)-Pflex(fl,spv,sw,t))=l=FLDATA(fl,'LR_pickup');
ConstraintFL_3(fl,spv,sw,t)..(Sbase/1000)*(Pflex(fl,spv,sw,t)-Pflex(fl,spv,sw,t+1))=l=FLDATA(fl,'LR_drop');
ConstraintFL_4(fl,spv,sw,t)..Qflex(fl,spv,sw,t)=e=PF*Pflex(fl,spv,sw,t);



** Calculations **
calculation1(t)..Pbuy(t)=e=sum((sb,spv,sw),(Rho_pv(spv)*Rho_w(sw)*Sbase/1000)*Ps_buy(sb,spv,sw,t));
calculation2(t)..Psell(t)=e=sum((sb,spv,sw),(Rho_pv(spv)*Rho_w(sw)*Sbase/1000)*Ps_sell(sb,spv,sw,t));
calculation3(dg,t)..PDG(dg,t)=e=sum((spv,sw),(Rho_pv(spv)*Rho_w(sw)*Sbase/1000)*P_DG(dg,spv,sw,t));
calculation4(es,t)..PChg(es,t)=e=sum((spv,sw),(Rho_pv(spv)*Rho_w(sw)*Sbase/1000)*Pch(es,spv,sw,t));
calculation5(es,t)..PDchg(es,t)=e=sum((spv,sw),(Rho_pv(spv)*Rho_w(sw)*Sbase/1000)*PDch(es,spv,sw,t));
calculation6(es,t)..SOE_ES(es,t)=e=sum((spv,sw),(Rho_pv(spv)*Rho_w(sw)*Sbase/1000)*SOE(es,spv,sw,t));
calculation7(fl,t)..PFL(fl,t)=e=sum((spv,sw),(Rho_pv(spv)*Rho_w(sw)*Sbase/1000)*Pflex(fl,spv,sw,t));
calculation8(t)..P_pv(t)=e=sum(spv,Rho_pv(spv)*Sbase/1000*Ppv(spv,t));
calculation9(t)..P_wind(t)=e=sum(sw,Rho_w(sw)*Sbase/1000*Pw(sw,t));
calculation10(t)..Pload_final(t)=e=sum((b,spv,sw),Rho_pv(spv)*Rho_w(sw)*(Sbase/1000)*(PD(b,t)-sum(fl,FLM(fl,b)*Pflex(fl,spv,sw,t))));
calculation11.. F1cost=e=sum((spv,sw),Rho_pv(spv)*Rho_w(sw)*F1(spv,sw));
calculation12.. F2cost=e=sum((spv,sw),Rho_pv(spv)*Rho_w(sw)*F2(spv,sw));
calculation13..F3cost=e=sum((spv,sw),Rho_pv(spv)*Rho_w(sw)*F3(spv,sw));

Model  SmartEnergyManagement /All/;
Option MIP = CPLEX;
option iterlim=100000000;
option reslim=1440000;
Solve SmartEnergyManagement using MIP minimizing Fobj;


*=== First unload to GDX file (occurs during execution phase)
*execute_unload "SEST.gdx" Fobj.l F1cost.l F2cost.l F3cost.l Pbuy.l Psell.l PDG.l PChg.l PDchg.l SOE_ES.l PFL.l P_pv.l P_wind.l Pload_final.l;
*=== Now write to variable levels to Excel file from GDX
*execute 'gdxxrw.exe SEST.gdx var=Fobj rng=Fobj! var=F1cost rng=F1cost! var=F2cost rng=F2cost! var=F3cost rng=F3cost! var=Pbuy rng=Pbuy! var=Psell rng=Psell! var=PDG rng=PDG! var=PChg rng=PChg! var=PDchg rng=PDchg! var=SOE_ES rng=SOE_ES! var=PFL rng=PFL! var=P_pv rng=P_pv! var=P_wind rng=P_wind! var=Pload_final rng=Pload_final!';


