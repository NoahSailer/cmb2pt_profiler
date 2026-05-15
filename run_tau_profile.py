from cobaya.run import run
base = "cmb2pt_lite.yaml"
taus = [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12]
taufn = lambda tau: f"chains/cmb2pt-lite_tau={tau:.2f}"
if __name__ == "__main__":
    for tau in taus:
        override = {"params": {"tau": {"value": tau}}, "output": taufn(tau)}
        run(base, override=override, minimize=True, force=True)