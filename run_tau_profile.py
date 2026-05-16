import argparse
from cobaya.run import run
taus = [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12]
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config",
        help="Base config name (with or without .yaml extension), e.g. cmb2pt_lite",
    )
    args = parser.parse_args()
    # accept both 'cmb2pt_lite' and 'cmb2pt_lite.yaml'
    stem = args.config[:-5] if args.config.endswith(".yaml") else args.config
    base = f"{stem}.yaml"
    taufn = lambda tau: f"chains/{stem}_tau={tau:.2f}"
    for tau in taus:
        override = {"params": {"tau": {"value": tau}}, "output": taufn(tau)}
        run(base, override=override, minimize=True, force=True)