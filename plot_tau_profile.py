import argparse
import numpy as np
import matplotlib.pyplot as plt
import yaml
import json


from getdist.types import BestFit
from run_tau_profile import taus


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config",
        help="Base config name (with or without .yaml extension), e.g. cmb2pt_lite",
    )
    args = parser.parse_args()

    stem  = args.config[:-5] if args.config.endswith(".yaml") else args.config
    taufn = lambda tau: f"chains/{stem}_tau={tau:.2f}"
    # Might want to pull in something from the config file, so load it here.
    with open(stem+'.yaml','r') as yfile:
        pars = yaml.safe_load(yfile)

    # load minima, skipping any tau whose minimization didn't finish / didn't write a usable file
    taus_used, chi2_used, omegam_used = [], [], []
    s8_used, H0_used, H0rd_used = [],[],[]
    for tau in taus:
        prefix = taufn(tau)
        try:
            bf = BestFit(prefix + ".minimum")
            c  = 2 * bf.logLike
            om = bf.parWithName("OmegaM").best_fit
            s8 = bf.parWithName("sigma8").best_fit
            H0 = bf.parWithName("H0").best_fit
            H0rd = bf.parWithName("H0rd").best_fit
            #
            taus_used.append(tau)
            chi2_used.append(c)
            omegam_used.append(om)
            s8_used.append(s8)
            H0_used.append(H0)
            H0rd_used.append(H0)
        except Exception as e:
            print(f"  skipping tau={tau:.3f}: {type(e).__name__}: {e}")
            continue

    if not taus_used:
        raise SystemExit(f"No usable .minimum files found for config '{stem}'.")

    taus_arr   = np.array(taus_used)
    chi2_arr   = np.array(chi2_used)
    omegam_arr = np.array(omegam_used)
    dchi2      = chi2_arr - chi2_arr.min()

    # table
    print(f"\n{'tau':>6} {'chi2':>14} {'dchi2':>10} {'OmegaM':>10}")
    for t, c, d, om in zip(taus_arr, chi2_arr, dchi2, omegam_arr):
        print(f"{t:6.3f} {c:14.4f} {d:10.4f} {om:10.4f}")
    print(f"\nMinimum chi2 at tau = {taus_arr[np.argmin(chi2_arr)]:.3f}")

    # JSON file.
    dd = {}
    dd['run_name'  ] = rf"CMB 2pt: {stem}"
    dd['tau'       ] = taus_arr.tolist()
    dd['OmegaM'    ] = omegam_arr.tolist()
    dd['dchi2'     ] = dchi2.tolist()
    dd['chi_min'   ] = float(np.min(chi2_arr))
    dd['tau_min'   ] = float(taus_arr[np.argmin(chi2_arr)])
    dd['sigma8'    ] = s8_used
    dd['H0'        ] = H0_used
    dd['H0rd'      ] = H0rd_used
    dd['likelihood'] = pars['likelihood']
    outpath = f"tau_profile_{stem}.json"
    with open(outpath,"w") as fout:
        json.dump(dd,fout,indent=4)
        print(f"\nSaved {outpath}",flush=True)

    # plot
    fig, ax = plt.subplots(figsize=(6.5, 4.25))
    l1, = ax.plot(taus_arr, dchi2, "o-", color="C0", label=r"$\Delta\chi^2$")
    ax.axhline(1, ls=":", color="gray", lw=1)
    ax.axhline(4, ls=":", color="gray", lw=1)
    ax.text(taus_arr[-1], 1.05, r"$1\sigma$", color="gray", va="bottom", ha="right")
    ax.text(taus_arr[-1], 4.05, r"$2\sigma$", color="gray", va="bottom", ha="right")
    ax.set_xlabel(r"$\tau$")
    ax.set_ylabel(r"$\Delta\chi^2(\tau)$", color="C0")
    ax.tick_params(axis="y", labelcolor="C0")
    ax.grid(alpha=0.3)

    ax2 = ax.twinx()
    l2, = ax2.plot(taus_arr, omegam_arr, "s--", color="C3", label=r"$\Omega_{\rm m}$")
    ax2.set_ylabel(r"$\Omega_{\rm m}$", color="C3")
    ax2.tick_params(axis="y", labelcolor="C3")

    ax.legend(handles=[l1, l2], loc="best", frameon=False)
    title = rf"CMB 2pt: {stem}"
    title = r"CMBp 2pt: PR4 ($30<\ell<1000$) + DR6 ($1000<\ell<4000$) + SPT-3G D1"
    plt.title(title)
    plt.tight_layout()
    outpath = f"tau_profile_{stem}.pdf"
    plt.savefig(outpath, bbox_inches="tight")
    print(f"Saved {outpath}")
    outpath = f"tau_profile_{stem}.png"
    plt.savefig(outpath, bbox_inches="tight",dpi=300)
    print(f"Saved {outpath}")
