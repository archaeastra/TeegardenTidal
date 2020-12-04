*****
Tidal Effects on the Planets of Teegarden’s Star
=====================================

Overview
--------
A Monte Carlo simulation of the tidal effects present in the Teegarden system, a solar system comprised of two Earth-mass 
planets with dense atmospheres in the habitable zone of a M type red dwarf star, with focus on Cassini States, obliquity evolution and tidal heating.

===================   ============
**Date**              04/12/20
**Author**            Ilyana A. Guez
**Modules**           DistOrb
                      DistRot
                      EqTide
                      STELLAR
**Approx. runtime**   1 week
===================   ============

This set-up allows the user to generate simulation data and plot results for a simulation of the Teegarden system with random variations in the parameters:
 - Cosine of Obliquity
 - Eccentricity
 - Inclination
 - Mass
 - Longitude of Ascending Node
 - Longitude of Pericenter
 - Precession Angle
 - Tidal Tau
 
 The different plotting routines are:
 - CSOH, Cassini State Obliquity Histogram. Figure 2 in the paper.
 - THeP, Tidal Heating Plot. Figure 3 in the paper.
 - THeSP, Tidal heating Substraction Plot. Figure 4 in the paper.
 - POE, Plot of Orbital Evolution. Figure 5 in the paper.


To run this example
-------------------

.. code-block:: bash
    vspace vspace.in
    multi-planet vspace.in <no. cores>
    python THeSP_Control.py
    python [RoutineName].py <pdf | png>

Note, the second step of this code block can take several days to complete. It is recommended to shunt this process to the background.

Expected output
---------------

.. figure::  	[RoutineName].png
   :width: 150px
   :align: left
.. figure::  	[RoutineName].png
   :width: 150px
   :align: right  
