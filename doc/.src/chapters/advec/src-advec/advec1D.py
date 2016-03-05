import numpy as np
import matplotlib.pyplot as plt

def solver_FECS(I, U0, v, L, dt, C, T, user_action=None):
    Nt = int(round(T/float(dt)))
    t = np.linspace(0, Nt*dt, Nt+1)   # Mesh points in time
    dx = v*dt/C
    Nx = int(round(L/dx))
    x = np.linspace(0, L, Nx+1)       # Mesh points in space
    # Make sure dx and dt are compatible with x and t
    dx = x[1] - x[0]
    dt = t[1] - t[0]
    C = v*dt/dx

    u   = np.zeros(Nx+1)
    u_1 = np.zeros(Nx+1)

    # Set initial condition u(x,0) = I(x)
    for i in range(0, Nx+1):
        u_1[i] = I(x[i])

    if user_action is not None:
        user_action(u_1, x, t, 0)

    for n in range(0, Nt):
        # Compute u at inner mesh points
        for i in range(1, Nx):
            u[i] = u_1[i] - 0.5*C*(u_1[i+1] - u_1[i-1])

        # Insert boundary condition
        u[0] = U0

        if user_action is not None:
            user_action(u, x, t, n+1)

        # Switch variables before next step
        u_1, u = u, u_1


def solver(I, U0, v, L, dt, C, T, user_action=None,
           scheme='FECS'):
    Nt = int(round(T/float(dt)))
    t = np.linspace(0, Nt*dt, Nt+1)   # Mesh points in time
    dx = v*dt/C
    Nx = int(round(L/dx))
    x = np.linspace(0, L, Nx+1)       # Mesh points in space
    # Make sure dx and dt are compatible with x and t
    dx = x[1] - x[0]
    dt = t[1] - t[0]
    C = v*dt/dx

    u   = np.zeros(Nx+1)
    u_1 = np.zeros(Nx+1)
    u_2 = np.zeros(Nx+1)

    # Set initial condition u(x,0) = I(x)
    for i in range(0, Nx+1):
        u_1[i] = I(x[i])

    if user_action is not None:
        user_action(u_1, x, t, 0)

    for n in range(0, Nt):
        if scheme == 'FECS':
            for i in range(1, Nx):
                u[i] = u_1[i] - 0.5*C*(u_1[i+1] - u_1[i-1])
        elif scheme == 'LFCS':
            if n == 0:
                # Use upwind for first step
                for i in range(1, Nx+1):
                    u[i] = u_1[i] - C*(u_1[i] - u_1[i-1])
            else:
                for i in range(1, Nx):
                    u[i] = u_2[i] - C*(u_1[i+1] - u_1[i-1])
            print n+1, u
        elif scheme == 'FEUS':
            for i in range(1, Nx+1):
                u[i] = u_1[i] - C*(u_1[i] - u_1[i-1])
        else:
            raise ValueError('scheme="%s" not implemented' % scheme)

        # Insert boundary condition
        u[0] = U0

        if user_action is not None:
            user_action(u, x, t, n+1)

        # Switch variables before next step
        u_2, u_1, u = u_1, u, u_2

def run_FSCS(case):
    if case == 'gaussian':
        def I(x):
            return np.exp(-0.5*((x-L/10)/sigma)**2)
    elif case == 'cosinehat':
        def I(x):
            return np.cos(np.pi*5/L*(x - L/10)) if x < L/5 else 0

    L = 1.0
    sigma = 0.02
    legends = []

    def plot(u, x, t, n):
        """Plot every m steps in the same figure."""
        m = 40
        if n % m != 0:
            return
        print 't=%g, n=%d, u in [%g, %g]' % \
              (t[n], n, u.min(), u.max())
        if np.abs(u).max() > 3:  # Instability?
            return
        plt.plot(x, u)
        legends.append('t=%g' % t[n])
        if n > 0:
            plt.hold('on')

    U0 = 0
    dt = 0.01
    C = 1
    T = 1
    solver(I=I, U0=U0, v=1.0, L=L, dt=dt, C=C, T=T,
           user_action=plot)
    plt.legend(legends, loc='lower left')
    plt.savefig('tmp.png'); plt.savefig('tmp.pdf')
    plt.axis([0, L, -0.75, 2])
    plt.show()

def run(scheme='FEUS', case='gaussian'):

    if case == 'gaussian':
        def I(x):
            return np.exp(-0.5*((x-L/10)/sigma)**2)
    elif case == 'cosinehat':
        def I(x):
            return np.cos(np.pi*5/L*(x - L/10)) if x < L/5 else 0

    L = 1.0
    sigma = 0.02
    legends = []

    def plot(u, x, t, n):
        """Plot every m steps in the same figure."""
        m = 4
        if n % m != 0:
            return
        print 't=%g, n=%d, u in [%g, %g]' % \
              (t[n], n, u.min(), u.max())
        if np.abs(u).max() > 3:  # Instability?
            return
        plt.plot(x, u)
        legends.append('t=%g' % t[n])
        if n > 0:
            plt.hold('on')

    U0 = 0
    dt = 0.1
    C = 1
    T = 1
    solver(I=I, U0=U0, v=1.0, L=L, dt=dt, C=C, T=T,
           scheme=scheme, user_action=plot)
    plt.legend(legends, loc='lower left')
    plt.savefig('tmp.png'); plt.savefig('tmp.pdf')
    plt.axis([0, L, -0.75, 2])
    plt.show()

if __name__ == '__main__':
    run(scheme='LFCS', case='gaussian')
    #run(solver, scheme='FECS', case='cosinehat')
    #run(solver_FE_CS, case='cosinehat')
