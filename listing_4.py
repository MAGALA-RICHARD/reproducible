"""
Example: Mixed-variable optimization in apsimNGpy

This listing demonstrates how to configure and execute a mixed-variable
optimization problem combining continuous and discrete decision variables.
Both local (e.g., Powell, Nelder–Mead, etc...) and global (Differential Evolution)
methods can be used to estimate APSIM parameters against observed data.

Author
    Magala et al. (2025).
"""
import numpy as np
from apsimNGpy.optimizer.minimize.single_mixed import MixedVariableOptimizer
from apsimNGpy.optimizer.problems.smp import MixedProblem
from apsimNGpy.optimizer.problems.variables import UniformVar, QrandintVar
from apsimNGpy.tests.unittests.test_factory import obs

if __name__ == "__main__":
    # -------------------------------------------------------------
    # 1. Define the mixed-variable optimization problem
    # -------------------------------------------------------------
    mp = MixedProblem(
        model="Maize",
        trainer_dataset=obs,
        pred_col="Yield",
        metric="wia",
        index="year",
        trainer_col="observed"
    )

    # -------------------------------------------------------------
    # 2. Define continuous and cultivar-specific optimization factors
    # -------------------------------------------------------------

    # (a) Continuous initial fresh soil organic matter factor
    soil_param = {
        "path": ".Simulations.Simulation.Field.Soil.Organic",
        "vtype": [UniformVar(1, 200)],
        "start_value": [1],
        "candidate_param": ["FOM"],
        "other_params": {"FBiom": 0.04, "Carbon": 1.89},
    }

    # (b) Cultivar-specific physiological factor
    cultivar_param = {
        "path": ".Simulations.Simulation.Field.Maize.CultivarFolder.Dekalb_XL82",
        "vtype": [ QrandintVar(400, 900, q=10)],  # Discrete step size of 2
        "start_value": [ 600],
        "candidate_param": [
                            '[Phenology].GrainFilling.Target.FixedValue'],
        "other_params": {"sowed": True},
        "cultivar": True,  # Signals to apsimNGpy to treat it as a cultivar parameter
    }
    rue = {
        "path": ".Simulations.Simulation.Field.Maize.CultivarFolder.Dekalb_XL82",
        'vtype': [ UniformVar(0.8,2.2),],
        'start_value': [1,],
        'candidate_param': ['[Leaf].Photosynthesis.RUE.FixedValue',],
        'other_params':{'sowed': True},
        "cultivar": True,
    }

    # Submit optimization factors
    #mp.submit_factor(**soil_param)
    mp.submit_factor(**rue)
   # mp.submit_factor(**cultivar_param)

    print(f" {mp.n_factors} optimization factors registered.")

    # -------------------------------------------------------------
    # 3. Configure and execute the optimizer
    # -------------------------------------------------------------
    from scipy.optimize import NonlinearConstraint


    def hess(x):
        return np.zeros((len(x), len(x)))
    minim = MixedVariableOptimizer(problem=mp)
    nlc = NonlinearConstraint(mp.evaluate_objectives, lb=-1.1, ub=-0.98)
    #tc=minim.minimize_with_local(method="trust-constr", constraints=[nlc],  # or empty list if you don't want nonlinear constraints
    #options={"verbose": 3}, hess=hess )
    #print(tc)
    de = minim.minimize_with_de(
        use_threads=True,
        updating="deferred",
        workers=14,  # Number of parallel workers
        popsize=30,  # Population size per generation
        constraints=nlc,
    )
    print(de)
    # (a) Local optimization examples
    import gc
    gc.collect()
    nelda = minim.minimize_with_local(method="Nelder-Mead")
    print(nelda)
    powell = minim.minimize_with_local(method="Powell")
    print(powell)
    sqlp = minim.minimize_with_local(method="L-BFGS-B", options={
        "gtol": 1e-12,
        "ftol": 1e-12,
        "maxfun": 50000,
        "maxiter": 30000
    })

    print(sqlp)
    bfgs = minim.minimize_with_local(method="BFGS")
    print(bfgs)

    print("\nOptimization completed:")
    import matplotlib.pyplot as plt
    import os
   # sns.relplot(x="year", y="y")
    plt.figure(figsize=(8, 6))
    df= de.data
    df.eval('ayield =Yield/1000', inplace=True)
    df.eval('oyield =observed/1000', inplace=True)
    # observed → scatter points
    plt.scatter(df["year"], df["ayield"], label="APSIM", s=60, color='red')

    # predicted → line
    plt.plot(df["year"], df["oyield"], label="Training data", linewidth=2)

    plt.xlabel("Time (Year)", fontsize=18)
    plt.ylabel("Maize grain yield (Mg ha⁻¹)", fontsize=18)
    plt.title("") #Observed vs Predicted Yield Over Time
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures.png")
    os.startfile("figures.png")
    plt.close()

