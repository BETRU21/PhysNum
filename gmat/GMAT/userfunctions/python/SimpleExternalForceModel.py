#Part of the sample Ex_R2022a_ExternalForceModel.script
#Must be in this folder until the external force model plugin can support user defined file locations

import math
#-------------------------------------------------------------------------------------------------------
# a = SimpleExternalForceModel.GetForces(s,t,o):
#-------------------------------------------------------------------------------------------------------
#*
#* Comuptes 2 body derivative of the state
#*
#* @param s - state vector (x,y,z, vx, vy, vz) km, km/sec
#* @param t - The current time. (In days from 05-JAN-1941 12:00:00 TAI)
#* @param o - order of derivative. 
#*
#* @return the Derivatives vector
#*
#-------------------------------------------------------------------------------------------------------

def GetForces(s,t,o):
    r = s[0:3]                                      # State of the spacecraft, just getting position info
    v = s[3:6]
    mu = 3.986004415e5                              # Earth M * G
    R=math.sqrt((r[0]**2)+(r[1]**2)+(r[2]**2))      # Distance of Spacecraft from origin (central body)
    a = mu/R**2                                     # Acceleration magnitude from eq. a = mu/R^2
    ds = [v[0],v[1],v[2],                           # Acceleration occurs in direction from spacecraft 
        a*(-(r[0]/R)),a*(-(r[1]/R)),a*(-(r[2]/R))]  #   towards the origin
    return ds                                       # (km/s, km/s, km/s, km/s^2, km/s^2, km/s^2)
    
#-------------------------------------------------------------------------------------------------------
# a = SimpleExternalForceModel.GetDelayForce(s,t,o):
#-------------------------------------------------------------------------------------------------------
#*
#* Computes an Anti Acceleration force 
#*
#* @param s - state vector (x,y,z, vx, vy, vz) km, km/sec
#* @param t - The current time. (In days from 05-JAN-1941 12:00:00 TAI)
#* @param o - order of derivative. 
#*
#* @return the Derivatives vector
#*
#-------------------------------------------------------------------------------------------------------
    
def GetDelayForce(s,t,o):
    v = s[3:6]
    norm = math.sqrt((v[0]**2)+(v[1]**2)+(v[2]**2))
    Accel = -1e-6   
    ds = [v[0],v[1],v[2], Accel*(v[0]/norm), Accel*(v[1]/norm), Accel*(v[2]/norm)]
    return ds